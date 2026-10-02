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

        # -------------------------------------------------
        # Colours
        # -------------------------------------------------

        self.background_color = "#EEF3F8"
        self.panel_color = "#FFFFFF"

        self.hero_color = "#17324D"
        self.hero_title_color = "#FFFFFF"
        self.hero_subtitle_color = "#D8E6F3"

        self.title_color = "#17324D"
        self.text_color = "#263238"
        self.soft_text_color = "#667788"

        self.load_color = "#2D6CDF"
        self.load_active_color = "#2458B8"

        self.hint_color = "#F4C95D"
        self.hint_active_color = "#E5B645"
        self.hint_text_color = "#2B2B2B"

        self.solve_color = "#25855A"
        self.solve_active_color = "#1D6947"

        self.image_border_color = "#4A78A8"
        self.canvas_color = "#DDE3EA"

        self.guide_border_color = "#A9BDD0"
        self.guide_box_color = "#F7FAFD"

        self.root.configure(
            background=self.background_color
        )

        # -------------------------------------------------
        # Window size
        # -------------------------------------------------

        screen_width = (
            self.root.winfo_screenwidth()
        )

        screen_height = (
            self.root.winfo_screenheight()
        )

        normal_width = min(
            1250,
            screen_width - 80
        )

        normal_height = min(
            900,
            screen_height - 80
        )

        self.root.geometry(
            str(normal_width)
            + "x"
            + str(normal_height)
        )

        self.root.minsize(
            normal_width,
            normal_height
        )

        # Start maximized on Windows.
        try:
            self.root.state(
                "zoomed"
            )
        except tk.TclError:
            pass

        # -------------------------------------------------
        # Image display size
        #
        # Calculated using the normal window size so the
        # whole interface still fits after restoring the
        # window from maximized mode.
        # -------------------------------------------------

        width_limit = (
            normal_width - 180
        ) // 2

        height_limit = (
            normal_height - 470
        )

        self.display_size = min(
            400,
            width_limit,
            height_limit
        )

        if self.display_size < 240:
            self.display_size = 240

        # -------------------------------------------------
        # Puzzle data
        # -------------------------------------------------

        self.puzzle = None

        self.original_photo = None
        self.puzzle_photo = None

        self.grid_size_var = tk.StringVar(
            value="3 x 3"
        )

        self.moves_var = tk.StringVar(
            value="0"
        )

        self.incorrect_var = tk.StringVar(
            value="0"
        )

        self.hints_var = tk.StringVar(
            value="0 / 3"
        )

        self.create_widgets()

    def create_widgets(self):
        """Create the main GUI widgets."""

        # =================================================
        # HERO SECTION
        # =================================================

        hero_frame = tk.Frame(
            self.root,
            background=self.hero_color,
            padx=20,
            pady=16
        )

        hero_frame.pack(
            fill=tk.X
        )

        title_label = tk.Label(
            hero_frame,
            text="PICTURE PUZZLE",
            font=(
                "Arial",
                25,
                "bold"
            ),
            foreground=self.hero_title_color,
            background=self.hero_color
        )

        title_label.pack()

        subtitle_label = tk.Label(
            hero_frame,
            text=(
                "Rebuild the original picture by "
                "swapping, rotating and flipping the tiles."
            ),
            font=(
                "Arial",
                11
            ),
            foreground=self.hero_subtitle_color,
            background=self.hero_color
        )

        subtitle_label.pack(
            pady=(5, 2)
        )

        small_hero_label = tk.Label(
            hero_frame,
            text=(
                "Choose a grid size, load an image, "
                "then restore every tile to its correct position."
            ),
            font=(
                "Arial",
                9
            ),
            foreground="#B9CCDD",
            background=self.hero_color
        )

        small_hero_label.pack()

        # =================================================
        # CONTROL SECTION
        # =================================================

        control_outer = tk.Frame(
            self.root,
            background="#C4D2E0",
            padx=1,
            pady=1
        )

        control_outer.pack(
            pady=(10, 7)
        )

        control_frame = tk.Frame(
            control_outer,
            background=self.panel_color,
            padx=18,
            pady=9
        )

        control_frame.pack()

        grid_label = tk.Label(
            control_frame,
            text="Grid Size:",
            font=(
                "Arial",
                10,
                "bold"
            ),
            foreground=self.text_color,
            background=self.panel_color
        )

        grid_label.grid(
            row=0,
            column=0,
            padx=(0, 7)
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
            padx=(0, 15)
        )

        self.load_button = tk.Button(
            control_frame,
            text="Load Image",
            command=self.load_image,
            font=(
                "Arial",
                10,
                "bold"
            ),
            background=self.load_color,
            foreground="white",
            activebackground=self.load_active_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=16,
            pady=7,
            cursor="hand2"
        )

        self.load_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.hint_button = tk.Button(
            control_frame,
            text="Hint",
            command=self.show_hint,
            state=tk.DISABLED,
            font=(
                "Arial",
                10,
                "bold"
            ),
            background=self.hint_color,
            foreground=self.hint_text_color,
            activebackground=self.hint_active_color,
            activeforeground=self.hint_text_color,
            disabledforeground="#777777",
            relief=tk.FLAT,
            padx=20,
            pady=7,
            cursor="hand2"
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
            state=tk.DISABLED,
            font=(
                "Arial",
                10,
                "bold"
            ),
            background=self.solve_color,
            foreground="white",
            activebackground=self.solve_active_color,
            activeforeground="white",
            disabledforeground="#777777",
            relief=tk.FLAT,
            padx=20,
            pady=7,
            cursor="hand2"
        )

        self.solve_button.grid(
            row=0,
            column=4,
            padx=5
        )

        # =================================================
        # INFORMATION SECTION
        # =================================================

        information_frame = tk.Frame(
            self.root,
            background=self.background_color
        )

        information_frame.pack(
            pady=(2, 8)
        )

        self.create_info_box(
            information_frame,
            "MOVES",
            self.moves_var,
            0
        )

        self.create_info_box(
            information_frame,
            "INCORRECT TILES",
            self.incorrect_var,
            1
        )

        self.create_info_box(
            information_frame,
            "HINTS USED",
            self.hints_var,
            2
        )

        # =================================================
        # IMAGE SECTION
        # =================================================

        image_frame = tk.Frame(
            self.root,
            background=self.background_color
        )

        image_frame.pack(
            padx=20,
            pady=(0, 8)
        )

        # -------------------------------------------------
        # Original image section
        # -------------------------------------------------

        original_border = tk.Frame(
            image_frame,
            background=self.image_border_color,
            padx=2,
            pady=2
        )

        original_border.grid(
            row=0,
            column=0,
            padx=10
        )

        original_frame = tk.Frame(
            original_border,
            background=self.panel_color,
            padx=9,
            pady=8
        )

        original_frame.pack()

        original_label = tk.Label(
            original_frame,
            text="ORIGINAL / Reference",
            font=(
                "Arial",
                12,
                "bold"
            ),
            foreground=self.title_color,
            background=self.panel_color
        )

        original_label.pack(
            pady=(0, 3)
        )

        original_description = tk.Label(
            original_frame,
            text="Use this image as your guide",
            font=(
                "Arial",
                8
            ),
            foreground=self.soft_text_color,
            background=self.panel_color
        )

        original_description.pack(
            pady=(0, 6)
        )

        self.original_canvas = tk.Canvas(
            original_frame,
            width=self.display_size,
            height=self.display_size,
            background=self.canvas_color,
            highlightthickness=0
        )

        self.original_canvas.pack()

        # -------------------------------------------------
        # Puzzle image section
        # -------------------------------------------------

        puzzle_border = tk.Frame(
            image_frame,
            background=self.image_border_color,
            padx=2,
            pady=2
        )

        puzzle_border.grid(
            row=0,
            column=1,
            padx=10
        )

        puzzle_frame = tk.Frame(
            puzzle_border,
            background=self.panel_color,
            padx=9,
            pady=8
        )

        puzzle_frame.pack()

        puzzle_label = tk.Label(
            puzzle_frame,
            text="YOUR PUZZLE / Play Here",
            font=(
                "Arial",
                12,
                "bold"
            ),
            foreground=self.title_color,
            background=self.panel_color
        )

        puzzle_label.pack(
            pady=(0, 3)
        )

        puzzle_description = tk.Label(
            puzzle_frame,
            text="Interact with the tiles on this side",
            font=(
                "Arial",
                8
            ),
            foreground=self.soft_text_color,
            background=self.panel_color
        )

        puzzle_description.pack(
            pady=(0, 6)
        )

        self.puzzle_canvas = tk.Canvas(
            puzzle_frame,
            width=self.display_size,
            height=self.display_size,
            background=self.canvas_color,
            highlightthickness=0
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

        # =================================================
        # HOW TO PLAY SECTION
        # =================================================

        guide_outer = tk.Frame(
            self.root,
            background=self.guide_border_color,
            padx=1,
            pady=1
        )

        guide_outer.pack(
            pady=(2, 12)
        )

        guide_frame = tk.Frame(
            guide_outer,
            background=self.panel_color,
            padx=16,
            pady=8
        )

        guide_frame.pack()

        guide_title = tk.Label(
            guide_frame,
            text="HOW TO PLAY",
            font=(
                "Arial",
                10,
                "bold"
            ),
            foreground=self.title_color,
            background=self.panel_color
        )

        guide_title.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=(0, 7)
        )

        self.create_guide_box(
            guide_frame,
            "LEFT CLICK",
            "Select / Swap",
            0
        )

        self.create_guide_box(
            guide_frame,
            "RIGHT CLICK",
            "Rotate 90°",
            1
        )

        self.create_guide_box(
            guide_frame,
            "SHIFT + LEFT CLICK",
            "Flip Horizontally",
            2
        )

        legend_label = tk.Label(
            guide_frame,
            text=(
                "✓ Green tick = correct position and orientation"
                "     "
                "● Blue circles = hint tile and home position"
            ),
            font=(
                "Arial",
                9
            ),
            foreground=self.soft_text_color,
            background=self.panel_color
        )

        legend_label.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=(8, 0)
        )

    def create_info_box(
        self,
        parent,
        heading,
        variable,
        column
    ):
        """Create an information card."""

        outer = tk.Frame(
            parent,
            background="#B8C9D9",
            padx=1,
            pady=1
        )

        outer.grid(
            row=0,
            column=column,
            padx=8
        )

        box = tk.Frame(
            outer,
            background=self.panel_color,
            width=180,
            height=60
        )

        box.pack()

        box.pack_propagate(
            False
        )

        heading_label = tk.Label(
            box,
            text=heading,
            font=(
                "Arial",
                8,
                "bold"
            ),
            foreground=self.soft_text_color,
            background=self.panel_color
        )

        heading_label.pack(
            pady=(7, 1)
        )

        value_label = tk.Label(
            box,
            textvariable=variable,
            font=(
                "Arial",
                15,
                "bold"
            ),
            foreground=self.title_color,
            background=self.panel_color
        )

        value_label.pack()

    def create_guide_box(
        self,
        parent,
        heading,
        description,
        column
    ):
        """Create one control guide box."""

        box = tk.Frame(
            parent,
            background=self.guide_box_color,
            width=210,
            height=48
        )

        box.grid(
            row=1,
            column=column,
            padx=5
        )

        box.grid_propagate(
            False
        )

        heading_label = tk.Label(
            box,
            text=heading,
            font=(
                "Arial",
                8,
                "bold"
            ),
            foreground=self.title_color,
            background=self.guide_box_color
        )

        heading_label.pack(
            pady=(6, 0)
        )

        description_label = tk.Label(
            box,
            text=description,
            font=(
                "Arial",
                9
            ),
            foreground=self.text_color,
            background=self.guide_box_color
        )

        description_label.pack()

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
                max_size=self.display_size
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

    def cv_image_to_photo(
        self,
        image
    ):
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

        # Grid lines
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

        # Green ticks
        for index in range(
            len(self.puzzle.tiles)
        ):
            tile = (
                self.puzzle.tiles[
                    index
                ]
            )

            if tile.is_correct(
                index
            ):
                row = (
                    index
                    // self.puzzle.grid_size
                )

                column = (
                    index
                    % self.puzzle.grid_size
                )

                x = (
                    column
                    * tile_size
                    + tile_size
                    - 22
                )

                y = (
                    row
                    * tile_size
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

        # Selected tile border
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

        # Hint circles
        if (
            self.puzzle.active_hint
            is not None
        ):
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
            column
            * tile_size
            + tile_size // 2
        )

        centre_y = (
            row
            * tile_size
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
        """Update moves, incorrect tiles and hints."""

        if self.puzzle is None:
            self.moves_var.set(
                "0"
            )

            self.incorrect_var.set(
                "0"
            )

            self.hints_var.set(
                "0 / 3"
            )

            return

        self.moves_var.set(
            str(
                self.puzzle.moves
            )
        )

        self.incorrect_var.set(
            str(
                self.puzzle.count_incorrect_tiles()
            )
        )

        self.hints_var.set(
            str(
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
