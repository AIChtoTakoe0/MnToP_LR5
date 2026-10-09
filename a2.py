import math
import time
import tkinter as tk
from tkinter import ttk, messagebox


def format_stopwatch(seconds: float) -> str:
    total_hundredths = int(seconds * 100)
    hundredths = total_hundredths % 100
    total_seconds = total_hundredths // 100
    seconds_part = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d}.{hundredths:02d}"


def format_timer(seconds: float) -> str:
    total = max(0, math.ceil(seconds))
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


class StopwatchTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)

        self.elapsed = 0.0
        self.running = False
        self.start_monotonic = 0.0
        self.after_id = None

        self.label = ttk.Label(self, text="00:00:00.00", font=("TkDefaultFont", 24))
        self.label.pack(pady=20)

        buttons = ttk.Frame(self)
        buttons.pack()

        ttk.Button(buttons, text="Старт", command=self.start).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Стоп", command=self.stop).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Сброс", command=self.reset).pack(
            side="left", padx=5
        )

    def start(self) -> None:
        if self.running:
            return

        self.running = True
        self.start_monotonic = time.monotonic()
        self._tick()

    def stop(self) -> None:
        if not self.running:
            return

        self.elapsed += time.monotonic() - self.start_monotonic
        self.running = False

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.label.config(text=format_stopwatch(self.elapsed))

    def reset(self) -> None:
        self.running = False

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.elapsed = 0.0
        self.label.config(text=format_stopwatch(0.0))

    def _tick(self) -> None:
        if not self.running:
            return

        current = self.elapsed + (time.monotonic() - self.start_monotonic)
        self.label.config(text=format_stopwatch(current))
        self.after_id = self.after(50, self._tick)


class TimerTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)

        self.remaining = 0.0
        self.running = False
        self.last_tick = 0.0
        self.after_id = None

        self.label = ttk.Label(self, text="00:00", font=("TkDefaultFont", 24))
        self.label.pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Минуты:").grid(row=0, column=0, padx=5)
        self.min_var = tk.StringVar(value="1")
        ttk.Entry(form, textvariable=self.min_var, width=5).grid(
            row=0, column=1, padx=5
        )

        ttk.Label(form, text="Секунды:").grid(row=0, column=2, padx=5)
        self.sec_var = tk.StringVar(value="0")
        ttk.Entry(form, textvariable=self.sec_var, width=5).grid(
            row=0, column=3, padx=5
        )

        buttons = ttk.Frame(self)
        buttons.pack(pady=10)

        ttk.Button(buttons, text="Старт", command=self.start).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Пауза", command=self.pause).pack(
            side="left", padx=5
        )
        ttk.Button(buttons, text="Сброс", command=self.reset).pack(
            side="left", padx=5
        )

    def _read_input(self):
        try:
            minutes = int(self.min_var.get())
            seconds = int(self.sec_var.get())
            if minutes < 0 or seconds < 0:
                raise ValueError
            return minutes * 60 + seconds
        except ValueError:
            messagebox.showerror("Ошибка", "Введите неотрицательные целые числа")
            return None

    def start(self) -> None:
        if self.running:
            return

        if self.remaining <= 0:
            total = self._read_input()
            if total is None:
                return
            if total <= 0:
                messagebox.showwarning("Внимание", "Время должно быть больше нуля")
                return
            self.remaining = float(total)

        self.running = True
        self.last_tick = time.monotonic()
        self._tick()

    def pause(self) -> None:
        if not self.running:
            return

        self.running = False

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.label.config(text=format_timer(self.remaining))

    def reset(self) -> None:
        self.running = False

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.remaining = 0.0
        self.label.config(text="00:00")

    def _tick(self) -> None:
        if not self.running:
            return

        now = time.monotonic()
        self.remaining -= now - self.last_tick
        self.last_tick = now

        if self.remaining <= 0:
            self.remaining = 0.0
            self.running = False
            self.label.config(text="00:00")
            messagebox.showinfo("Таймер", "Время вышло!")
            return

        self.label.config(text=format_timer(self.remaining))
        self.after_id = self.after(100, self._tick)


def main():
    root = tk.Tk()
    root.title("Задание 5. Таймер/секундомер")
    root.geometry("420x320")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    notebook.add(StopwatchTab(notebook), text="Секундомер")
    notebook.add(TimerTab(notebook), text="Таймер")

    root.mainloop()


if __name__ == "__main__":
    main()
