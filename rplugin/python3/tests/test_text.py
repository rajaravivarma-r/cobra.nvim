import unittest

from text import Text


class TestTextMethods(unittest.TestCase):

    def test_is_snake_case(self):
        self.assertTrue(Text("hello_world").is_snake_case())
        self.assertFalse(Text("HelloWorld").is_snake_case())

    def test_is_pascal_case(self):
        self.assertTrue(Text("HelloWorld").is_pascal_case())
        self.assertFalse(Text("hello_world").is_pascal_case())
        self.assertFalse(Text("helloWorld").is_pascal_case())

    def test_is_camel_case(self):
        self.assertTrue(Text("helloWorld").is_camel_case())
        self.assertFalse(Text("HelloWorld").is_camel_case())
        self.assertFalse(Text("hello_world").is_camel_case())

    def test_is_constant_case(self):
        self.assertTrue(Text("HELLO_WORLD").is_constant_case())
        self.assertFalse(Text("HelloWorld").is_constant_case())
        self.assertFalse(Text("hello_world").is_constant_case())

    def test_convert_to_constant_case(self):
        self.assertEqual(Text("hello_world").convert_to_constant_case(), "HELLO_WORLD")
        self.assertEqual(Text("HelloWorld").convert_to_constant_case(), "HELLO_WORLD")
        self.assertEqual(Text("helloWorld").convert_to_constant_case(), "HELLO_WORLD")

    def test_convert_to_camel_case(self):
        self.assertEqual(Text("hello_world").convert_to_camel_case(), "helloWorld")
        self.assertEqual(Text("HELLO_WORLD").convert_to_camel_case(), "helloWorld")
        self.assertEqual(Text("HelloWorld").convert_to_camel_case(), "helloWorld")
        self.assertEqual(Text("helloWorld").convert_to_camel_case(), "helloWorld")

    def test_convert_to_snake_case(self):
        self.assertEqual(Text("helloWorld").convert_to_snake_case(), "hello_world")
        self.assertEqual(Text("HelloWorld").convert_to_snake_case(), "hello_world")
        self.assertEqual(Text("already_snake").convert_to_snake_case(), "already_snake")

    def test_pascal_case_to_constant_case(self):
        self.assertEqual(
            Text("HelloWorld").pascal_case_to_constant_case(), "HELLO_WORLD"
        )

    def test_pascal_case_to_snake_case(self):
        self.assertEqual(Text("HelloWorld").pascal_case_to_snake_case(), "hello_world")

    def test_snake_case_to_constant_case(self):
        self.assertEqual(
            Text("hello_world").snake_case_to_constant_case(), "HELLO_WORLD"
        )

    def test_snake_case_to_camel_case(self):
        self.assertEqual(Text("hello_world").snake_case_to_camel_case(), "helloWorld")

    def test_camel_case_to_snake_case(self):
        self.assertEqual(Text("helloWorld").camel_case_to_snake_case(), "hello_world")


if __name__ == "__main__":
    unittest.main()
