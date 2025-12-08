class Logger:
    def __init__(self, namespace: str, color: callable):
        self.namespace = namespace
        self.color = color

    def log(self, message: str):
        print(f"[{self.color(self.namespace)}] {message}", flush=True)

    def log_block(self, title: str, content: str):
        print(f"[{self.color(self.namespace)}] {title}\n{'=' * len(title)}\n{content}\n{'=' * len(title)}", flush=True)

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