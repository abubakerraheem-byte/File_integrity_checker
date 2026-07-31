# ==========================================================
# HashGuard Pro v2.2
# Advanced Multiple File Integrity Checker
# Developed By: Abubaker Raheem
# UI Theme Upgrade: Modern Sidebar + Custom Color Palette
# ==========================================================

import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import hashlib
import sqlite3
import os
from datetime import datetime


# ================= COLOR PALETTE =================
# Central place to control the whole theme's look & feel

COLORS = {
    "bg_dark":        "#0F1420",
    "sidebar":        "#141A2B",
    "card":           "#1B2237",
    "card_hover":     "#232C46",
    "accent":         "#5B8CFF",
    "accent_hover":   "#3E6FE0",
    "accent_soft":    "#2A3357",
    "text_main":      "#EAEFFB",
    "text_dim":       "#8A93AC",
    "success":        "#3DDC84",
    "danger":         "#FF5C7A",
    "warning":        "#FFC857",
}

FONT_HEADER  = ("Segoe UI", 30, "bold")
FONT_SUB     = ("Segoe UI", 13)
FONT_NAV     = ("Segoe UI", 14, "bold")
FONT_BODY    = ("Consolas", 12)
FONT_STATUS  = ("Segoe UI", 13, "bold")


# ================= DATABASE =================

