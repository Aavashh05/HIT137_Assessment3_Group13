# HIT137 Assessment 3 - Image Puzzle Game

## Group 13

### Group Members
- Aavash Khatiwada
- Abiud Kiprop
- Dipak Karki

## Project Overview

This project was developed for HIT137 Software Now Assessment 3.

The application is a desktop image puzzle game developed using Python, Tkinter and OpenCV. The player loads an image, selects a grid size, and restores the scrambled image by swapping, rotating and flipping puzzle tiles.

The project demonstrates:

- Object-Oriented Programming (OOP)
- Encapsulation
- Inheritance
- Polymorphism
- Tkinter GUI development
- OpenCV image processing
- Event handling
- Error handling

## Features

The application includes the following features:

- Loads images from the user's computer
- Supports JPG, JPEG, PNG and BMP image formats
- Supports 3 x 3, 4 x 4 and 5 x 5 puzzle grids
- Uses 3 x 3 as the default grid size
- Displays the original image and transformed puzzle side by side
- Resizes images to fit the application window
- Preserves image aspect ratio during resizing
- Pads images so they divide evenly into the selected grid
- Randomly applies Swap, Rotate and Flip transformations
- Generates all initial transformations before applying them
- Prevents the same tile from participating in more than one initial transformation
- Scales the number of transformations according to grid size
- Reassembles transformed tiles into a single image for display
- Draws faint grid lines over the transformed image
- Highlights the selected tile
- Displays a green tick when a tile is in its correct position and orientation
- Tracks player moves
- Displays the number of incorrect tiles
- Provides up to three hints per puzzle
- Includes an instant Solve button
- Detects puzzle completion
- Prevents further puzzle input after completion
- Allows the player to load another image and start a new round
- Handles cancelled file selection and invalid image files safely

## Grid Sizes and Transformations

| Grid Size | Number of Tiles | Initial Transformations |
|---|---:|---:|
| 3 x 3 | 9 | 6 |
| 4 x 4 | 16 | 12 |
| 5 x 5 | 25 | 20 |

The transformations are randomly generated each time a new image is loaded.

## Puzzle Controls

| Action | Control |
|---|---|
| Select a tile | Left Click |
| Deselect a selected tile | Left Click the same tile again |
| Swap two tiles | Select one tile, then Left Click another tile |
| Rotate a tile 90 degrees clockwise | Right Click |
| Flip a tile horizontally | Shift + Left Click |
| Display a hint | Hint button |
| Solve the puzzle | Solve button |

## How to Play

1. Start the application.
2. Select a grid size: 3 x 3, 4 x 4 or 5 x 5.
3. Click **Load Image**.
4. Select a JPG, JPEG, PNG or BMP image.
5. The original image appears on the left for reference.
6. The transformed puzzle appears on the right.
7. Use the mouse controls to restore the image.
8. A green tick appears on tiles that are in the correct position and orientation.
9. Use the **Hint** button if assistance is required.
10. Up to three hints can be used for each puzzle.
11. The application notifies the player when the puzzle is completely restored.
12. After completion, load another image to start a new round.

## Project Structure

### `main.py`

The entry point of the application.

It:

- Creates the Tkinter root window
- Creates the `PuzzleApp` object
- Starts the application

### `gui.py`

Contains the `PuzzleApp` class and manages the graphical user interface.

It is responsible for:

- Creating Tkinter widgets
- Displaying the original and puzzle images
- Grid-size selection
- Image loading
- Mouse interaction
- Tile selection highlighting
- Grid-line overlays
- Green tick overlays
- Hint display
- Move and incorrect-tile counters
- Completion notifications
- Solve functionality
- User-facing error messages

### `puzzle.py`

Contains the puzzle logic and image-processing classes.

The main classes are:

- `Tile`
- `Puzzle`
- `Transformation`
- `RotateTransformation`
- `FlipTransformation`
- `SwapTransformation`

The file manages:

- Image loading
- Image resizing and padding
- Tile creation
- Tile position and orientation
- Puzzle scrambling
- Transformations
- Player moves
- Tile selection
- Puzzle correctness
- Hints
- Puzzle completion
- Puzzle solving

### `README.md`

Contains project information, features, controls, requirements and instructions for running the application.

### `github_link.txt`

Contains the public GitHub repository link required for submission.

## Object-Oriented Programming Design

The application uses Object-Oriented Programming to separate responsibilities between the graphical interface, puzzle state, tiles and transformations.

### `Tile`

Represents an individual puzzle tile.

Each tile stores:

- Its current image
- Its original image
- Its correct home position
- Its current orientation

The class includes methods for rotating, flipping, resetting and checking the tile.

### `Puzzle`

Manages the main puzzle state and gameplay logic.

It manages:

- Grid size
- Puzzle tiles
- Image processing
- Scrambling
- Player moves
- Tile selection
- Hints
- Incorrect tiles
- Puzzle completion
- Solving

### `Transformation`

`Transformation` is the base class for the puzzle transformations.

The following classes inherit from it:

- `RotateTransformation`
- `FlipTransformation`
- `SwapTransformation`

Each subclass provides its own implementation of the `apply()` method, demonstrating inheritance and polymorphism.

## Image Processing

OpenCV is used to:

- Load images
- Resize images
- Preserve aspect ratio
- Pad images to a square size
- Divide images into puzzle tiles
- Rotate tiles
- Flip tiles
- Reassemble tiles into a complete image

The processed image size is adjusted so that it divides evenly according to the selected grid size.

## Scrambling

Each time an image is loaded, the puzzle generates a new random set of transformations.

The application uses:

- Swap transformations
- Rotation transformations of 90, 180 or 270 degrees
- Horizontal or vertical flip transformations

All transformations are generated before they are applied.

During initial scrambling, participating tiles are selected so that the same tile is not used more than once.

## Moves and Incorrect Tiles

The interface displays:

- Total number of moves
- Number of incorrect tiles

Each player action counts as one move:

- Swap
- Rotate
- Flip

When all tiles are in their correct positions and orientations, the puzzle is complete.

## Hint System

The player can use a maximum of three hints for each puzzle.

A hint:

- Marks one currently incorrect tile on the transformed image with a blue circle
- Marks that tile's correct home position on the original image with a blue circle
- Disappears after the player's next move

After three hints have been used, the Hint button is disabled.

## Solve Function

The **Solve** button restores every tile to its correct:

- Position
- Orientation

It also clears the move count and restores the image to its completed state. Further puzzle interaction is disabled until a new image is loaded.

## Error Handling

The application handles common user and input errors, including:

- Cancelling the image-selection dialog
- Selecting an invalid or non-image file
- Invalid grid sizes in the puzzle model
- Invalid tile indexes
- Mouse clicks outside the puzzle image
- Player input after puzzle completion

Invalid image errors are shown using Tkinter message boxes, and the application remains open.

## Requirements

The application requires:

- Python 3
- OpenCV
- NumPy
- Tkinter

Install the required external Python packages using:

```bash
pip install opencv-python numpy
```

Tkinter is normally included with standard Python installations.

## Running the Application

Open a terminal or command prompt in the project folder and run:

```bash
python main.py
```

The Image Puzzle Game window will open.

## GitHub Repository

The public GitHub repository link is stored in:

`github_link.txt`

