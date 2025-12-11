from textwrap import dedent


class WriterProfile(dict):
    """Profile for a writer with attributes and instruction generation."""
    
    def __init__(self, name: str, gender: str, expertise: str, position: str, 
                 tone: str, writing_style: str, additional_instructions: str):
        super().__init__(
            name=name,
            gender=gender,
            expertise=expertise,
            position=position,
            tone=tone,
            writing_style=writing_style,
            additional_instructions=additional_instructions
        )
    
    def instruction(self) -> str:
        return dedent(f"""Name:{self['name']}
            Gender:{self['gender']}
            Expertise:{self['expertise']}
            Tone:{self['tone']}
            Writing Style:{self['writing_style']}
            Additional Instructions:{self['additional_instructions']}""")
