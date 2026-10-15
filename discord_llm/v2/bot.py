"""Run the v2 Discord conversation bot."""

import discord
import hydra

from discord_llm.bot import LLMBot

from .conversation_model import DirectAPIConversationModel as load_model


@hydra.main(version_base=None, config_path=None, config_name="config")
def main(config):
    client = LLMBot(config, discord.Intents.all(), model_factory=load_model)
    client.run(config["discord"]["token"])


if __name__ == "__main__":
    main()
