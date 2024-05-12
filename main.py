import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Global variable to store the previous result
previous_result = None

# Function to evaluate the expression entered by the user
def evaluate_expression():
    global previous_result
    try:
        result = eval(entry.get())
        # Check if the result is an integer or float
        if isinstance(result, (int, float)):
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result) + '\n')
            previous_result = result  # Store the result for future use
        else:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error\n")
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error\n")

# Function to handle button clicks and insert the corresponding symbol into the entry field
def button_click(symbol):
    if entry.get().endswith("\n"):
        clear_entry()
    elif entry.get().endswith(str(previous_result)):
        clear_entry()
    elif symbol in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'ln']:
        # If the button pressed is a function, automatically insert '(' after the function
        entry.insert(tk.END, symbol + '(')
    entry.insert(tk.END, symbol)

# Function to clear the entry field
def clear_entry():
    entry.delete(0, tk.END)

# Function to use the previous result in the entry field
def use_previous_result():
    global previous_result
    if entry.get().endswith("Error\n"):
        clear_entry()
    if previous_result is not None:
        entry.insert(tk.END, str(previous_result))

# Function to switch to the advanced calculator window
def switch_to_advanced_calculator():
    root.withdraw()  # Hide the main calculator window
    advanced_calculator_window = tk.Toplevel(root)
    advanced_calculator_window.title("Advanced Calculator")
    advanced_calculator_window.configure(bg='#000000')  # Set background color

    # Function to evaluate the expression entered in the advanced calculator
    def evaluate_advanced_expression():
        try:
            # Evaluate the expression with custom functions for trigonometric and logarithmic calculations
            result = eval(advanced_entry.get(), {'__builtins__': None}, {"sin": math.sin, "cos": math.cos, "tan": math.tan,
                                                                   "cot": lambda x: 1 / math.tan(x),
                                                                   "sec": lambda x: 1 / math.cos(x),
                                                                   "csc": lambda x: 1 / math.sin(x),
                                                                   "log": math.log10, "ln": math.log})
            if isinstance(result, (int, float)):
                advanced_entry.delete(0, tk.END)
                advanced_entry.insert(tk.END, str(result) + '\n')
            else:
                advanced_entry.delete(0, tk.END)
                advanced_entry.insert(tk.END, "Error\n")
        except:
            advanced_entry.delete(0, tk.END)
            advanced_entry.insert(tk.END, "Error\n")

    # Function to handle button clicks in the advanced calculator
    def button_click_advanced(symbol):
        if advanced_entry.get().endswith("\n"):
            clear_entry_advanced()
        advanced_entry.insert(tk.END, symbol)

    # Function to clear the entry field in the advanced calculator
    def clear_entry_advanced():
        advanced_entry.delete(0, tk.END)

    # Entry widget for the advanced calculator
    advanced_entry = tk.Entry(advanced_calculator_window, width=30, borderwidth=5, font=('Arial', 16), bg='#000000', fg='#FFFFFF')
    advanced_entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    # Define buttons for advanced calculator
    advanced_buttons = [
        ('sin', 'cos', 'tan', '(', ')'),
        ('cot', 'sec', 'csc', 'log', 'ln'),
        ('7', '8', '9', '/', 'C'),
        ('4', '5', '6', '*', ''),
        ('1', '2', '3', '-', ''),
        ('0', '.', '=', '+', '')
    ]

    # Place buttons on the grid
    row_num = 1
    col_num = 0
    for row in advanced_buttons:
        for button in row:
            if button == '=':
                tk.Button(advanced_calculator_window, text=button, padx=20, pady=10, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=evaluate_advanced_expression).grid(row=row_num, column=col_num, padx=5, pady=5)
            elif button == 'C':
                tk.Button(advanced_calculator_window, text=button, padx=20, pady=10, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=clear_entry_advanced).grid(row=row_num, column=col_num, padx=5, pady=5)
            else:
                tk.Button(advanced_calculator_window, text=button, padx=20, pady=10, font=('Arial', 16), bg='#000000', fg='#FFFFFF', command=lambda symbol=button: button_click_advanced(symbol)).grid(row=row_num, column=col_num, padx=5, pady=5)
            col_num += 1
        col_num = 0
        row_num += 1

    # Button to go back to the main calculator window
    back_button = tk.Button(advanced_calculator_window, text="Back to Calculator", padx=40, pady=20, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=lambda: back_to_calculator(advanced_calculator_window))
    back_button.grid(row=row_num, column=0, columnspan=5, padx=10, pady=10)

