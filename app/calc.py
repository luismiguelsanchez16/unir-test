import math

import app


class InvalidPermissions(Exception):
    pass


class Calculator:
    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def substract(self, x, y):
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y):
        if not app.util.validate_permissions(f"{x} * {y}", "user1"):
            raise InvalidPermissions('User has no permissions')

        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")

        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        try:
            return math.pow(x, y)
        except (ValueError, OverflowError) as error:
            raise TypeError(f"Power {x}^{y} cannot be calculated") from error

    def sqrt(self, x):
        self.check_types(x)
        if x < 0:
            raise TypeError("Square root of a negative number is not possible")

        return math.sqrt(x)

    def log10(self, x):
        self.check_types(x)
        if x <= 0:
            raise TypeError("Logarithm is only defined for numbers greater than zero")

        return math.log10(x)

    @staticmethod
    def check_types(*values):
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError("Parameters must be numbers")


if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
