class Course: #Amani
    def __init__(self, course_code, credits, students):
        """function representing a single course in the university catalog"""
        self.course_code = str(course_code)
        self.credits = int(credits)
        self.students = []
    def add_student(self, student):
       if student not in self.students:
            self.students.append(student)
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
        self.courses[course] = grade
        if self not in course.students:
            course.students.append(self)
    
    def update_grade(self, course, grade:str):
        self.courses[course] = grade
    
    def calculate_gpa(self):
        """Compute weighted GPA using course credits."""
        total_points = 0
        total_credits = 0

        for course, grade in self.courses.items():
            if grade in Student.GRADE_POINTS:
                points = Student.GRADE_POINTS[grade]
                total_points += points * course.credits
                total_credits += course.credits

        if total_credits == 0:
            return 0.0

        return total_points / total_credits
    
    def get_courses(self):
        return list(self.courses.keys())
    
    def get_course_info(self):
        info = []
        for course, grade in self.courses.items():
            info.append({
                "course code": course.course.code,
                "credits": course.credit,
                "grade": grade
            })
        return info
     
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

