# To-Do List CLI Application (v2 in Progress 🚧)

A simple command-line To-Do List manager in Python supporting multiple lists, task priorities, and CSV import/export. Currently on v1, with v2 in progress.
Features (v1)

Create and manage multiple to-do lists
Add, remove, and view tasks with title, description, and priority (1-5)
Save and load lists as CSV files
Interactive menu-driven interface

Upcoming (v2)

Multi-list management (open/edit multiple lists simultaneously)
a UI using tkinter library

Requirements

Python 3.6+
Install via: pip install -r requirements.txt (create with csv if needed)

Usage

Run: python main.py
Menu Options:
1: Create a new to-do list
2: Open an existing to-do list
3: Add a task to the open list
4: Remove a task from the open list
5: Delete a to-do list
6: View tasks in a list
7: Save a list to a CSV file
8: Load a list from a CSV file
0: Exit



File Structure

main.py — Main CLI interface
todolist.py — todolist and task classes

Notes

v1 limitation: Only one list open at a time for edits.
CSV files save to the current directory.

Getting Started
Clone this repo, install requirements, and run main.py. Example output:  
To-Do List: Work
------------------------------
Task 1:
Title: Meeting
Description: Team sync
Priority: 3
------------------------------

About
First project by Hossein Garossian. v2 in development—suggestions appreciated!
