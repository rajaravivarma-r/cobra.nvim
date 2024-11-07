import re


class Text:
    def __init__(self, value):
        self.value = value

    def is_snake_case(self):
        if "_" in self.value:
            if self.value.lower() == self.value:
                return True
        return False

    def is_pascal_case(self):
        if self.value[0].isupper() and any(char.islower() for char in self.value):
            return True
        return False

    def is_camel_case(self):
        return bool(re.match(r"^[a-z]+(?:[A-Z][a-z]*)*$", self.value))

    def is_constant_case(self):
        return self.value.isupper() and "_" in self.value

    def convert_to_constant_case(self):
        if self.is_constant_case():
            return self.value
        elif self.is_pascal_case():
            return self.pascal_case_to_constant_case()
        elif self.is_snake_case():
            return self.snake_case_to_constant_case()
        elif self.is_camel_case():
            return self.camel_case_to_constant_case()
        else:
            raise ValueError("Don't know how to handle conversion for this")

    def convert_to_camel_case(self):
        if self.is_camel_case():
            return self.value
        elif self.is_snake_case():
            return self.snake_case_to_camel_case()
        elif self.is_constant_case():
            return self.constant_case_to_camel_case()
        elif self.is_pascal_case():
            return self.pascal_case_to_camel_case()
        else:
            raise ValueError("Don't know how to handle conversion for this")

    def convert_to_snake_case(self):
        if self.is_camel_case():
            return self.camel_case_to_snake_case()
        elif self.is_pascal_case():
            return self.pascal_case_to_snake_case()
        else:
            return self.value

    def pascal_case_to_constant_case(self):
        words = re.findall(r"[A-Z][a-z]+", self.value)
        constant_word = [w.upper() for w in words]
        return "_".join(constant_word)

    def pascal_case_to_snake_case(self):
        snake_str = re.sub(r"(?<!^)([A-Z])", r"_\1", self.value).lower()
        return snake_str

    def pascal_case_to_camel_case(self):
        return self.value[0].lower() + self.value[1:]

    def snake_case_to_constant_case(self):
        return self.value.upper()

    def snake_case_to_camel_case(self):
        words = self.value.split("_")
        first_word = words.pop(0)
        capitalized_words = [first_word] + [w.capitalize() for w in words]
        return "".join(capitalized_words)

    def snake_case_to_pascal_case(self):
        words = self.value.split("_")
        first_word = words.pop(0)
        capitalized_words = [first_word.capitalize()] + [w.capitalize() for w in words]
        return "".join(capitalized_words)

    def camel_case_to_snake_case(self):
        snake_str = re.sub(r"([A-Z])", r"_\1", self.value).lower()
        return snake_str.lstrip("_")

    def camel_case_to_constant_case(self):
        constant_str = re.sub(r'([a-z])([A-Z])', r'\1_\2', self.value).upper()
        return constant_str

    def constant_case_to_camel_case(self):
        words = self.value.lower().split("_")
        first_word = words.pop(0)
        capitalized_words = [first_word] + [w.capitalize() for w in words]
        return "".join(capitalized_words)
