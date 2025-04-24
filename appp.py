import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect("issues.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            timestamp TEXT,
            status TEXT DEFAULT "Open"
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Submit issue function
def submit_issue():
    title = title_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()
    location = location_entry.get()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not title or not description or not location:
        messagebox.showerror("Error", "All fields are required.")
        return

    conn = sqlite3.connect("issues.db")
    c = conn.cursor()
    c.execute("INSERT INTO issues (title, description, location, timestamp) VALUES (?, ?, ?, ?)",
              (title, description, location, timestamp))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Issue submitted!")

    title_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)
    location_entry.delete(0, tk.END)

# Show issues with filter
def show_issues(status_filter=None):
    issues_window = tk.Toplevel(root)
    issues_window.title("Reported Issues")

    conn = sqlite3.connect("issues.db")
    c = conn.cursor()
    if status_filter:
        c.execute("SELECT * FROM issues WHERE status=?", (status_filter,))
    else:
        c.execute("SELECT * FROM issues")
    issues = c.fetchall()
    conn.close()

    if not issues:
        tk.Label(issues_window, text="No issues found.").pack()
        return

    for issue in issues:
        id_, title, desc, loc, time, status = issue
        issue_text = f"[{status}] {title} ({loc})\nReported: {time}\n{desc}\n"
        label = tk.Label(issues_window, text=issue_text, justify="left", wraplength=400)
        label.pack(anchor="w", padx=10, pady=5)

        if status == "Open":
            resolve_btn = tk.Button(issues_window, text="Mark as Resolved",
                                    command=lambda i=id_: resolve_issue(i, issues_window))
            resolve_btn.pack(anchor="w", padx=10)

def resolve_issue(issue_id, window):
    conn = sqlite3.connect("issues.db")
    c = conn.cursor()
    c.execute("UPDATE issues SET status='Resolved' WHERE id=?", (issue_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", "Issue marked as resolved.")
    window.destroy()
    show_issues("Open")

# GUI Setup
root = tk.Tk()
root.title("Environment Issue Reporter")
root.geometry("500x700")
root.configure(bg="#f8f9fa")  # Light background

# Configure layout
root.grid_columnconfigure(0, weight=1)

# Title
tk.Label(root, text="🟢 Report Environment Issue", font=("Arial", 16, "bold"), bg="#f8f9fa").grid(row=0, column=0, pady=(20, 10))

# Issue Title
tk.Label(root, text="Issue Title", bg="#f8f9fa").grid(row=1, column=0, sticky="w", padx=40)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=2, column=0, padx=40, pady=5)

# Description
tk.Label(root, text="Description", bg="#f8f9fa").grid(row=3, column=0, sticky="w", padx=40)
desc_entry = tk.Text(root, height=5, width=50)
desc_entry.grid(row=4, column=0, padx=40, pady=5)

# Location
tk.Label(root, text="Location", bg="#f8f9fa").grid(row=5, column=0, sticky="w", padx=40)
location_entry = tk.Entry(root, width=50)
location_entry.grid(row=6, column=0, padx=40, pady=5)

# Submit Button
submit_btn = tk.Button(root, text="Submit Issue", command=submit_issue, bg="#28a745", fg="white", width=20)
submit_btn.grid(row=7, column=0, pady=15)

# View Section
tk.Label(root, text="📋 View Reported Issues", font=("Arial", 13, "bold"), bg="#f8f9fa").grid(row=8, column=0, pady=(30, 5))

# View Buttons
view_all_btn = tk.Button(root, text="View All Issues", command=lambda: show_issues(None), width=20)
view_all_btn.grid(row=9, column=0, pady=2)

view_open_btn = tk.Button(root, text="View Open Issues", command=lambda: show_issues("Open"), width=20)
view_open_btn.grid(row=10, column=0, pady=2)

view_resolved_btn = tk.Button(root, text="View Resolved Issues", command=lambda: show_issues("Resolved"), width=20)
view_resolved_btn.grid(row=11, column=0, pady=2)

root.mainloop()
