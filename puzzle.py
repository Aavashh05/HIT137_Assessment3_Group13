import cv2
import numpy as np
import random


class Tile:
    """Represents one tile of the puzzle."""

    def __init__(self, image, home_index):
        self.original_image = image.copy()
        self.image = image.copy()
        self.home_index = home_index
        self.orientation = (0, 1, 2, 3)

    def rotate_clockwise(self):
        self.image = cv2.rotate(
            self.image,
            cv2.ROTATE_90_CLOCKWISE
        )

        a, b, c, d = self.orientation
        self.orientation = (d, a, b, c)

    def rotate(self, angle):
        if angle == 90:
            self.rotate_clockwise()

        elif angle == 180:
            self.rotate_clockwise()
            self.rotate_clockwise()

        elif angle == 270:
            self.rotate_clockwise()
            self.rotate_clockwise()
            self.rotate_clockwise()

        else:
            raise ValueError(
                "Rotation angle must be 90, 180 or 270."
            )

    def flip_horizontal(self):
        self.image = cv2.flip(
            self.image,
            1
        )

        a, b, c, d = self.orientation
        self.orientation = (b, a, d, c)

    def flip_vertical(self):
        self.image = cv2.flip(
            self.image,
            0
        )

        a, b, c, d = self.orientation
        self.orientation = (d, c, b, a)

    def reset_orientation(self):
        self.image = self.original_image.copy()
        self.orientation = (0, 1, 2, 3)

    def is_correct(self, current_index):
        return (
            self.home_index == current_index
            and self.orientation == (0, 1, 2, 3)
        )


