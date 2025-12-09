import re


def extract_section(text, section_title):
    section_start_pattern = re.compile(rf"(\*\*)?START OF {section_title}(\*\*)?")
    section_end_pattern = re.compile(rf"(\*\*)?END OF {section_title}(\*\*)?")
    other_section_start_pattern = re.compile(r"(\*\*)?START OF [A-Z ]+(\*\*)?")
    match = re.search(section_start_pattern, text)
    
    if match:
        start_index = match.end()
        end_match = re.search(section_end_pattern, text[start_index:])
        if end_match:
            end_index = start_index + end_match.start()
            return text[start_index:end_index].strip()
        other_section_match = re.search(other_section_start_pattern, text[start_index:])
        if other_section_match:
            end_index = start_index + other_section_match.start()
            return text[start_index:end_index].strip()
        return text[start_index:].strip()
    return ""