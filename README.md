Overview

This project is a simple habit tracker application built using Python and SQLite. It allows users to create, track, and manage their habits, with features like adding new habits, checking off habits, and viewing habits by their periodicity (daily or weekly). The application also tracks streaks and the longest streak for each habit, providing users with insights into their consistency.

Features
Add Habits: Users can add new habits with a name and periodicity (daily or weekly).

Check Habits: Users can check off habits, which updates the streak and longest streak.

Edit/Delete Habits: Users can edit or delete existing habits.

View Habits: Users can view all habits or filter them by periodicity (daily or weekly).

Streak Tracking: The application tracks the current streak and the longest streak for each habit.

Habit Checks: Each time a habit is checked, the date is recorded in the database.

Database Schema
The application uses an SQLite database with two tables:

habits:

id: Primary key.

name: Name of the habit.

periodicity: Periodicity of the habit (daily or weekly).

streak: Current streak of the habit.

longest_streak: Longest streak achieved for the habit.

last_checked: Date the habit was last checked.

habit_checks:

id: Primary key.

habit_id: Foreign key referencing the habit.

date_checked: Date the habit was checked.

How to Use
Run the Application:

Execute the script habit_tracker.py to start the application.

The application will prompt you with a menu of options.

Menu Options:

1. Display list: Shows all habits.

2. Add habit: Allows you to add a new habit.

3. Edit habit: Allows you to edit or delete an existing habit.

4. Display daily habits: Shows all habits with a daily periodicity.

5. Display weekly habits: Shows all habits with a weekly periodicity.

6. Exit: Exits the application.

Adding a Habit:

When prompted, enter the name of the habit and its periodicity (daily or weekly).

Checking a Habit:

Use the "Edit habit" option to check off a habit. This will update the streak and longest streak.

Deleting a Habit:

Use the "Edit habit" option to delete a habit.

Testing
The application includes unit tests to ensure the functionality works as expected. The tests cover:

Adding a habit.

Checking a habit.

Resetting the streak when a habit is broken.

Updating the longest streak.

Displaying habits by periodicity.

Deleting a habit.

To run the tests, execute the script with the following command:

bash
Copy
python habit_tracker.py
The tests will run automatically and display the results in the console.

Dependencies
Python 3.x

SQLite3 (included with Python standard library)

