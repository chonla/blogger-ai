class Pen:
    GRAY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY_BRIGHT = "\033[90;1m"
    RED_BRIGHT = "\033[91;1m"
    GREEN_BRIGHT = "\033[92;1m"
    YELLOW_BRIGHT = "\033[93;1m"
    BLUE_BRIGHT = "\033[94;1m"
    MAGENTA_BRIGHT = "\033[95;1m"
    CYAN_BRIGHT = "\033[96;1m"
    WHITE_BRIGHT = "\033[97;1m"
    RESET = "\033[0m"

    def gray(self, text: str) -> str:
        return self.colorize_text(text, self.GRAY)
    
    def red(self, text: str) -> str:
        return self.colorize_text(text, self.RED)
    
    def green(self, text: str) -> str:
        return self.colorize_text(text, self.GREEN)
    
    def yellow(self, text: str) -> str:
        return self.colorize_text(text, self.YELLOW)
    
    def blue(self, text: str) -> str:
        return self.colorize_text(text, self.BLUE)
    
    def magenta(self, text: str) -> str:
        return self.colorize_text(text, self.MAGENTA)
    
    def cyan(self, text: str):
        return self.colorize_text(text, self.CYAN)
    
    def white(self, text: str) -> str:
        return self.colorize_text(text, self.WHITE)
    
    def gray_bright(self, text: str) -> str:
        return self.colorize_text(text, self.GRAY_BRIGHT)
    
    def red_bright(self, text: str) -> str:
        return self.colorize_text(text, self.RED_BRIGHT)
    
    def green_bright(self, text: str) -> str:
        return self.colorize_text(text, self.GREEN_BRIGHT)
    
    def yellow_bright(self, text: str) -> str:
        return self.colorize_text(text, self.YELLOW_BRIGHT)
    
    def blue_bright(self, text: str) -> str:
        return self.colorize_text(text, self.BLUE_BRIGHT)
    
    def magenta_bright(self, text: str) -> str:
        return self.colorize_text(text, self.MAGENTA_BRIGHT)
    
    def cyan_bright(self, text: str) -> str:
        return self.colorize_text(text, self.CYAN_BRIGHT)
    
    def white_bright(self, text: str) -> str:
        return self.colorize_text(text, self.WHITE_BRIGHT)

    def colorize_text(self, text: str, color: str) -> str:
        if "\n" in text:
            lines = text.split("\n")
            colored_lines = [self.colorize_text(line, color) for line in lines]
            return "\n".join(colored_lines)
        return f"{color}{text}{self.RESET}"

pen = Pen()
