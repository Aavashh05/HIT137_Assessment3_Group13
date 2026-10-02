import tkinter as tk

from gui import PuzzleApp


def main():
    root = tk.Tk()

    app = PuzzleApp(
        root
    )

    app.run()


if __name__ == "__main__":
    main()
