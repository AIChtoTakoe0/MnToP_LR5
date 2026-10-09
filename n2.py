import random
import tkinter as tk


COLORS = [
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "cyan",
    "magenta",
    "white",
    "black",
]


def change_color(panel: tk.Frame, label: tk.Label) -> None:
    color = random.choice(COLORS)
    panel.config(bg=color)
    label.config(text=f"Текущий цвет: {color}")


def main():
    root = tk.Tk()
    root.title("Задание 9. Цветная панель")
    root.geometry("420x320")

    panel = tk.Frame(root, bg="lightgray")
    panel.pack(padx=20, pady=20, fill="both", expand=True)

    label = tk.Label(root, text="Текущий цвет: lightgray")
    label.pack(pady=(0, 10))

    button = tk.Button(
        root,
        text="Сменить цвет",
        command=lambda: change_color(panel, label),
    )
    button.pack(pady=(0, 20))

    root.mainloop()


if __name__ == "__main__":
    main()
