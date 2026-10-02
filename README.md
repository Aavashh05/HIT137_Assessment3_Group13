# HIT137 Assessment 3 - Image Puzzle Game

## Group 13

### Group Members
- Aavash Khatiwada
- Abiud Kiprop
- Dipak Karki

## Project Overview

This project was developed for HIT137 Software Now Assessment 3.

The application is a desktop image puzzle game developed using Python, Tkinter and OpenCV. The player can load an image, select a grid size and restore the scrambled image by swapping, rotating and flipping puzzle tiles.

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

- Load an image from the computer
- Supports JPG, JPEG, PNG and BMP image formats
- Choose between:
  - 3 x 3 grid
  - 4 x 4 grid
  - 5 x 5 grid
- Displays the original image and puzzle image side by side
- Preserves the image aspect ratio when resizing
- Pads the image so it can be divided evenly into tiles
- Randomly applies three types of transformations:
  - Swap
  - Rotate
  - Flip
- Generates all initial transformations before applying them
- Prevents the same tile from participating in more than one initial transformation
- Uses different numbers of transformations depending on the grid size
- Displays faint grid lines over the puzzle
- Highlights the currently selected tile
- Displays a green tick when a tile is in its correct position and orientation
- Tracks the number of player moves
- Displays the number of incorrect tiles
- Provides up to three hints per puzzle
- Includes an instant Solve button
- Detects when the puzzle is completed
- Prevents further puzzle interaction after completion
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
| Swap two tiles | Select one tile and then Left Click another tile |
| Rotate a tile 90 degrees clockwise | Right Click |
| Flip a tile horizontally | Shift + Left Click |
| Display a hint | Hint button |
| Solve the puzzle | Solve button |

## How to Play

1. Start the application.
2. Select a grid size: 3 x 3, 4 x 4 or 5 x 5.
3. Click **Load Image**.
4. Select a JPG, JPEG, PNG or BMP image from the computer.
5. The original image will appear on the left.
6. The transformed puzzle will appear on the right.
7. Use the mouse controls to restore the puzzle.
8. A green tick appears on tiles that are in the correct position and orientation.
9. Use the **Hint** button if assistance is required.
10. Up to three hints can be used for each puzzle.
11. The application notifies the player when the puzzle is completely restored.
12. A new image can then be loaded to start another puzzle.

## Project Structure

### `main.py`

The main entry point of the application.

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
- Move counter
- Incorrect-tile counter
- Completion notifications
- Solve functionality

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
- Puzzle correctness
- Hints
- Puzzle completion
- Puzzle solving

### `README.md`

Contains information about the project, features, controls, installation and usage.

### `github_link.txt`

Contains the public GitHub repository link required for submission.

## Object-Oriented Programming Design

The application uses Object-Oriented Programming to separate different responsibilities.

### `Tile`

Represents an individual puzzle tile.

Each tile stores:

- Its image
- Its original image
- Its correct home position
- Its current orientation

The class also contains methods for rotating, flipping and resetting the tile.

### `Puzzle`

Manages the main puzzle state and gameplay logic.

It manages:

- Puzzle tiles
- Grid size
- Image processing
- Scrambling
- Player moves
- Tile selection
- Hints
- Incorrect tiles
- Puzzle completion
- Solving

### `Transformation`

`Transformation` is the base class used for the different puzzle transformations.

The following classes inherit from it:

- `RotateTransformation`
- `FlipTransformation`
- `SwapTransformation`

Each subclass provides its own implementation of the `apply()` method. This demonstrates inheritance and polymorphism.

The GUI interacts with the `Puzzle` object through its methods, helping separate the interface from the puzzle logic.

## Image Processing

OpenCV is used to:

- Load images
- Resize images
- Preserve aspect ratio
- Pad images to a square size
- Divide images into puzzle tiles
- Rotate tiles
- Flip tiles
- Reassemble the tiles into a complete image

The image size is adjusted so that it can be divided evenly according to the selected grid size.

## Scrambling

Each time an image is loaded, the puzzle automatically generates a new random set of transformations.

The application uses:

- Swap transformations
- Rotation transformations of 90, 180 or 270 degrees
- Horizontal or vertical flip transformations

All transformations are generated before they are applied.

During the initial scrambling process, puzzle tiles are selected so that the same tile does not participate in more than one transformation.

## Moves and Scoring

The application displays:

- Total number of moves
- Number of incorrect tiles

Each player action counts as one move:

- Swap
- Rotate
- Flip

When the puzzle is solved, the number of incorrect tiles becomes zero.

## Hint System

The player can use a maximum of three hints for each puzzle.

A hint:

- Marks an incorrect tile on the puzzle image with a blue circle
- Marks the correct home position of that tile on the original image
- Disappears after the player's next move

After three hints have been used, the Hint button is disabled.

## Solve Function

The **Solve** button restores every tile to its correct:

- Position
- Orientation

The puzzle is then displayed as the completed original image and further puzzle interaction is disabled.

## Error Handling

The application handles common user and input errors, including:

- Cancelling the image-selection dialog
- Selecting an invalid or non-image file
- Invalid grid sizes
- Invalid tile indexes
- Mouse clicks outside the puzzle image
- Player input after puzzle completion

Image-loading errors are displayed using Tkinter message boxes.

## Requirements

The application requires:

- Python 3
- OpenCV
- NumPy
- Tkinter

Install the required external Python packages using:

```bash
pip install opencv-python numpy
