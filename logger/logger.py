import os

from pen.pen import pen


class Logger:
    def __init__(self, namespace: str, color: callable, log_level: str = "INFO"):
        self.namespace = namespace
        self.color = color
        self.set_level(log_level)
        
    def set_level(self, level: str):
        self.log_level = level.upper()
        
    def debug(self, message: str):
        if self.log_level == "DEBUG":
            print(f"[{self.color(self.namespace)}] {pen.gray(message)}", flush=True)
    
    def debug_block(self, title: str, content: str):
        if self.log_level == "DEBUG":
            line_length = len(title) + len(self.namespace) + 3
            block_delimiter = f"{pen.gray('=' * line_length)}"
            print(f"[{self.color(self.namespace)}] {title}\n{block_delimiter}\n{pen.gray(content)}\n{block_delimiter}", flush=True)

    def log(self, message: str):
        print(f"[{self.color(self.namespace)}] {message}", flush=True)

    def log_block(self, title: str, content: str):
        line_length = len(title) + len(self.namespace) + 3
        block_delimiter = '=' * line_length
        print(f"[{self.color(self.namespace)}] {title}\n{block_delimiter}\n{content}\n{block_delimiter}", flush=True)

    def log_time_taken(self, time_taken_in_second: float):
        print(f"[{self.color(self.namespace)}] time taken {self.format_elapsed_time(time_taken_in_second)}", flush=True)

    def format_elapsed_time(self, seconds: float):
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}, {remaining_seconds:.2f} seconds"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            remaining_seconds = seconds % 60
            return f"{hours} hour{'s' if hours != 1 else ''}, {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}, {remaining_seconds:.2f} seconds"