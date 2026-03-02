import unittest
from Groupproject import Course, Student, University

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.course = Course("CSE1010", 3, [])
        self.student = Student("STU00001", "Mei")

    def test_course_creation(self):
        self.assertEqual(self.course.course_code, "CS1010")
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

# Student test

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

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

class Course:
    def __init__(self, course_code, credits):
        self.course_code = course_code
        self.credits = credits
        self.students = []

class UniversityTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = University()

    def test_add_course(self):
        course = self.uni.add_course("CSE1010", 3)
        self.assertEqual(course.course_code, "CSE1010")
        self.assertEqual(course.credits, 3)
        self.assertIn("CSE1010", self.uni.courses)

    def test_add_student(self):
        student = self.uni.add_student("STU00016", "Alice")
        self.assertEqual(student.student_id, "STU00016")
        self.assertEqual(student.name, "Alice")
        self.assertIn("STU00016", self.uni.students)

    def test_get_student(self):
        self.uni.add_student("STU00017", "Bob")
        student = self.uni.get_student("STU00017")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Bob")

    def test_get_course(self):
        self.uni.add_course("MATH1010", 3)
        course = self.uni.get_course("MATH1010")
        self.assertIsNotNone(course)
        self.assertEqual(course.credits, 3)

    def test_get_course_enrollment(self):
        course = self.uni.add_course("CSE3100", 2)
        self.assertEqual(self.uni.get_course_enrollment("CSE3100"), 0)

        student1 = self.uni.add_student("STU00171", "Charlie")
        student2 = self.uni.add_student("STU00172", "Dana")
        course.students.append(student1)
        course.students.append(student2)

        self.assertEqual(self.uni.get_course_enrollment("CHEM1010"), 3)

    def test_get_students_in_course(self):
        course = self.uni.add_course("PHY1010", 3)
        student = self.uni.add_student("STU00019", "Eve")
        course.students.append(student)

        students = self.uni.get_students_in_course("PHY1010")
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, "Eve")

    def test_nonexistent_course(self):
        self.assertEqual(self.uni.get_course_enrollment("NONE"), 0)
        self.assertEqual(self.uni.get_students_in_course("NONE"), [])

if __name__ == "__main__":
    unittest.main()