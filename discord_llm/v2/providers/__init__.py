"""Direct SDK adapters loaded per provider."""


def AutoModelForAPI(model_type, **kwargs):
    if model_type == "openai":
        from .openai_client import OpenAIGPT

        return OpenAIGPT(**kwargs)
    if model_type == "google":
        from .gemini_client import GoogleGemini

        return GoogleGemini(**kwargs)
    raise ValueError(f"Unknown API provider: {model_type}")
