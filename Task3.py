class University: #Amani
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_course(self, course_code, credits):
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_course(self, course_code):
        return self.courses.get(course_code)

    def get_course_enrollment(self, course_code):
        course = self.get_course(course_code)
        if course is None:
            return 0
        return len(course.students)

    def get_students_in_course(self, course_code):
        course = self.get_course(course_code)
        if course is None:
            return []
        return list(course.students)