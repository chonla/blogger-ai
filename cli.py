import os
from dotenv import load_dotenv

from agent.editor_agent import EditorAgent
from agent.seo_agent import SEOAgent
from agent.writer_agent import WriterAgent
from publisher.markdown import MarkdownPublisher
from studio.blog_studio import BlogStudio


load_dotenv()

if __name__ == "__main__":
    preferred_language = "Thai"
    writer_llm = os.getenv("WRITER_LLM", "ollama://llama2:13b")
    editor_llm = os.getenv("EDITOR_LLM", "ollama://llama2:13b")
    seo_llm = os.getenv("SEO_LLM", "ollama://llama2:13b")
    
    writer = WriterAgent(writer_llm, preferred_language)
    editor = EditorAgent(editor_llm)
    seo = SEOAgent(seo_llm, preferred_language)
    publisher = MarkdownPublisher()
    
    studio = BlogStudio(writer, editor, seo, publisher)
    studio.create_blog_post("ประโยชน์ของการทำสมาธิต่อสุขภาพจิต")