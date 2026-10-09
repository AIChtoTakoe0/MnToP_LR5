import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Задание 7. Меню File → Exit")
    root.geometry("360x220")

    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menubar)

    label = tk.Label(root, text="Выберите File → Exit для выхода")
    label.pack(expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
