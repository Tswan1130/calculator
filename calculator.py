class Calculator:
    """Class for performing arithmetic operations."""

    def add(self, values: list[float]) -> float:
        return sum(values)

    def subtract(self, values: list[float]) -> float:
        return values[0] - sum(values[1:])

    def multiply(self, values: list[float]) -> float:
        result = 1
        for value in values:
            result *= value
        return result

    def divide(self, values: list[float]) -> float:
        result = values[0]
        for value in values[1:]:
            if value == 0:
                raise ValueError("Cannot divide by zero")
            result /= value
        return result
