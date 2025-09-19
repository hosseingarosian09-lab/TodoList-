# To-Do List CLI Application

A simple command-line To-Do List manager in Python that supports multiple lists, task priorities, and CSV import/export.

## Features

- Create and manage multiple to-do lists
- Add, remove, and view tasks with title, description, and priority (1-5)
- Save and load lists as CSV files
- Lists and tasks are managed interactively via a menu

## Usage

1. **Run the application:**
   ```sh
   python main.py
   ```

2. **Menu Options:**
   - `1`: Create a new to-do list
   - `2`: Open an existing to-do list
   - `3`: Add a task to the open list
   - `4`: Remove a task from the open list
   - `5`: Delete a to-do list
   - `6`: View tasks in a list
   - `7`: Save a list to a CSV file
   - `8`: Load a list from a CSV file
   - `0`: Exit the application

## File Structure

- `main.py` — Main CLI interface for the to-do list manager
- `todolist.py` — Contains the `todolist` and `task` classes for managing lists and tasks

## Requirements

- Python 3.x

## Notes

- Only one list can be open at a time for adding/removing tasks.
- CSV files are saved in the current directory.