import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records 
             (id INTEGER PRIMARY KEY, date TEXT, bmi REAL)''')
conn.commit()

# BMI Calculation
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError("Values must be positive.")
        
        bmi = weight / (height ** 2)
        category = classify_bmi(bmi)
        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
        
        save_bmi(bmi)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# BMI Classification
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Save BMI to Database
def save_bmi(bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_records (date, bmi) VALUES (?, ?)", (date, bmi))
    conn.commit()
    messagebox.showinfo("Saved", "BMI record saved.")

# Show BMI History
def show_history():
    c.execute("SELECT date, bmi FROM bmi_records")
    records = c.fetchall()
    history_text.delete(1.0, tk.END)
    for date, bmi in records:
        history_text.insert(tk.END, f"{date}: BMI = {bmi:.2f}\n")

# Plot BMI Trend
def plot_bmi():
    c.execute("SELECT date, bmi FROM bmi_records")
    records = c.fetchall()
    dates = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in records]
    bmis = [record[1] for record in records]
    if dates and bmis:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o', color='b')
        plt.title("BMI Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.grid()
        plt.show()
    else:
        messagebox.showinfo("No Data", "No BMI data to display.")

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")

# Labels and Inputs
tk.Label(root, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Height (m):").grid(row=1, column=0, padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=5)

# Result Label
result_label = tk.Label(root, text="BMI: \nCategory:", font=("Arial", 14))
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Buttons
tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="Show History", command=show_history).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Plot BMI Trend", command=plot_bmi).grid(row=5, column=0, columnspan=2, pady=5)

# History Display
history_text = tk.Text(root, height=10, width=40)
history_text.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()

# Close database connection on exit
root.protocol("WM_DELETE_WINDOW", lambda: [conn.close(), root.destroy()])
