import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "records.db"


class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
            """
        )
        self.conn.commit()

    def add(self, name: str, phone: str, email: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO records (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email),
        )
        self.conn.commit()
        return cur.lastrowid

    def update(self, record_id: int, name: str, phone: str, email: str) -> None:
        self.conn.execute(
            "UPDATE records SET name = ?, phone = ?, email = ? WHERE id = ?",
            (name, phone, email, record_id),
        )
        self.conn.commit()

    def delete(self, record_id: int) -> None:
        self.conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
        self.conn.commit()

    def all(self):
        cur = self.conn.execute(
            "SELECT id, name, phone, email FROM records ORDER BY id"
        )
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Задание 7. GUI для работы с SQLite")
        self.root.geometry("720x480")

        self.db = Database(DB_NAME)
        self.selected_id = None

        self._build_ui()
        self.refresh()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self) -> None:
        form = ttk.Frame(self.root, padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Телефон:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.phone_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.phone_var, width=30).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(form, text="Email:").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var, width=30).grid(
            row=2, column=1, padx=5, pady=5
        )

        buttons = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        buttons.pack(fill="x")

        ttk.Button(buttons, text="Добавить", command=self.add).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Обновить", command=self.update).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Удалить", command=self.delete).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Очистить", command=self.clear_form).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Обновить список", command=self.refresh).pack(
            side="left", padx=5
        )

        columns = ("id", "name", "phone", "email")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col, text in zip(columns, ("ID", "Имя", "Телефон", "Email")):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=100 if col != "email" else 180)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def add(self) -> None:
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Имя обязательно")
            return

        self.db.add(name, self.phone_var.get().strip(), self.email_var.get().strip())
        self.refresh()
        self.clear_form()

    def update(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Внимание", "Выберите запись")
            return

        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Имя обязательно")
            return

        self.db.update(
            self.selected_id,
            name,
            self.phone_var.get().strip(),
            self.email_var.get().strip(),
        )
        self.refresh()

    def delete(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Внимание", "Выберите запись")
            return

        if not messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            return

        self.db.delete(self.selected_id)
        self.refresh()
        self.clear_form()

    def clear_form(self) -> None:
        self.selected_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in self.db.all():
            self.tree.insert("", "end", values=row)

    def on_select(self, event) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])
        self.name_var.set(values[1])
        self.phone_var.set(values[2])
        self.email_var.set(values[3])

    def on_close(self) -> None:
        self.db.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
