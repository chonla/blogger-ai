import unittest

from pen.pen import Pen, pen


class PenColorMethodsTests(unittest.TestCase):
    def setUp(self):
        self.pen = Pen()
        self.colors = {
            "gray": Pen.GRAY,
            "red": Pen.RED,
            "green": Pen.GREEN,
            "yellow": Pen.YELLOW,
            "blue": Pen.BLUE,
            "magenta": Pen.MAGENTA,
            "cyan": Pen.CYAN,
            "white": Pen.WHITE,
            "gray_bright": Pen.GRAY_BRIGHT,
            "red_bright": Pen.RED_BRIGHT,
            "green_bright": Pen.GREEN_BRIGHT,
            "yellow_bright": Pen.YELLOW_BRIGHT,
            "blue_bright": Pen.BLUE_BRIGHT,
            "magenta_bright": Pen.MAGENTA_BRIGHT,
            "cyan_bright": Pen.CYAN_BRIGHT,
            "white_bright": Pen.WHITE_BRIGHT,
        }

    def test_color_methods_wrap_text_with_reset(self):
        for method_name, color in self.colors.items():
            with self.subTest(method=method_name):
                method = getattr(self.pen, method_name)
                self.assertEqual(method("hello"), f"{color}hello{Pen.RESET}")

    def test_colorize_text_handles_newlines_per_line(self):
        text = "line1\nline2"
        expected = f"{Pen.RED}line1{Pen.RESET}\n{Pen.RED}line2{Pen.RESET}"
        self.assertEqual(self.pen.colorize_text(text, Pen.RED), expected)

    def test_module_level_pen_is_usable(self):
        self.assertIsInstance(pen, Pen)
        self.assertEqual(pen.blue("ok"), f"{Pen.BLUE}ok{Pen.RESET}")


if __name__ == "__main__":
    unittest.main()
