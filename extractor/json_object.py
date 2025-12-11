def extract_json_objects(text) -> list[str]:
    objs = []
    brace_level = 0
    start = None
    in_string = False
    escape = False

    for i, ch in enumerate(text):
        if ch == '"' and not escape:
            in_string = not in_string

        if ch == "\\" and not escape:
            escape = True
        else:
            escape = False

        if not in_string:
            if ch == "{":
                if brace_level == 0:
                    start = i
                brace_level += 1
            elif ch == "}":
                brace_level -= 1
                if brace_level == 0 and start is not None:
                    chunk = text[start:i+1]
                    objs.append(chunk)

        # continue scanning

    return objs