import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from logger.logger import Logger
from pen.pen import pen


class LoggerTests(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("APP", lambda text: f"<{text}>")
        self.logger.set_level("INFO")

    def capture_output(self, func, *args, **kwargs):
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue()

    def test_log_prints_colored_namespace_and_message(self):
        out = self.capture_output(self.logger.log, "hello")
        self.assertEqual(out, "[<APP>] hello\n")

    def test_log_block_prints_delimited_block(self):
        title = "TITLE"
        content = "details"
        delimiter = "=" * (len(title) + len(self.logger.namespace) + 3)
        expected = f"[<APP>] {title}\n{delimiter}\n{content}\n{delimiter}\n"
        out = self.capture_output(self.logger.log_block, title, content)
        self.assertEqual(out, expected)

    def test_log_time_taken_uses_formatted_elapsed_time(self):
        out = self.capture_output(self.logger.log_time_taken, 1.5)
        self.assertEqual(out, "[<APP>] time taken 1.50 seconds\n")

    def test_format_elapsed_time_ranges(self):
        self.assertEqual(self.logger.format_elapsed_time(5), "5.00 seconds")
        self.assertEqual(self.logger.format_elapsed_time(75), "1 minute, 15.00 seconds")
        self.assertEqual(
            self.logger.format_elapsed_time(3725),
            "1 hour, 2 minutes, 5.00 seconds",
        )

    def test_debug_no_output_when_not_in_debug_level(self):
        out = self.capture_output(self.logger.debug, "hidden")
        self.assertEqual(out, "")

    def test_debug_outputs_when_log_level_debug(self):
        self.logger.set_level("DEBUG")
        out = self.capture_output(self.logger.debug, "shown")
        expected = f"[<APP>] {pen.gray('shown')}\n"
        self.assertEqual(out, expected)

    def test_debug_block_outputs_gray_block(self):
        self.logger.set_level("DEBUG")
        title = "TITLE"
        content = "content"
        line_length = len(title) + len(self.logger.namespace) + 3
        delimiter = pen.gray("=" * line_length)
        expected = (
            f"[<APP>] {title}\n"
            f"{delimiter}\n"
            f"{pen.gray(content)}\n"
            f"{delimiter}\n"
        )
        out = self.capture_output(self.logger.debug_block, title, content)
        self.assertEqual(out, expected)


if __name__ == "__main__":
    unittest.main()
