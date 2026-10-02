# HIT137 Assessment 3 - Image Puzzle Game

## Group 13

### Group Members
- Aavash Khatiwada
- Abiud

## Project Overview

This project is a desktop image puzzle game developed for HIT137 Software Now Assessment 3.

The application demonstrates:

- Object-Oriented Programming (OOP)
- Tkinter GUI development
- OpenCV image processing
- Image transformations
- Event handling
- Error handling

The user can load an image, choose a puzzle grid size, and restore the scrambled image by swapping, rotating, and flipping tiles.

## Features

- Supports JPG, JPEG, PNG and BMP images
- Grid sizes:
  - 3 x 3
  - 4 x 4
  - 5 x 5
- Displays the original image and puzzle side by side
- Randomly applies:
  - Swap transformations
  - Rotation transformations
  - Flip transformations
- Prevents the same tile from being used more than once during initial scrambling
- Displays green ticks for correctly positioned and oriented tiles
- Tracks:
  - Number of moves
  - Number of incorrect tiles
- Provides up to three hints
- Includes an instant Solve option
- Detects puzzle completion
- Prevents further puzzle interaction after completion
- Handles invalid image files and cancelled file selection safely

## Puzzle Controls

| Action | Control |
|---|---|
| Select a tile | Left Click |
| Deselect a tile | Left Click the selected tile again |
| Swap two tiles | Select one tile, then Left Click another tile |
| Rotate tile 90 degrees clockwise | Right Click |
| Flip tile horizontally | Shift + Left Click |
| Hint | Hint button |
| Solve puzzle | Solve button |

## Grid Sizes

The image is divided according to the selected grid size:

- 3 x 3 = 9 tiles
- 4 x 4 = 16 tiles
- 5 x 5 = 25 tiles

The number of initial transformations also increases with grid size:

- 3 x 3 = 6 transformations
- 4 x 4 = 12 transformations
- 5 x 5 = 20 transformations

## Project Files

### main.py
The entry point of the application.

It creates the Tkinter window and starts the puzzle application.

### gui.py
Contains the `PuzzleApp` class.

It manages:

- Tkinter widgets
- Image display
- Mouse events
- Puzzle controls
- Hints
- Green tick overlays
- Move and incorrect-tile counters
- Completion messages

### puzzle.py
Contains the main puzzle logic and OOP classes.

Main classes include:

- `Tile`
- `Puzzle`
- `Transformation`
- `RotateTransformation`
- `FlipTransformation`
- `SwapTransformation`

The transformation subclasses demonstrate inheritance and polymorphism.

### test_puzzle.py
Contains tests for:

- Tile orientation
- Puzzle operations
- Image processing
- Grid sizes
- Image formats
- Invalid inputs
- Scrambling
- Transformation uniqueness
- Player actions
- Selection
- Hints
- Puzzle completion

## Requirements

The program requires Python 3 and the following Python packages:

```text
opencv-python
numpy
