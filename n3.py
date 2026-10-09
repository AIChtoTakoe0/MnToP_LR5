import tkinter as tk
from tkinter import messagebox


class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Задание 3. Простейший калькулятор")
        self.root.geometry("340x260")
        self._build_ui()

    def _build_ui(self) -> None:
        tk.Label(self.root, text="Число 1:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry1 = tk.Entry(self.root, width=15)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Число 2:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry2 = tk.Entry(self.root, width=15)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        self.result_var = tk.StringVar(value="Результат: —")
        tk.Label(self.root, textvariable=self.result_var).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        operations = [
            ("+", lambda a, b: a + b),
            ("-", lambda a, b: a - b),
            ("*", lambda a, b: a * b),
            ("/", lambda a, b: a / b),
        ]

        frame = tk.Frame(self.root)
        frame.grid(row=3, column=0, columnspan=2, pady=5)

        for symbol, operation in operations:
            button = tk.Button(
                frame,
                text=symbol,
                width=4,
                command=lambda s=symbol, op=operation: self.calculate(s, op),
            )
            button.pack(side="left", padx=3)

    def _get_numbers(self):
        try:
            first = float(self.entry1.get())
            second = float(self.entry2.get())
            return first, second
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
            return None

    def calculate(self, symbol: str, operation) -> None:
        numbers = self._get_numbers()
        if numbers is None:
            return

        first, second = numbers

        try:
            if symbol == "/" and second == 0:
                raise ZeroDivisionError
            result = operation(first, second)
            if float(result).is_integer():
                result = int(result)
            self.result_var.set(f"Результат: {result}")
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль")
            self.result_var.set("Результат: ошибка")


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
