import unittest
from datetime import date
from Groupproject import Course, Student, University, Queue, Course, Student, Record, insertion_sort, selection_sort

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.course = Course("CSE1010", 3)
        self.student = Student("STU00001", "Mei")

    def test_course_creation(self):
        self.assertEqual(self.course.course_code, "CSE1010")
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.students, [])

    def test_add_student(self):
        self.course.add_student(self.student)
        self.assertIn(self.student, self.course.students)

    def test_no_duplicate_students(self):
        self.course.add_student(self.student)
        self.course.add_student(self.student)
        self.assertEqual(len(self.course.students), 1)

    def test_student_count(self):
        s2 = Student("S2", "Amani")
        self.course.add_student(self.student)
        self.course.add_student(s2)
        self.assertEqual(self.course.get_student_count(), 2)

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student("S1", "Mei")
        self.course1 = Course("CS101", 3)
        self.course2 = Course("MATH101", 4)

    def test_student_creation(self):
        self.assertEqual(self.student.student_id, "S1")
        self.assertEqual(self.student.name, "Mei")
        self.assertEqual(self.student.courses, {})

    def test_enroll(self):
        self.student.enroll(self.course1, "A")
        self.assertIn(self.course1, self.student.courses)
        self.assertIn(self.student, self.course1.students)

    def test_gpa_calculation(self):
        self.student.enroll(self.course1, "A")
        self.student.enroll(self.course2, "B")

        expected = ((4.0 * 3) + (3.0 * 4)) / 7
        self.assertAlmostEqual(self.student.calculate_gpa(), expected)

    def test_get_courses(self):
        self.student.enroll(self.course1, "A")
        courses = self.student.get_courses()
        self.assertIn(self.course1, courses)

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

        student1 = self.uni.add_student("STU00171", "Charlie")
        student2 = self.uni.add_student("STU00172", "Dana")

        student1.enroll(course, "A")
        student2.enroll(course, "B")

        self.assertEqual(self.uni.get_course_enrollment("CSE3100"), 2)

    def test_get_students_in_course(self):
        course = self.uni.add_course("PHY1010", 3)
        student = self.uni.add_student("STU00019", "Eve")
        student.enroll(course, "A")

        students = self.uni.get_students_in_course("PHY1010")
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, "Eve")

    def test_nonexistent_course(self):
        self.assertEqual(self.uni.get_course_enrollment("NONE"), 0)
        self.assertEqual(self.uni.get_students_in_course("NONE"), [])

class TestQueue(unittest.TestCase):

    def test_fifo_order(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)

        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_dequeue_empty_raises(self):
        q = Queue()
        with self.assertRaises(ValueError):
            q.dequeue()

    def test_size_tracking(self):
        q = Queue()
        self.assertEqual(len(q), 0)
        q.enqueue(10)
        q.enqueue(20)
        self.assertEqual(len(q), 2)
        q.dequeue()
        self.assertEqual(len(q), 1)


class TestEnrollment(unittest.TestCase):

    def setUp(self):
        self.course = Course("CSE2000", 3, 2)
        self.s1 = Student("STU00001", "Alice")
        self.s2 = Student("STU00002", "Bob")
        self.s3 = Student("STU00003", "Charlie")

    def test_enroll_until_capacity(self):
        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.assertEqual(len(self.course.roster), 2)

    def test_waitlist_when_full(self):
        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.course.request_enroll(self.s3, "2026-01-03")

        self.assertEqual(len(self.course.roster), 2)
        self.assertEqual(len(self.course.waitlist), 1)

    def test_drop_promotes_waitlist(self):
        self.course.request_enroll(self.s1, "2026-01-01")
        self.course.request_enroll(self.s2, "2026-01-02")
        self.course.request_enroll(self.s3, "2026-01-03")

        self.course.drop("STU00001", date(2026, 1, 5))

        ids = [r.student.student_id for r in self.course.roster]
        self.assertEqual(len(self.course.roster), 2)
        self.assertIn("STU00003", ids)


class TestSorting(unittest.TestCase):

    def setUp(self):
        self.records = [
            Record("Charlie", 103, "2026-01-14"),
            Record("Alice", 102, "2026-01-15"),
            Record("Bob", 101, "2026-01-12")
        ]

    def test_insertion_sort_by_id(self):
        insertion_sort(self.records, 'id')
        ids = [r.student_id for r in self.records]
        self.assertEqual(ids, [101, 102, 103])

    def test_selection_sort_by_name(self):
        selection_sort(self.records, 'name')
        names = [r.name for r in self.records]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])

    def test_sort_by_date(self):
        insertion_sort(self.records, 'date')
        dates = [r.date for r in self.records]
        self.assertEqual(dates, ["2026-01-12", "2026-01-14", "2026-01-15"])


class TestBinarySearch(unittest.TestCase):

    def binary_search(self, arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid].student_id == target:
                return mid
            elif arr[mid].student_id < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def setUp(self):
        self.records = [
            Record("A", 100, "2026-01-01"),
            Record("B", 101, "2026-01-02"),
            Record("C", 102, "2026-01-03"),
            Record("D", 103, "2026-01-04")
        ]

    def test_find_first(self):
        self.assertEqual(self.binary_search(self.records, 100), 0)

    def test_find_middle(self):
        self.assertEqual(self.binary_search(self.records, 102), 2)

    def test_find_last(self):
        self.assertEqual(self.binary_search(self.records, 103), 3)

    def test_not_found(self):
        self.assertEqual(self.binary_search(self.records, 999), -1)

    def test_unsorted_behavior(self):
        unsorted_records = [
            Record("C", 102, "2026-01-03"),
            Record("A", 100, "2026-01-01"),
            Record("B", 101, "2026-01-02"),
        ]
        result = self.binary_search(unsorted_records, 100)
        self.assertNotEqual(result, 1)

if __name__ == "__main__":
    unittest.main()