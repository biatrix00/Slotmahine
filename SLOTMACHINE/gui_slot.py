
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

ROWS = 3
COLS = 3
MAX_LINES = 3
MIN_BET = 1
MAX_BET = 10000000000000000

symbol_count = {
    "🍒": 2,
    "💎": 4,
    "🍋": 6,
    "🔔": 8
}

symbol_values = {
    "🍒": 10,
    "💎": 8,
    "🍋": 5,
    "🔔": 3
}

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def format_slots(columns):
    rows = len(columns[0])
    formatted = ""
    formatted += "┌─────┬─────┬─────┐\n"
    for row in range(rows):
        row_symbols = [f" {column[row]} " for column in columns]
        formatted += "│" + "│".join(row_symbols) + "│\n"
        if row < rows - 1:
            formatted += "├─────┼─────┼─────┤\n"
    formatted += "└─────┴─────┴─────┘\n"
    return formatted

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Vegas Slot Machine")
        self.balance = 0
        self.root.configure(bg="#0a0a23")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", foreground="#fff", background="#e60073", padding=8, font=("Helvetica", 10, "bold"))
        style.configure("TLabel", foreground="#fff", background="#0a0a23", font=("Helvetica", 10))
        style.configure("TEntry", padding=4)

        ttk.Label(root, text="Deposit:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.deposit_entry = ttk.Entry(root)
        self.deposit_entry.grid(row=0, column=1)
        ttk.Button(root, text="Deposit", command=self.deposit).grid(row=0, column=2)

        ttk.Label(root, text="Bet per Line:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.bet_entry = ttk.Entry(root)
        self.bet_entry.grid(row=1, column=1)

        ttk.Label(root, text=f"Lines (1-{MAX_LINES}):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lines_entry = ttk.Entry(root)
        self.lines_entry.grid(row=2, column=1)

        self.spin_button = ttk.Button(root, text="🎲 Spin the Reels!", command=self.spin)
        self.spin_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.output_text = tk.Text(root, height=10, width=40, state='disabled', bg="#1c1c3c", fg="#00ffcc", font=("Courier", 14, "bold"))
        self.output_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.output_text.tag_configure("center", justify='center')

        self.balance_label = ttk.Label(root, text="Balance: $0")
        self.balance_label.grid(row=5, column=0, columnspan=3)

    def deposit(self):
        amount = self.deposit_entry.get()
        if amount.isdigit():
            self.balance += int(amount)
            self.update_balance()
            self.deposit_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def spin(self):
        try:
            bet = int(self.bet_entry.get())
            lines = int(self.lines_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Bet and lines must be numbers.")
            return

        if not (MIN_BET <= bet <= MAX_BET):
            messagebox.showerror("Invalid Bet", f"Bet must be between {MIN_BET} and {MAX_BET}.")
            return
        if not (1 <= lines <= MAX_LINES):
            messagebox.showerror("Invalid Lines", f"Lines must be between 1 and {MAX_LINES}.")
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showerror("Insufficient Funds", "You don't have enough balance.")
            return

        self.balance -= total_bet
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Spinning the reels...\n", "center")
        self.output_text.config(state='disabled')
        self.root.after(1000, lambda: self.finish_spin(lines, bet))

    def finish_spin(self, lines, bet):
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
        self.balance += winnings

        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, format_slots(slots), "center")
        self.output_text.insert(tk.END, f"\n💰 You won ${winnings} on lines: {', '.join(map(str, winning_lines)) or 'None'}\n", "center")
        self.output_text.config(state='disabled')
        self.update_balance()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

if __name__ == '__main__':
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
