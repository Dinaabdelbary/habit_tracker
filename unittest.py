from habit_tracker.DB import HabitTrackerDB
from datetime import datetime, timedelta
import unittest


class TestHabitTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up an in-memory database for testing."""
        cls.db = HabitTrackerDB(":memory:")

    @classmethod
    def tearDownClass(cls):
        """Close database connection after tests."""
        cls.db.close_connection()

    def setUp(self):
        """Clear data before each test."""
        self.db.c.execute("DELETE FROM habits")
        self.db.c.execute("DELETE FROM habit_checks")
        self.db.conn.commit()

    def test_add_habit(self):
        """Test adding a habit."""
        self.db.add_habit("Test Habit", "daily")
        habits = self.db.display_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0][1], "Test Habit")

    def test_check_habit(self):
        """Test checking a habit updates streaks correctly."""
        self.db.add_habit("Test Habit", "daily")
        habit_id = self.db.display_habits()[0][0]
        self.db.check_habit(habit_id)

        self.db.c.execute("SELECT streak FROM habits WHERE id = ?", (habit_id,))
        streak = self.db.c.fetchone()[0]
        self.assertEqual(streak, 1)

if __name__ == "__main__":
    unittest.main()
