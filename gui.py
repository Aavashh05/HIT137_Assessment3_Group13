import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import base64
import cv2

from puzzle import Puzzle


class PuzzleApp:
    """Tkinter interface for the image puzzle game."""

    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 Image Puzzle Game")

        self.puzzle = None

        self.original_photo = None
        self.puzzle_photo = None

        self.grid_size_var = tk.StringVar(
            value="3 x 3"
        )

        self.moves_var = tk.StringVar(
            value="Moves: 0"
        )

        self.incorrect_var = tk.StringVar(
            value="Incorrect Tiles: 0"
        )

        self.hints_var = tk.StringVar(
            value="Hints Used: 0 / 3"
        )

        self.create_widgets()

    def create_widgets(self):
        """Create the main GUI widgets."""

        title_label = tk.Label(
            self.root,
            text="Image Puzzle Game",
            font=("Arial", 20, "bold")
        )

        title_label.pack(
            pady=10
        )

        control_frame = tk.Frame(
            self.root
        )

        control_frame.pack(
            pady=5
        )

        grid_label = tk.Label(
            control_frame,
            text="Grid Size:"
        )

        grid_label.grid(
            row=0,
            column=0,
            padx=5
        )

        self.grid_selector = ttk.Combobox(
            control_frame,
            textvariable=self.grid_size_var,
            values=[
                "3 x 3",
                "4 x 4",
                "5 x 5"
            ],
            state="readonly",
            width=8
        )

        self.grid_selector.grid(
            row=0,
            column=1,
            padx=5
        )

        self.load_button = tk.Button(
            control_frame,
            text="Load Image",
            command=self.load_image
        )

        self.load_button.grid(
            row=0,
            column=2,
            padx=10
        )

        self.hint_button = tk.Button(
            control_frame,
            text="Hint",
            command=self.show_hint,
            state=tk.DISABLED
        )

        self.hint_button.grid(
            row=0,
            column=3,
            padx=5
        )

        self.solve_button = tk.Button(
            control_frame,
            text="Solve",
            command=self.solve_puzzle,
            state=tk.DISABLED
        )

        self.solve_button.grid(
            row=0,
            column=4,
            padx=5
        )

        image_frame = tk.Frame(
            self.root
        )

        image_frame.pack(
            padx=10,
            pady=10
        )

        original_frame = tk.Frame(
            image_frame
        )

        original_frame.grid(
            row=0,
            column=0,
            padx=10
        )

        puzzle_frame = tk.Frame(
            image_frame
        )

        puzzle_frame.grid(
            row=0,
            column=1,
            padx=10
        )

        original_label = tk.Label(
            original_frame,
            text="Original Image",
            font=("Arial", 12, "bold")
        )

        original_label.pack(
            pady=5
        )

        puzzle_label = tk.Label(
            puzzle_frame,
            text="Puzzle Image",
            font=("Arial", 12, "bold")
        )

        puzzle_label.pack(
            pady=5
        )

        self.original_canvas = tk.Canvas(
            original_frame,
            width=450,
            height=450,
            background="lightgray"
        )

        self.original_canvas.pack()

        self.puzzle_canvas = tk.Canvas(
            puzzle_frame,
            width=450,
            height=450,
            background="lightgray"
        )

        self.puzzle_canvas.pack()

        self.puzzle_canvas.bind(
            "<Button-1>",
            self.handle_left_click
        )

        self.puzzle_canvas.bind(
            "<Button-3>",
            self.handle_right_click
        )

        information_frame = tk.Frame(
            self.root
        )

        information_frame.pack(
            pady=10
        )

        moves_label = tk.Label(
            information_frame,
            textvariable=self.moves_var,
            font=("Arial", 12)
        )

        moves_label.grid(
            row=0,
            column=0,
            padx=20
        )

        incorrect_label = tk.Label(
            information_frame,
            textvariable=self.incorrect_var,
            font=("Arial", 12)
        )

        incorrect_label.grid(
            row=0,
            column=1,
            padx=20
        )

        hints_label = tk.Label(
            information_frame,
            textvariable=self.hints_var,
            font=("Arial", 12)
        )

        hints_label.grid(
            row=0,
            column=2,
            padx=20
        )

        instruction_label = tk.Label(
            self.root,
            text=(
                "Left Click: Select / Swap     "
                "Right Click: Rotate     "
                "Shift + Left Click: Flip"
            )
        )

        instruction_label.pack(
            pady=(0, 10)
        )

    def get_selected_grid_size(self):
        """Return the selected grid size."""

        value = self.grid_size_var.get()

        if value == "3 x 3":
            return 3

        if value == "4 x 4":
            return 4

        return 5

    def load_image(self):
        """Load an image selected by the user."""

        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp"
                ),
                (
                    "JPEG Files",
                    "*.jpg *.jpeg"
                ),
                (
                    "PNG Files",
                    "*.png"
                ),
                (
                    "BMP Files",
                    "*.bmp"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if file_path == "":
            return

        grid_size = (
            self.get_selected_grid_size()
        )

        try:
            new_puzzle = Puzzle(
                grid_size
            )

            new_puzzle.load_image(
                file_path,
                max_size=450
            )

        except ValueError as error:
            messagebox.showerror(
                "Image Error",
                str(error)
            )
            return

        except Exception:
            messagebox.showerror(
                "Error",
                "The image could not be loaded."
            )
            return

        self.puzzle = new_puzzle

        self.hint_button.config(
            state=tk.NORMAL
        )

        self.solve_button.config(
            state=tk.NORMAL
        )

        self.display_images()
        self.update_information()

    def cv_image_to_photo(self, image):
        """Convert an OpenCV image into a Tkinter image."""

        success, encoded_image = cv2.imencode(
            ".png",
            image
        )

        if not success:
            raise ValueError(
                "The image could not be displayed."
            )

        image_data = base64.b64encode(
            encoded_image.tobytes()
        )

        return tk.PhotoImage(
            data=image_data
        )

    def display_images(self):
        """Display the original and puzzle images."""

        if self.puzzle is None:
            return

        original_image = (
            self.puzzle.processed_image
        )

        puzzle_image = (
            self.puzzle.reassemble_image()
        )

        try:
            self.original_photo = (
                self.cv_image_to_photo(
                    original_image
                )
            )

            self.puzzle_photo = (
                self.cv_image_to_photo(
                    puzzle_image
                )
            )

        except ValueError as error:
            messagebox.showerror(
                "Display Error",
                str(error)
            )
            return

        image_size = (
            self.puzzle.processed_image.shape[0]
        )

        self.original_canvas.config(
            width=image_size,
            height=image_size
        )

        self.puzzle_canvas.config(
            width=image_size,
            height=image_size
        )

        self.original_canvas.delete(
            "all"
        )

        self.puzzle_canvas.delete(
            "all"
        )

        self.original_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.original_photo
        )

        self.puzzle_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.puzzle_photo
        )

        self.draw_overlays()

    def draw_overlays(self):
        """Draw grid lines, ticks, selection and hints."""

        if self.puzzle is None:
            return

        image_size = (
            self.puzzle.processed_image.shape[0]
        )

        tile_size = (
            image_size
            // self.puzzle.grid_size
        )

        for number in range(
            1,
            self.puzzle.grid_size
        ):
            position = (
                number * tile_size
            )

            self.puzzle_canvas.create_line(
                position,
                0,
                position,
                image_size,
                fill="gray",
                width=1
            )

            self.puzzle_canvas.create_line(
                0,
                position,
                image_size,
                position,
                fill="gray",
                width=1
            )

        for index in range(
            len(self.puzzle.tiles)
        ):
            tile = self.puzzle.tiles[
                index
            ]

            if tile.is_correct(index):

                row = (
                    index
                    // self.puzzle.grid_size
                )

                column = (
                    index
                    % self.puzzle.grid_size
                )

                x = (
                    column * tile_size
                    + tile_size
                    - 22
                )

                y = (
                    row * tile_size
                    + 12
                )

                self.puzzle_canvas.create_line(
                    x,
                    y + 7,
                    x + 6,
                    y + 13,
                    fill="green",
                    width=3
                )

                self.puzzle_canvas.create_line(
                    x + 6,
                    y + 13,
                    x + 16,
                    y,
                    fill="green",
                    width=3
                )

        selected_index = (
            self.puzzle.get_selected_index()
        )

        if selected_index is not None:

            row = (
                selected_index
                // self.puzzle.grid_size
            )

            column = (
                selected_index
                % self.puzzle.grid_size
            )

            x1 = (
                column * tile_size
            )

            y1 = (
                row * tile_size
            )

            x2 = (
                x1 + tile_size
            )

            y2 = (
                y1 + tile_size
            )

            self.puzzle_canvas.create_rectangle(
                x1 + 2,
                y1 + 2,
                x2 - 2,
                y2 - 2,
                outline="orange",
                width=4
            )

        if self.puzzle.active_hint is not None:

            current_index, home_index = (
                self.puzzle.active_hint
            )

            self.draw_hint_circle(
                self.puzzle_canvas,
                current_index,
                tile_size
            )

            self.draw_hint_circle(
                self.original_canvas,
                home_index,
                tile_size
            )

    def draw_hint_circle(
        self,
        canvas,
        index,
        tile_size
    ):
        """Draw a blue hint circle."""

        row = (
            index
            // self.puzzle.grid_size
        )

        column = (
            index
            % self.puzzle.grid_size
        )

        centre_x = (
            column * tile_size
            + tile_size // 2
        )

        centre_y = (
            row * tile_size
            + tile_size // 2
        )

        radius = max(
            12,
            tile_size // 8
        )

        canvas.create_oval(
            centre_x - radius,
            centre_y - radius,
            centre_x + radius,
            centre_y + radius,
            outline="blue",
            width=4
        )

    def get_tile_index(
        self,
        x,
        y
    ):
        """Convert mouse coordinates into a tile index."""

        if self.puzzle is None:
            return None

        image_size = (
            self.puzzle.processed_image.shape[0]
        )

        if (
            x < 0
            or y < 0
            or x >= image_size
            or y >= image_size
        ):
            return None

        tile_size = (
            image_size
            // self.puzzle.grid_size
        )

        column = (
            x // tile_size
        )

        row = (
            y // tile_size
        )

        index = (
            row
            * self.puzzle.grid_size
            + column
        )

        if not self.puzzle.valid_index(
            index
        ):
            return None

        return index

    def handle_left_click(
        self,
        event
    ):
        """Select, deselect, swap or flip puzzle tiles."""

        if self.puzzle is None:
            return

        if self.puzzle.completed:
            return

        index = self.get_tile_index(
            event.x,
            event.y
        )

        if index is None:
            return

        shift_pressed = (
            event.state & 0x0001
        )

        if shift_pressed:

            self.puzzle.player_flip(
                index
            )

            self.after_player_action()
            return

        selected_index = (
            self.puzzle.get_selected_index()
        )

        if selected_index is None:

            self.puzzle.select_tile(
                index
            )

            self.display_images()
            return

        if selected_index == index:

            self.puzzle.clear_selection()

            self.display_images()
            return

        self.puzzle.player_swap(
            selected_index,
            index
        )

        self.after_player_action()

    def handle_right_click(
        self,
        event
    ):
        """Rotate a tile 90 degrees clockwise."""

        if self.puzzle is None:
            return

        if self.puzzle.completed:
            return

        index = self.get_tile_index(
            event.x,
            event.y
        )

        if index is None:
            return

        self.puzzle.player_rotate(
            index
        )

        self.after_player_action()

    def after_player_action(self):
        """Refresh the GUI after a player move."""

        self.display_images()
        self.update_information()

        if self.puzzle.completed:

            self.hint_button.config(
                state=tk.DISABLED
            )

            self.solve_button.config(
                state=tk.DISABLED
            )

            messagebox.showinfo(
                "Puzzle Complete",
                (
                    "Congratulations! "
                    "You restored the image."
                )
            )

    def update_information(self):
        """Update moves, incorrect tiles and hint information."""

        if self.puzzle is None:

            self.moves_var.set(
                "Moves: 0"
            )

            self.incorrect_var.set(
                "Incorrect Tiles: 0"
            )

            self.hints_var.set(
                "Hints Used: 0 / 3"
            )

            return

        self.moves_var.set(
            "Moves: "
            + str(
                self.puzzle.moves
            )
        )

        self.incorrect_var.set(
            "Incorrect Tiles: "
            + str(
                self.puzzle.count_incorrect_tiles()
            )
        )

        self.hints_var.set(
            "Hints Used: "
            + str(
                self.puzzle.hints_used
            )
            + " / 3"
        )

        if self.puzzle.can_use_hint():

            self.hint_button.config(
                state=tk.NORMAL
            )

        else:

            self.hint_button.config(
                state=tk.DISABLED
            )

    def show_hint(self):
        """Display one puzzle hint."""

        if self.puzzle is None:
            return

        hint = self.puzzle.get_hint()

        if hint is None:

            self.hint_button.config(
                state=tk.DISABLED
            )

            return

        self.display_images()
        self.update_information()

    def solve_puzzle(self):
        """Instantly solve the current puzzle."""

        if self.puzzle is None:
            return

        solved = self.puzzle.solve()

        if not solved:
            return

        self.display_images()
        self.update_information()

        self.hint_button.config(
            state=tk.DISABLED
        )

        self.solve_button.config(
            state=tk.DISABLED
        )

        messagebox.showinfo(
            "Puzzle Solved",
            "The puzzle has been solved."
        )

    def run(self):
        """Start the Tkinter event loop."""

        self.root.mainloop()
