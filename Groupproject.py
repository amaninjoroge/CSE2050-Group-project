class Course: #Amani
    def __init__(self, course_code, credits, students):
        """function representing a single course in the university catalog"""
        self.course_code = str(course_code)
        self.credits = int(credits)
        self.students = []
    def add_student(self, student):
       self.student = student
       self.student.append(student)
    def get_student_count(self):
        return len(self.students)

