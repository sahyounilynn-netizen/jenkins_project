# tests/test_app.py
import contextlib
import io
import os
import runpy
import unittest

from app import greet, main

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")


class TestApp(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World from Lynn Sahyouni!")

    def test_greet_other_name(self):
        self.assertEqual(greet("Jenkins"), "Hello, Jenkins from Lynn Sahyouni!")

    def test_greet_empty_name(self):
        self.assertEqual(greet(""), "Hello,  from Lynn Sahyouni!")

    def test_main_prints_and_returns_greeting(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = main()
        self.assertEqual(result, "Hello, World from Lynn Sahyouni!")
        self.assertEqual(buffer.getvalue(), "Hello, World from Lynn Sahyouni!\n")

    def test_script_entry_point(self):
        # Runs app.py as a script so the ``if __name__ == "__main__"`` path is exercised.
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            runpy.run_path(APP_PATH, run_name="__main__")
        self.assertEqual(buffer.getvalue().strip(), "Hello, World from Lynn Sahyouni!")


if __name__ == "__main__":
    unittest.main()
