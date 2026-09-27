import cv2


class Tile:
  

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

    def flip_horizontal(self):
        self.image = cv2.flip(self.image, 1)

        a, b, c, d = self.orientation
        self.orientation = (b, a, d, c)

    def flip_vertical(self):
        self.image = cv2.flip(self.image, 0)

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
   

    def __init__(self, grid_size=3):
        self.grid_size = grid_size
        self.tiles = []

        self.moves = 0
        self.hints_used = 0
        self.selected_index = None
        self.completed = False

    def set_tiles(self, tiles):
        self.tiles = tiles
        self.moves = 0
        self.hints_used = 0
        self.selected_index = None
        self.completed = False

    def swap_tiles(self, first_index, second_index):
        self.tiles[first_index], self.tiles[second_index] = (
            self.tiles[second_index],
            self.tiles[first_index]
        )

    def rotate_tile(self, index):
        self.tiles[index].rotate_clockwise()

    def flip_tile(self, index):
        self.tiles[index].flip_horizontal()

    def count_incorrect_tiles(self):
        incorrect = 0

        for index in range(len(self.tiles)):
            if not self.tiles[index].is_correct(index):
                incorrect += 1

        return incorrect

    def is_complete(self):
        return self.count_incorrect_tiles() == 0

    def solve(self):
        self.tiles.sort(key=lambda tile: tile.home_index)

        for tile in self.tiles:
            tile.reset_orientation()

        self.moves = 0
        self.selected_index = None
        self.completed = True
