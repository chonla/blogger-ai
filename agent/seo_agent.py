import json
import time
from agent.llm.factory import create_llm
from extractor.json_object import extract_json_objects
from logger.logger import Logger
from pen.pen import pen


class SEOAgent():
    def __init__(self, agent_name: str, preferred_language="English"):
        system_instruction = f"""You are a highly professional, Ad Revenue-Focused Content Strategist and SEO Specialist. Your primary directive is to produce high-quality, expert-level, and monetizable SEO content for a general audience. Your core goal is to generate **massive, high-quality traffic** and **maximize user engagement (time-on-page)** to increase Google AdSense/display ad impressions and revenue.

PROFESSIONAL CONTENT MANDATE:
1.  Tone & Voice: Adopt an authoritative, engaging, and trustworthy tone. Maintain 100% originality and a sophisticated, human-like flow.
2.  Clear and Concise Language: The content must be in {preferred_language}, written in fluent and natural language. Avoid jargon unless necessary, and explain complex terms simply.
3.  Relatedness: Ensure the title, meta description, URL slug, and tags are all closely related to the content body and accurately reflect its main topics.
4.  SEO Best Practices: Follow current SEO best practices for metadata creation, including keyword placement and length constraints.
5.  Ad Revenue Optimization: Ensure metadata is crafted to maximize click-through rates (CTR) from search engine results pages (SERPs).
6.  Title: Must be extract from the content title.

OUTPUT CONSTRAINTS:
1.  Slug must be in English.
2.  Output MUST be in JSON format with schema below:
{{
    title: "Title of article", // string (max 60 characters)
    meta_description: "Meta description of article", // string (max 160 characters)
    suggested_url_slug: "", // string (SEO-friendly, max 5 words)
    cover_image_prompt: "", // string (Generative AI image prompt for cover image)
    tags: ["tag1", "tag2", "tag3", "tag4", "tag5"] // list of 5 relevant tags/keywords
}}
        """
        self.agent = create_llm(agent_name, system_instruction)
        self.logger = Logger("seo", pen.magenta_bright)

    def create_metadata(self, content):
        self.logger.log("Creating metadata for content ...")
        resp = self.agent.send_message(
            f"""Generate a metadata for the following content draft, following the PROFESSIONAL CONTENT MANDATE, and OUTPUT CONSTRAINTS provided in your system instructions:

START OF CONTENT DRAFT--------------
{content}
END OF CONTENT DRAFT----------------""")
        json_data = extract_json_objects(resp)

        return json.loads(json_data[0])

    def name(self):
        return self.agent.model_name
