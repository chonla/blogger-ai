import os
from dotenv import load_dotenv

from profiles.profiles import profiles
from publisher.screen import ScreenPublisher
from studio.editor_agent import EditorAgent
from studio.marketer_agent import MarketerAgent
from studio.writer_agent import WriterAgent
# from publisher.markdown import MarkdownPublisher
from studio.studio import Studio
from llm.factory import use_model


load_dotenv()

if __name__ == "__main__":
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    blog_topic = "Next generation of rubber duck debugging"
    blog_language = "Thai"
    
    writer_llm = use_model(os.getenv("WRITER_LLM", "ollama://llama2:13b"))
    writer_llm.with_instruction(profiles["alice"].instruction())

    editor_llm = use_model(os.getenv("EDITOR_LLM", "ollama://llama2:13b"))
    editor_llm.with_instruction(profiles["bob"].instruction())
    
    marketer_llm = use_model(os.getenv("MARKETER_LLM", "ollama://llama2:13b"))
    marketer_llm.with_instruction(profiles["carol"].instruction())
    
    writer_agent = WriterAgent(writer_llm)
    editor_agent = EditorAgent(editor_llm)
    marketer_agent = MarketerAgent(marketer_llm)
    
    blog_studio = Studio(
        writer=writer_agent,
        editor=editor_agent,
        marketer=marketer_agent,
        log_level=log_level
    )
    content = blog_studio.create_entry(blog_topic, blog_language)
    if content is not None:
        publisher = ScreenPublisher()
        publisher.publish(content["content"], content["metadata"])
