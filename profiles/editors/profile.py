from textwrap import dedent


class EditorProfile(dict):
    """Profile for an editor with attributes and instruction generation."""
    
    def __init__(self, name: str, gender: str, expertise: str, position: str, 
                additional_instructions: str):
        super().__init__(
            name=name,
            gender=gender,
            expertise=expertise,
            position=position,
            additional_instructions=additional_instructions
        )
    
    def instruction(self) -> str:
        return dedent(f"""Name:{self['name']}
            Gender:{self['gender']}
            Expertise:{self['expertise']}
            Additional Instructions:{self['additional_instructions']}""")