db = sqlite3.connect("hashguard.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
hash TEXT,
status TEXT,
date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS monitor(
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT,
path TEXT,
hash TEXT
)
""")

db.commit()


# ================= GLOBAL =================

selected_files = []


# ================= HASH FUNCTION =================

def sha256_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


# ================= SELECT MULTIPLE FILES =================

def browse():
    global selected_files

    files = filedialog.askopenfilenames(title="Select Multiple Files")

    if files:
        selected_files = list(files)

        entry.delete(0, tk.END)
        entry.insert(0, f"{len(selected_files)} file(s) selected")

        msg(f"{len(selected_files)} Files Loaded", COLORS["success"])


# ================= GENERATE HASH =================

def generate():
    if not selected_files:
        msg("Select files first", COLORS["danger"])
        return

    box.delete("1.0", tk.END)

    for path in selected_files:
        try:
            value = sha256_hash(path)
            name = os.path.basename(path)

            cur.execute(
                """
                INSERT INTO history
                (filename,hash,status,date)
                VALUES(?,?,?,?)
                """,
                (name, value, "HASH GENERATED", datetime.now())
            )
            db.commit()

            box.insert(
                tk.END,
                f"""
🔐  FILE INFORMATION
────────────────────────────────────────
 Name   :  {name}
 SHA-256:  {value}
 Time   :  {datetime.now()}
────────────────────────────────────────

"""
            )

        except Exception as e:
            box.insert(tk.END, f"\n⚠️  {name}\nERROR: {e}\n\n")

    msg("All Hashes Generated Successfully", COLORS["success"])


# ================= MONITOR FILES =================

def add_monitor():
    if not selected_files:
        msg("Select files first", COLORS["danger"])
        return

    for path in selected_files:
        name = os.path.basename(path)
        value = sha256_hash(path)

        cur.execute(
            """
            INSERT INTO monitor
            (filename,path,hash)
            VALUES(?,?,?)
            """,
            (name, path, value)
        )

    db.commit()
    msg("Files Added To Monitoring", COLORS["success"])


# ================= CHECK INTEGRITY =================

def check():
    box.delete("1.0", tk.END)

    cur.execute("SELECT * FROM monitor")
    files = cur.fetchall()

    if not files:
        box.insert(tk.END, "No monitored files yet.\nUse 'Add Monitoring' to start tracking files.")
        return

    for f in files:
        try:
            new_hash = sha256_hash(f[2])
            result = "SAFE ✅" if new_hash == f[3] else "MODIFIED ⚠️"

            box.insert(
                tk.END,
                f"""
File   :  {f[1]}
Status :  {result}
────────────────────────────────────────

"""
            )

        except Exception:
            box.insert(tk.END, f"\n{f[1]}\nNOT FOUND ❌\n\n")


# ================= HISTORY =================

def history():
    box.delete("1.0", tk.END)

    cur.execute("SELECT * FROM history")
    rows = cur.fetchall()

    if not rows:
        box.insert(tk.END, "No history yet. Generate a hash to see it recorded here.")
        return

    for r in rows:
        box.insert(
            tk.END,
            f"""
ID     :  {r[0]}
File   :  {r[1]}
Hash   :  {r[2][:50]}...
Status :  {r[3]}
Date   :  {r[4]}
────────────────────────────────────────

"""
        )


# ================= CLEAR =================

def clear():
    box.delete("1.0", tk.END)
    msg("Ready", COLORS["text_dim"])


# ================= THEME =================

def toggle_theme():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")


# ================= MESSAGE =================

def msg(text, color):
    status_label.configure(text=text, text_color=color)


# ================= NAV BUTTON HELPER =================

def make_nav_button(parent, text, command):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=200,
        height=44,
        corner_radius=10,
        fg_color="transparent",
        hover_color=COLORS["card_hover"],
        text_color=COLORS["text_main"],
        font=FONT_NAV,
        anchor="w",
    )


# ================= GUI =================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🔐 HashGuard Pro | File Integrity Security")
app.geometry("1050x680")
app.resizable(False, False)
app.configure(fg_color=COLORS["bg_dark"])

# ---------- Layout: Sidebar + Main content ----------

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# ---------- Sidebar ----------

sidebar = ctk.CTkFrame(app, width=230, corner_radius=0, fg_color=COLORS["sidebar"])
sidebar.grid(row=0, column=0, sticky="nswe")
sidebar.grid_propagate(False)

logo = ctk.CTkLabel(
    sidebar,
    text="🔐 HashGuard",
    font=("Segoe UI", 22, "bold"),
    text_color=COLORS["accent"],
)
logo.pack(pady=(30, 0), padx=20, anchor="w")

logo_sub = ctk.CTkLabel(
    sidebar,
    text="PRO  v2.2",
    font=("Segoe UI", 11),
    text_color=COLORS["text_dim"],
)
logo_sub.pack(pady=(0, 30), padx=20, anchor="w")

nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
nav_frame.pack(fill="x", padx=15)

make_nav_button(nav_frame, "📂  Browse Files", browse).pack(pady=6, fill="x")
make_nav_button(nav_frame, "🔑  Generate Hash", generate).pack(pady=6, fill="x")
make_nav_button(nav_frame, "🛡️  Add Monitoring", add_monitor).pack(pady=6, fill="x")
make_nav_button(nav_frame, "🔍  Check Integrity", check).pack(pady=6, fill="x")
make_nav_button(nav_frame, "🕓  View History", history).pack(pady=6, fill="x")
make_nav_button(nav_frame, "🧹  Clear Output", clear).pack(pady=6, fill="x")

theme_btn = ctk.CTkButton(
    sidebar,
    text="🌗  Toggle Theme",
    command=toggle_theme,
    width=200,
    height=40,
    corner_radius=10,
    fg_color=COLORS["accent_soft"],
    hover_color=COLORS["accent"],
    text_color=COLORS["text_main"],
    font=FONT_NAV,
)
theme_btn.pack(side="bottom", pady=25, padx=15, fill="x")

footer = ctk.CTkLabel(
    sidebar,
    text="Developed by\nAbubaker Raheem",
    font=("Segoe UI", 10),
    text_color=COLORS["text_dim"],
    justify="left",
)
footer.pack(side="bottom", pady=(0, 10), padx=20, anchor="w")

# ---------- Main content area ----------

main = ctk.CTkFrame(app, fg_color=COLORS["bg_dark"])
main.grid(row=0, column=1, sticky="nswe", padx=25, pady=25)
main.grid_columnconfigure(0, weight=1)

header = ctk.CTkLabel(
    main,
    text="File Integrity Dashboard",
    font=FONT_HEADER,
    text_color=COLORS["text_main"],
)
header.grid(row=0, column=0, sticky="w")

sub = ctk.CTkLabel(
    main,
    text="Advanced SHA-256 Multiple File Integrity Monitoring System",
    font=FONT_SUB,
    text_color=COLORS["text_dim"],
)
sub.grid(row=1, column=0, sticky="w", pady=(0, 20))

# ---- File selector card ----

selector_card = ctk.CTkFrame(main, fg_color=COLORS["card"], corner_radius=14)
selector_card.grid(row=2, column=0, sticky="we", pady=(0, 20))
selector_card.grid_columnconfigure(0, weight=1)

entry = ctk.CTkEntry(
    selector_card,
    height=44,
    corner_radius=10,
    fg_color=COLORS["bg_dark"],
    border_color=COLORS["accent_soft"],
    text_color=COLORS["text_main"],
    placeholder_text="No files selected yet...",
)
entry.grid(row=0, column=0, padx=20, pady=20, sticky="we")

browse_btn = ctk.CTkButton(
    selector_card,
    text="📂  Browse Files",
    width=180,
    height=44,
    corner_radius=10,
    fg_color=COLORS["accent"],
    hover_color=COLORS["accent_hover"],
    font=FONT_NAV,
    command=browse,
)
browse_btn.grid(row=0, column=1, padx=(0, 20), pady=20)

# ---- Output card ----

output_card = ctk.CTkFrame(main, fg_color=COLORS["card"], corner_radius=14)
output_card.grid(row=3, column=0, sticky="nswe")
main.grid_rowconfigure(3, weight=1)
output_card.grid_columnconfigure(0, weight=1)
output_card.grid_rowconfigure(1, weight=1)

output_label = ctk.CTkLabel(
    output_card,
    text="OUTPUT LOG",
    font=("Segoe UI", 12, "bold"),
    text_color=COLORS["text_dim"],
)
output_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))

box = ctk.CTkTextbox(
    output_card,
    fg_color=COLORS["bg_dark"],
    text_color=COLORS["text_main"],
    corner_radius=10,
    font=FONT_BODY,
    wrap="word",
)
box.grid(row=1, column=0, sticky="nswe", padx=20, pady=15)

# ---- Status bar ----

status_bar = ctk.CTkFrame(main, fg_color="transparent")
status_bar.grid(row=4, column=0, sticky="we", pady=(15, 0))

status_dot = ctk.CTkLabel(status_bar, text="●", text_color=COLORS["success"], font=("Segoe UI", 16))
status_dot.pack(side="left", padx=(0, 8))

status_label = ctk.CTkLabel(
    status_bar,
    text="Ready",
    font=FONT_STATUS,
    text_color=COLORS["text_dim"],
)
status_label.pack(side="left")


app.mainloop()