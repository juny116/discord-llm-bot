import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from discord_llm.message_formatting import (
    add_author,
    convert_id_to_name,
    convert_name_to_id,
    remove_author,
)
from discord_llm.v2.conversation_model import DirectAPIConversationModel


class FormattingTests(unittest.TestCase):
    def test_unknown_and_nickname_mentions(self):
        self.assertEqual(
            convert_id_to_name(
                {"12345678901234567": "Alice"},
                "<@!12345678901234567> <@99999999999999999>",
            ),
            "<@Alice> <@99999999999999999>",
        )
        self.assertEqual(
            convert_name_to_id({"Alice": "123"}, "<@Alice> <@unknown>"),
            "<@123> <@unknown>",
        )
        self.assertEqual(remove_author("Al", "Alice: hello"), "Alice: hello")
        self.assertEqual(add_author("Al", "Already here"), "Al: Already here")
        self.assertEqual(remove_author("Al", "Al: hi"), "hi")

    def test_direct_provider_response_shapes(self):
        config = {
            "type": "openai",
            "model_name": "test",
            "max_tokens": 20,
            "temperature": 0,
        }
        history = SimpleNamespace(
            get_messages=lambda: [SimpleNamespace(type="human", content="hi")]
        )
        for response in [
            "hello",
            {"messages": [{"role": "assistant", "content": "hello"}], "error": None},
        ]:
            calls = []

            def generate(messages, **kwargs):
                calls.append((messages, kwargs))
                return response

            model = DirectAPIConversationModel(
                config, client=SimpleNamespace(generate=generate), token_counter=len
            )
            self.assertEqual(model.generate(history, "Bot"), ("Bot: hello", 10))
            self.assertEqual(calls[0][0], [{"role": "user", "content": "hi"}])
        model = DirectAPIConversationModel(
            config,
            client=SimpleNamespace(generate=lambda *a, **k: {"error": "failed"}),
            token_counter=len,
        )
        with self.assertRaisesRegex(RuntimeError, "failed"):
            model.generate(history, "Bot")

    def test_both_version_entrypoints(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "config.yaml").write_text("model: {}\n")
            for version in ["v1", "v2"]:
                proc = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "discord_llm",
                        version,
                        "--config-dir",
                        directory,
                        "--cfg",
                        "job",
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn("model: {}", proc.stdout)


class BotTests(unittest.IsolatedAsyncioTestCase):
    async def test_message_and_token_window_command(self):
        import discord
        from discord_llm.bot import LLMBot
        from discord_llm.conversation_memory import ChatMessageHistoryWithContextWindow
        from langchain.schema import SystemMessage

        model = SimpleNamespace(
            get_num_tokens=len, generate=lambda history, name: ("Bot: hello", 10)
        )
        bot = LLMBot(
            {"model": {}, "long_term_memory": False},
            discord.Intents.none(),
            model_factory=lambda cfg: model,
        )
        bot._connection.user = SimpleNamespace(
            name="Bot", mentioned_in=lambda msg: True
        )
        bot.history = ChatMessageHistoryWithContextWindow(100)
        bot.history.set_system_message(
            SystemMessage(content="system", additional_kwargs={"token_length": 6})
        )
        bot.current_turn = 0
        bot.max_turns = 3
        bot.name_to_id = {}
        bot.id_to_name = {}
        channel = SimpleNamespace(send=AsyncMock())
        message = SimpleNamespace(
            author=SimpleNamespace(name="Alice"), content="hello", channel=channel
        )
        await bot.on_message(message)
        channel.send.assert_awaited_with("hello")
        self.assertEqual(bot.current_turn, 1)
        message.content = "!max_token 200"
        await bot.on_message(message)
        self.assertEqual(bot.history.window_size, 200)
        self.assertIn("200", channel.send.call_args.args[0])
        message.content = "!memorize"
        await bot.on_message(message)
        self.assertIn("not enabled", channel.send.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
