from llm.llm import LLM


def create_llm(llm: str, system_instruction: str = None) -> LLM:
    [namespace, model_name] = llm.split("://", 1)
    if namespace == "ollama":
        from .ollama import Ollama
        return Ollama(model_name, system_instruction)
    elif namespace == "google":
        if model_name.startswith("gemini-"):
            from .gemini import Gemini
            return Gemini(model_name, system_instruction)
    elif namespace == "openai":
        if model_name.startswith("gpt-"):
            from .openai import OpenAI
            return OpenAI(model_name, system_instruction)
    raise ValueError(f"Unsupported model: {llm}")