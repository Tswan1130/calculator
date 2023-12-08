import tkinter as tk
from tkinter import messagebox
from calculator import Calculator
from data_handling import DataLogger

class CalculatorApp(tk.Tk):
    """GUI application for the calculator."""

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.calculator = Calculator()
        self.data_logger = DataLogger()
        self.result_displayed = False
        self.create_widgets()
        self.current_input = []

    def create_widgets(self):
        # Display Field
        self.display_var = tk.StringVar()
        self.display = tk.Entry(self, textvariable=self.display_var, justify='right', font=('Arial', 16))
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Button Layout
        btn_texts = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1),
            ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
            ('C', 4, 0), ('=', 4, 2)
        ]

        for (text, row, col) in btn_texts:
            button = tk.Button(self, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew")

        # Configure row/column weights
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, text):
        if text == 'C':
            # Clear the current input
            self.current_input.clear()
            self.display_var.set('')
        elif text == '=':
            # Perform the calculation
            self.calculate_result()
            # After calculation, set a flag indicating result was just displayed
            self.result_displayed = True
        else:
            if self.result_displayed and text in ['+', '-', '*', '/']:
                # If a result was just displayed and an operator is pressed,
                # continue with the result for a new operation
                self.current_input = [self.display_var.get(), text]
                self.result_displayed = False
            elif self.result_displayed or not self.current_input:
                # If a result was just displayed or there's no current input, start a new input
                self.current_input = [text]
                self.result_displayed = False
            else:
                # Regular input handling
                if text.isdigit() or text == '.':
                    if self.current_input[-1] in ['+', '-', '*', '/']:
                        self.current_input.append(text)
                    else:
                        self.current_input[-1] += text
                else:
                    if self.current_input[-1] in ['+', '-', '*', '/']:
                        self.current_input[-1] = text
                    else:
                        self.current_input.append(text)

            self.display_var.set(''.join(self.current_input))
    def calculate_result(self):
        try:
            expression = ''.join(self.current_input)
            values = []
            if '/' in expression:
                values = expression.split('/')
                result = self.calculator.divide([float(v) for v in values])
            elif '*' in expression:
                values = expression.split('*')
                result = self.calculator.multiply([float(v) for v in values])
            elif '+' in expression:
                values = expression.split('+')
                result = self.calculator.add([float(v) for v in values])
            elif '-' in expression:
                values = expression.split('-')
                result = self.calculator.subtract([float(v) for v in values])
            else:
                result = float(expression)

            self.display_var.set(str(result))
            self.data_logger.log_operation(expression, [float(v) for v in values if v], result)
            self.current_input = [str(result)]  # Store the result for potential further operations
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.current_input.clear()
            self.display_var.set('')


app = CalculatorApp()
app.mainloop()
