# 파일 대응표

| 이전 경로 | 현재 경로 |
|---|---|
| `llmbot.py` | `discord_llm/bot.py + discord_llm/v1/bot.py + discord_llm/v2/bot.py` |
| `models.py` | `discord_llm/v1/{model_backends,hosted_models,local_models}.py` |
| `api_adapters/` | `discord_llm/v2/providers/` |
| `memory.py` | `discord_llm/conversation_memory.py` |
| `utils.py` | `discord_llm/message_formatting.py` |
| `utilbot.py` | `discord_llm/moderation_bot.py` |