# Function to switch to the graph calculator window
def switch_to_graph_calculator():
    root.withdraw()  # Hide the main calculator window
    graph_calculator_window = tk.Toplevel(root)
    graph_calculator_window.title("Graph Calculator")
    graph_calculator_window.configure(bg='#000000')  # Set background color

    # Function to plot the graph based on the expression entered
    def plot_graph():
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(graph_entry.get())
            ax.clear()
            ax.plot(x, y)
            ax.axhline(0, color='black',linewidth=0.5)
            ax.axvline(0, color='black',linewidth=0.5)
            ax.grid(True, which='both')
            ax.set_title('Graph')
            canvas.draw()
        except:
            graph_entry.delete(0, tk.END)
            graph_entry.insert(tk.END, "Error")

    # Entry widget for the graph calculator
    graph_entry = tk.Entry(graph_calculator_window, width=30, borderwidth=5, font=('Arial', 16), bg='#000000', fg='#FFFFFF')
    graph_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Button to plot the graph
    plot_button = tk.Button(graph_calculator_window, text="Plot", padx=40, pady=20, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=plot_graph)
    plot_button.grid(row=0, column=3, padx=10, pady=10)

    # Create matplotlib figure and canvas for plotting
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=graph_calculator_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # Button to go back to the main calculator window
    back_button = tk.Button(graph_calculator_window, text="Back to Calculator", padx=40, pady=20, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=lambda: back_to_calculator(graph_calculator_window))
    back_button.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

# Function to switch back to the main calculator window
def back_to_calculator(window):
    window.destroy()
    root.deiconify()  # Show the main calculator window

# Create main window
root = tk.Tk()
root.title("Calculator")
root.configure(bg='#000000')  # Set background color

# Create entry widget
entry = tk.Entry(root, width=30, borderwidth=5, font=('Arial', 24), bg='#000000', fg='#FFFFFF')  # Set font and colors
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Define buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+',
    'ans', '.', '(', ')',
    'Advance', 'Graph'
]

# Place buttons on the grid
row_num = 1
col_num = 0
for button in buttons:
    if button == '=':
        tk.Button(root, text=button, padx=20, pady=10, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=evaluate_expression).grid(row=row_num, column=col_num, padx=5, pady=5)
    elif button == 'C':
        tk.Button(root, text=button, padx=20, pady=10, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=clear_entry).grid(row=row_num, column=col_num, padx=5, pady=5)
    elif button == 'ans':
        tk.Button(root, text=button, padx=20, pady=10, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=use_previous_result).grid(row=row_num, column=col_num, padx=5, pady=5)
    elif button == 'Advance':
        tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=switch_to_advanced_calculator).grid(row=row_num, column=col_num, padx=5, pady=5, columnspan=2, sticky="ew")
        col_num += 1
    elif button == 'Graph':
        tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 16), bg='#FFA500', fg='#FFFFFF', command=switch_to_graph_calculator).grid(row=row_num, column=col_num, padx=5, pady=5, columnspan=2, sticky="ew")
        col_num += 1
    elif button in ['(', ')']:
        tk.Button(root, text=button, padx=20, pady=10, font=('Arial', 16), bg='#000000', fg='#FFFFFF', command=lambda symbol=button: button_click(symbol)).grid(row=row_num, column=col_num, padx=5, pady=5)
    else:
        tk.Button(root, text=button, padx=20, pady=10, font=('Arial', 16), bg='#000000', fg='#FFFFFF', command=lambda symbol=button: button_click(symbol)).grid(row=row_num, column=col_num, padx=5, pady=5)
    col_num += 1
    if col_num > 3:
        col_num = 0
        row_num += 1

root.mainloop()
