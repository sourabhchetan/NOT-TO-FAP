
import json
import datetime
import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

DATA_FILE = "streak_data.json"
QUOTES = [
    "Discipline is choosing what you want most over what you want now.",
    "You don't grow when you're comfortable.",
    "The pain of regret is worse than the pain of discipline.",
    "Energy saved is energy redirected. Use it wisely.",
    "Every day without fapping is a step closer to power."
]

# Load or initialize
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"streak": 0, "last_entry": "", "log": []}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Update streak
def update_streak(fapped):
    today = str(datetime.date.today())
    if data["last_entry"] == today:
        messagebox.showinfo("Info", "You've already logged today.")
        return

    if not fapped:
        data["streak"] += 1
    else:
        data["streak"] = 0

    data["last_entry"] = today
    data["log"].append({"date": today, "fapped": fapped})
    save_data(data)
    update_labels()

# Update GUI labels
def update_labels():
    streak_label.config(text=f"🔥 Current Streak: {data['streak']} days")
    quote_label.config(text=f"🧠 Motivation: {random_quote()}")

# Get random quote
def random_quote():
    import random
    return random.choice(QUOTES)

# Plot streak history
def show_graph():
    dates = [entry["date"] for entry in data["log"]]
    streaks = []
    streak_count = 0

    for entry in data["log"]:
        if not entry["fapped"]:
            streak_count += 1
        else:
            streak_count = 0
        streaks.append(streak_count)

    if not dates:
        messagebox.showinfo("Graph", "No data to plot.")
        return

    plt.figure(figsize=(8, 4))
    plt.plot(dates, streaks, marker='o', linestyle='-')
    plt.xticks(rotation=45)
    plt.title("No-Fap Streak Progress")
    plt.xlabel("Date")
    plt.ylabel("Streak")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# --- GUI ---
data = load_data()

root = tk.Tk()
root.title("NOT TO FAP TRACKER")
root.geometry("400x300")
root.resizable(False, False)

streak_label = tk.Label(root, text="", font=("Helvetica", 16), fg="green")
streak_label.pack(pady=10)

quote_label = tk.Label(root, text="", wraplength=350, font=("Arial", 10))
quote_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=15)

btn_yes = tk.Button(frame, text="YES 😓 (I fapped)", width=15, command=lambda: update_streak(True))
btn_no = tk.Button(frame, text="NO 💪 (I resisted)", width=15, command=lambda: update_streak(False))

btn_yes.grid(row=0, column=0, padx=5)
btn_no.grid(row=0, column=1, padx=5)

graph_btn = tk.Button(root, text="📊 Show Progress Graph", command=show_graph)
graph_btn.pack(pady=10)

update_labels()
root.mainloop()
