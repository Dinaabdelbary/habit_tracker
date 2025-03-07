# Habit Tracker

## Overview
The **Habit Tracker** is a Python-based application that helps users track their habits and maintain streaks. It uses an SQLite database to store habit information and allows users to interact with it via a command-line interface (CLI). Additionally, unit tests are included to ensure the correct functionality of habit tracking features.

## Features
- Add new habits with a **daily** or **weekly** periodicity.
- Display all habits or filter them by periodicity.
- Check habits to update streaks and longest streaks.
- Delete habits when no longer needed.
- Maintain a log of habit checks.
- Automated unit tests for key functionality.

## Project Structure
```
habit_tracker/
│── habit_tracker_db.py    # Handles all database operations (CRUD functions)
│── habit_tracker_cli.py   # Command-line interface for user interaction
│── test_habit_tracker.py  # Unit tests for the habit tracker
│── README.md              # Documentation for the project
```

## Installation & Setup
### Prerequisites
Ensure you have Python (3.x recommended) installed on your system.

### Clone the Repository
```bash
git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker
```

### Install Dependencies
This project requires SQLite, which comes pre-installed with Python. No additional dependencies are required.

## Usage
### Running the Habit Tracker
```bash
python habit_tracker_cli.py
```

### Command Line Options
1. **Display habits** – View all recorded habits.
2. **Add a habit** – Create a new habit (daily or weekly).
3. **Edit a habit** – Check or delete a habit.
4. **View daily habits** – Filter and display daily habits.
5. **View weekly habits** – Filter and display weekly habits.
6. **Exit** – Quit the application.

### Running Unit Tests
```bash
python -m unittest test_habit_tracker.py
```

## Example Usage
```
1. Display list
2. Add habit
3. Edit habit
4. Display daily habits
5. Display weekly habits
6. Exit
Enter your choice: 2
Enter habit name: Exercise
Enter periodicity (daily/weekly): daily
Habit added successfully!
```
