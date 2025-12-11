from llm.llm import LLM


def use_model(llm: str) -> LLM:
    [namespace, model_name] = llm.split("://", 1)
    if namespace == "ollama":
        from .ollama import Ollama
        return Ollama(model_name)
    elif namespace == "google":
        if model_name.startswith("gemini-"):
            from .gemini import Gemini
            return Gemini(model_name)
    elif namespace == "openai":
        if model_name.startswith("gpt-"):
            from .openai import OpenAI
            return OpenAI(model_name)
    raise ValueError(f"Unsupported model: {llm}")