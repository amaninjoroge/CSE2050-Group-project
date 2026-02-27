import unittest
from Groupproject import Course, Student

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.course = Course("CS101", 3, [])
        self.student = Student("S1", "Mei")

    def test_course_creation(self):
        self.assertEqual(self.course.course_code, "CS101")
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.students, [])

    def test_add_student(self):
        self.course.add_student(self.student)
        self.assertIn(self.student, self.course.students)

    def test_no_duplicate_students(self):
        self.course.add_student(self.student)
        self.course.add_student(self.student)
        self.assertEqual(self.course.students.count(self.student), 1)

    def test_student_count(self):
        s2 = Student("S2", "Amani")
        self.course.add_student(self.student)
        self.course.add_student(s2)
        self.assertEqual(self.course.get_student_count(), 2)


# -----------------------
# STUDENT TESTS
# -----------------------

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student("S1", "Mei")
        self.course1 = Course("CS101", 3, [])
        self.course2 = Course("MATH101", 4, [])

    def test_student_creation(self):
        self.assertEqual(self.student.student_id, "S1")
        self.assertEqual(self.student.name, "Mei")
        self.assertEqual(self.student.courses, {})

    def test_enroll(self):
        self.student.enroll(self.course1, "A")
        self.assertIn(self.course1, self.student.courses)
        self.assertIn(self.student, self.course1.students)

    def test_gpa_calculation(self):
        self.student.enroll(self.course1, "A")  # 4.0 * 3
        self.student.enroll(self.course2, "B")  # 3.0 * 4

        expected = ((4.0 * 3) + (3.0 * 4)) / 7
        self.assertAlmostEqual(self.student.calculate_gpa(), expected)

    def test_get_courses(self):
        self.student.enroll(self.course1, "A")
        courses = self.student.get_courses()
        self.assertIn(self.course1, courses)


# -----------------------
# RUN TESTS
# -----------------------

if __name__ == "__main__":
    unittest.main()