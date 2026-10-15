"""Adapt direct SDK responses to the shared conversation-model interface."""

from .providers import AutoModelForAPI


class DirectAPIConversationModel:
    def __init__(self, config, *, client=None, token_counter=None):
        self.config = config
        self.client = client or AutoModelForAPI(
            config["type"],
            model=config["model_name"],
            api_key=config.get("api_key"),
            max_retry=config.get("max_retry", 5),
            timeout=config.get("timeout", 120),
        )
        if token_counter is None:
            import tiktoken

            encoding = tiktoken.get_encoding("cl100k_base")
            token_counter = lambda text: len(encoding.encode(text))
        self.token_counter = token_counter

    def get_num_tokens(self, text):
        return self.token_counter(text)

    def generate(self, history, name):
        roles = {"human": "user", "ai": "assistant", "system": "system"}
        messages = [
            {"role": roles[m.type], "content": m.content}
            for m in history.get_messages()
        ]
        result = self.client.generate(
            messages,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
        )
        if isinstance(result, dict):
            if result.get("error"):
                raise RuntimeError(result["error"])
            text = result["messages"][-1]["content"]
        else:
            text = result
        response = name + ": " + (text or "").strip()
        return response, self.get_num_tokens(response)