class Puzzle:
    """Stores and manages the state of the image puzzle."""

    def __init__(self, grid_size=3):
        if grid_size not in (3, 4, 5):
            raise ValueError(
                "Grid size must be 3, 4 or 5."
            )

        self.grid_size = grid_size
        self.tiles = []

        self.original_image = None
        self.processed_image = None

        self.moves = 0
        self.hints_used = 0
        self.active_hint = None
        self.selected_index = None
        self.completed = False

        self.scramble_history = []

    def set_tiles(self, tiles):
        self.tiles = tiles

        self.moves = 0
        self.hints_used = 0
        self.active_hint = None
        self.selected_index = None
        self.completed = False

        self.scramble_history = []

    def load_image(
        self,
        image_path,
        max_size=600
    ):
        image = cv2.imread(
            image_path
        )

        if image is None:
            raise ValueError(
                "The selected file is not a valid image."
            )

        self.original_image = image.copy()

        height, width = image.shape[:2]

        final_size = (
            max_size
            - (max_size % self.grid_size)
        )

        scale = min(
            final_size / width,
            final_size / height
        )

        new_width = max(
            1,
            int(width * scale)
        )

        new_height = max(
            1,
            int(height * scale)
        )

        resized_image = cv2.resize(
            image,
            (
                new_width,
                new_height
            )
        )

        square_image = np.zeros(
            (
                final_size,
                final_size,
                3
            ),
            dtype=np.uint8
        )

        x_start = (
            final_size - new_width
        ) // 2

        y_start = (
            final_size - new_height
        ) // 2

        square_image[
            y_start:y_start + new_height,
            x_start:x_start + new_width
        ] = resized_image

        self.processed_image = square_image

        self.create_tiles()
        self.scramble()

    def create_tiles(self):
        if self.processed_image is None:
            raise ValueError(
                "No image has been loaded."
            )

        tiles = []

        image_size = (
            self.processed_image.shape[0]
        )

        tile_size = (
            image_size
            // self.grid_size
        )

        home_index = 0

        for row in range(
            self.grid_size
        ):
            for column in range(
                self.grid_size
            ):

                y1 = row * tile_size
                y2 = y1 + tile_size

                x1 = column * tile_size
                x2 = x1 + tile_size

                tile_image = (
                    self.processed_image[
                        y1:y2,
                        x1:x2
                    ].copy()
                )

                tile = Tile(
                    tile_image,
                    home_index
                )

                tiles.append(
                    tile
                )

                home_index += 1

        self.set_tiles(
            tiles
        )

    def get_scramble_count(self):
        if self.grid_size == 3:
            return 6

        if self.grid_size == 4:
            return 12

        return 20

    def scramble(self):
        """Scramble the puzzle without reusing any participating tile."""

        if len(self.tiles) == 0:
            raise ValueError(
                "No puzzle tiles are available."
            )

        transformation_count = (
            self.get_scramble_count()
        )

        while True:

            # Start from the solved puzzle.
            self.tiles.sort(
                key=lambda tile:
                tile.home_index
            )

            for tile in self.tiles:
                tile.reset_orientation()

            total_tiles = len(
                self.tiles
            )

            # Each swap uses one additional unique tile.
            max_swaps = (
                total_tiles
                - transformation_count
            )

            swap_count = random.randint(
                1,
                max_swaps
            )

            remaining_count = (
                transformation_count
                - swap_count
            )

            # Keep at least one Rotate and one Flip.
            rotate_count = random.randint(
                1,
                remaining_count - 1
            )

            flip_count = (
                remaining_count
                - rotate_count
            )

            transformation_types = (
                ["swap"] * swap_count
                + ["rotate"] * rotate_count
                + ["flip"] * flip_count
            )

            random.shuffle(
                transformation_types
            )

            # Swap requires two unique tiles.
            tiles_needed = (
                transformation_count
                + swap_count
            )

            available_home_indices = (
                random.sample(
                    [
                        tile.home_index
                        for tile in self.tiles
                    ],
                    tiles_needed
                )
            )

            transformations = []

            tile_position = 0

            for transformation_type in (
                transformation_types
            ):

                if transformation_type == "swap":

                    target_home_index = (
                        available_home_indices[
                            tile_position
                        ]
                    )

                    partner_home_index = (
                        available_home_indices[
                            tile_position + 1
                        ]
                    )

                    tile_position += 2

                    transformation = (
                        SwapTransformation(
                            target_home_index,
                            partner_home_index
                        )
                    )

                elif transformation_type == "rotate":

                    target_home_index = (
                        available_home_indices[
                            tile_position
                        ]
                    )

                    tile_position += 1

                    angle = random.choice(
                        [
                            90,
                            180,
                            270
                        ]
                    )

                    transformation = (
                        RotateTransformation(
                            target_home_index,
                            angle
                        )
                    )

                else:

                    target_home_index = (
                        available_home_indices[
                            tile_position
                        ]
                    )

                    tile_position += 1

                    direction = random.choice(
                        [
                            "horizontal",
                            "vertical"
                        ]
                    )

                    transformation = (
                        FlipTransformation(
                            target_home_index,
                            direction
                        )
                    )

                transformations.append(
                    transformation
                )

            # All transformations are generated
            # before any are applied.
            self.scramble_history = (
                transformations
            )

            for transformation in (
                transformations
            ):
                transformation.apply(
                    self
                )

            if not self.is_complete():
                break

        self.moves = 0
        self.hints_used = 0
        self.active_hint = None
        self.selected_index = None
        self.completed = False

    def find_tile_index(
        self,
        home_index
    ):
        """Find a tile's current position using its home index."""

        for index in range(
            len(self.tiles)
        ):
            if (
                self.tiles[index].home_index
                == home_index
            ):
                return index

        return None

    def valid_index(
        self,
        index
    ):
        return (
            isinstance(index, int)
            and 0 <= index < len(self.tiles)
        )

    def swap_tiles(
        self,
        first_index,
        second_index
    ):
        if not self.valid_index(
            first_index
        ):
            raise ValueError(
                "Invalid first tile index."
            )

        if not self.valid_index(
            second_index
        ):
            raise ValueError(
                "Invalid second tile index."
            )

        self.tiles[
            first_index
        ], self.tiles[
            second_index
        ] = (
            self.tiles[second_index],
            self.tiles[first_index]
        )

    def rotate_tile(
        self,
        index
    ):
        if not self.valid_index(
            index
        ):
            raise ValueError(
                "Invalid tile index."
            )

        self.tiles[
            index
        ].rotate_clockwise()

    def flip_tile(
        self,
        index
    ):
        if not self.valid_index(
            index
        ):
            raise ValueError(
                "Invalid tile index."
            )

        self.tiles[
            index
        ].flip_horizontal()

    def finish_player_move(self):
        self.moves += 1
        self.active_hint = None
        self.selected_index = None

        if self.is_complete():
            self.completed = True

    def player_swap(
        self,
        first_index,
        second_index
    ):
        if self.completed:
            return False

        if first_index == second_index:
            return False

        self.swap_tiles(
            first_index,
            second_index
        )

        self.finish_player_move()

        return True

    def player_rotate(
        self,
        index
    ):
        if self.completed:
            return False

        self.rotate_tile(
            index
        )

        self.finish_player_move()

        return True

    def player_flip(
        self,
        index
    ):
        if self.completed:
            return False

        self.flip_tile(
            index
        )

        self.finish_player_move()

        return True

    def select_tile(
        self,
        index
    ):
        """Select a puzzle tile."""

        if not self.valid_index(
            index
        ):
            return False

        if self.completed:
            return False

        self.selected_index = index

        return True

    def clear_selection(self):
        """Clear the selected puzzle tile."""

        self.selected_index = None

    def get_selected_index(self):
        """Return the selected tile index."""

        return self.selected_index

    def get_incorrect_indices(self):
        """Return the positions of all incorrect tiles."""

        incorrect_indices = []

        for index in range(
            len(self.tiles)
        ):
            if not self.tiles[
                index
            ].is_correct(
                index
            ):
                incorrect_indices.append(
                    index
                )

        return incorrect_indices

    def can_use_hint(self):
        """Check whether another hint can be used."""

        return (
            len(self.tiles) > 0
            and not self.completed
            and self.hints_used < 3
            and len(
                self.get_incorrect_indices()
            ) > 0
        )

    def get_hint(self):
        """Choose an incorrect tile and return its current and home positions."""

        if not self.can_use_hint():
            return None

        incorrect_indices = (
            self.get_incorrect_indices()
        )

        current_index = random.choice(
            incorrect_indices
        )

        home_index = (
            self.tiles[
                current_index
            ].home_index
        )

        self.active_hint = (
            current_index,
            home_index
        )

        self.hints_used += 1

        return self.active_hint

    def count_incorrect_tiles(self):
        incorrect = 0

        for index in range(
            len(self.tiles)
        ):
            if not self.tiles[
                index
            ].is_correct(
                index
            ):
                incorrect += 1

        return incorrect

    def is_complete(self):
        if len(self.tiles) == 0:
            return False

        return (
            self.count_incorrect_tiles()
            == 0
        )

    def reassemble_image(self):
        if len(self.tiles) == 0:
            raise ValueError(
                "No puzzle tiles are available."
            )

        tile_height, tile_width = (
            self.tiles[0].image.shape[:2]
        )

        result = np.zeros(
            (
                tile_height
                * self.grid_size,

                tile_width
                * self.grid_size,

                3
            ),
            dtype=np.uint8
        )

        index = 0

        for row in range(
            self.grid_size
        ):
            for column in range(
                self.grid_size
            ):

                y1 = (
                    row * tile_height
                )

                y2 = (
                    y1 + tile_height
                )

                x1 = (
                    column * tile_width
                )

                x2 = (
                    x1 + tile_width
                )

                result[
                    y1:y2,
                    x1:x2
                ] = (
                    self.tiles[
                        index
                    ].image
                )

                index += 1

        return result

    def solve(self):
        if len(self.tiles) == 0:
            return False

        self.tiles.sort(
            key=lambda tile:
            tile.home_index
        )

        for tile in self.tiles:
            tile.reset_orientation()

        self.moves = 0
        self.active_hint = None
        self.selected_index = None
        self.completed = True
        self.scramble_history = []

        return True


