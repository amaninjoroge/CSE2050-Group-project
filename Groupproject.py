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


class Student: #Mei Mei
    """A class to respresent an student and their courses with grades"""
    
    GRADE_POINTS = { 
        'A' : 4.0, 'A-' : 3.7, 
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7, 
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7, 
        'D' : 1.0, 
        'F' : 0.0 
    }
    
    
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def enroll(self, course, grade:str): 
        self._courses[course] = grade
        if self not in course.students:
            course.students.append(self)
    
    def update_grade(self, course, grade:str):
        self._courses[course] = grade
    
    def calculate_gpa(self):
        """Compute weighted GPA using course credits."""
        total_points = 0
        total_credits = 0

        for course, grade in self.courses.items():
            if grade in Student.GRADE_POINTS:
                points = Student.GRADE_POINTS[grade]
                total_points += points * course.credit
                total_credits += course.credit

        if total_credits == 0:
            return 0.0

        return total_points / total_credits
    
    def get_courses(self):
        return list(self.courses.keys)
    
    def get_course_info(self):
        pass
    