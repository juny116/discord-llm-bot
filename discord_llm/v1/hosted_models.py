"""LangChain chat and completion model backends."""

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import AIMessage

from discord_llm.message_formatting import messages_to_prompt


class ChatGPT:
    def __init__(self, config):
        self.config = config
        self.model = ChatOpenAI(
            model_name=self.config["model_name"],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"],
        )
        print(self.model.json)

    def generate(self, history, name):
        messages = history.get_messages()
        # For debug purposes
        prompt = messages_to_prompt(messages)
        print(prompt)
        messages.append(AIMessage(content=f"{name}:"))
        response = self.model(messages=messages).content.strip()
        response = f"{name}: " + response
        token_length = self.model.get_num_tokens(response)

        print(response)
        return response, token_length

    def get_num_tokens(self, text):
        return self.model.get_num_tokens(text)


class OpenAIGPT:
    def __init__(self, config):
        self.config = config
        self.model = OpenAI(
            model_name=self.config["model_name"],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"],
        )
        print(self.model.json)

    def generate(self, history, name):
        prompt = history.get_prompt() + f"{name}:"
        print(prompt)
        response = self.model(prompt).strip()
        response = f"{name}: " + response
        token_length = self.model.get_num_tokens(response)
        print(response)
        return response, token_length

    def get_num_tokens(self, text):
        return self.model.get_num_tokens(text)