class Transformation:
    """Base class for puzzle transformations."""

    def __init__(
        self,
        target_home_index
    ):
        self.target_home_index = (
            target_home_index
        )

    def apply(
        self,
        puzzle
    ):
        raise NotImplementedError(
            "Subclasses must implement apply()."
        )


class RotateTransformation(
    Transformation
):
    """Rotates one puzzle tile."""

    def __init__(
        self,
        target_home_index,
        angle
    ):
        super().__init__(
            target_home_index
        )

        self.angle = angle

    def apply(
        self,
        puzzle
    ):
        current_index = (
            puzzle.find_tile_index(
                self.target_home_index
            )
        )

        puzzle.tiles[
            current_index
        ].rotate(
            self.angle
        )


class FlipTransformation(
    Transformation
):
    """Flips one puzzle tile."""

    def __init__(
        self,
        target_home_index,
        direction
    ):
        super().__init__(
            target_home_index
        )

        self.direction = direction

    def apply(
        self,
        puzzle
    ):
        current_index = (
            puzzle.find_tile_index(
                self.target_home_index
            )
        )

        if self.direction == "horizontal":

            puzzle.tiles[
                current_index
            ].flip_horizontal()

        elif self.direction == "vertical":

            puzzle.tiles[
                current_index
            ].flip_vertical()

        else:
            raise ValueError(
                "Flip direction must be horizontal or vertical."
            )


class SwapTransformation(
    Transformation
):
    """Swaps two puzzle tiles."""

    def __init__(
        self,
        target_home_index,
        partner_home_index
    ):
        super().__init__(
            target_home_index
        )

        self.partner_home_index = (
            partner_home_index
        )

    def apply(
        self,
        puzzle
    ):
        target_index = (
            puzzle.find_tile_index(
                self.target_home_index
            )
        )

        partner_index = (
            puzzle.find_tile_index(
                self.partner_home_index
            )
        )

        puzzle.swap_tiles(
            target_index,
            partner_index
        )
