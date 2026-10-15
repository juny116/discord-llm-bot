"""Load only the dependencies needed by the selected v1 backend."""


def load_model(config):
    kind = config["type"]
    if kind in {"chatgpt", "openai"}:
        from .hosted_models import ChatGPT, OpenAIGPT

        cls = {"chatgpt": ChatGPT, "openai": OpenAIGPT}[kind]
    elif kind in {"flan-ul2", "flan-t5", "vicuna"}:
        from .local_models import FlanT5, FlanUL2, Vicuna

        cls = {"flan-ul2": FlanUL2, "flan-t5": FlanT5, "vicuna": Vicuna}[kind]
    else:
        raise ValueError(f"Unknown v1 model type: {kind}")
    return cls(config)
