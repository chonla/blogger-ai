import unittest

from extractor.json_object import extract_json_objects
from extractor.section import extract_section


class ExtractJsonObjectsTests(unittest.TestCase):
    def test_single_object_is_returned(self):
        text = 'prefix {"a": 1} suffix'
        self.assertEqual(extract_json_objects(text), ['{"a": 1}'])

    def test_multiple_objects_with_nested_content(self):
        text = 'x {"a": {"b": 2}} y {"c": 3}'
        self.assertEqual(
            extract_json_objects(text),
            ['{"a": {"b": 2}}', '{"c": 3}'],
        )

    def test_braces_inside_strings_are_ignored(self):
        text = '{"text": "{ not a brace }"}{"next": 1}'
        self.assertEqual(
            extract_json_objects(text),
            ['{"text": "{ not a brace }"}', '{"next": 1}'],
        )

    def test_unclosed_brace_returns_empty(self):
        self.assertEqual(extract_json_objects('{"a": 1'), [])


class ExtractSectionTests(unittest.TestCase):
    def test_extracts_between_start_and_end_markers(self):
        text = """Intro
START OF INTRO
Hello there
END OF INTRO
Outro"""
        self.assertEqual(extract_section(text, "INTRO"), "Hello there")

    def test_handles_bold_markers(self):
        text = """**START OF SUMMARY**
Summary text
**END OF SUMMARY**"""
        self.assertEqual(extract_section(text, "SUMMARY"), "Summary text")

    def test_stops_at_next_section_when_no_end_marker(self):
        text = """START OF INTRO
First part
START OF CONCLUSION
Second part
END OF CONCLUSION"""
        self.assertEqual(extract_section(text, "INTRO"), "First part")

    def test_returns_empty_string_when_section_missing(self):
        text = """START OF BODY
Something here
END OF BODY"""
        self.assertEqual(extract_section(text, "INTRO"), "")


if __name__ == "__main__":
    unittest.main()
