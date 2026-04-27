import csv
from datetime import date

class EnrollmentRecord: #Mei Mei Task 1
    """to represent enrollment in course"""
    def __init__(self, student, enroll_date):
        self.student = student
        
        if isinstance(enroll_date, str):
            year, month, day = map(int, enroll_date.split("-"))
            self.enroll_date = date(year, month, day)
        else:
            self.enroll_date = enroll_date

class Node: #Amani
    def __init__(self, data):
        """Node class for waitlist"""
        self.data = data
        self.next = None

class Queue: #Amani
    def __init__(self):
        """Queue for waitlist"""
        self.head = None  
        self.tail = None   
        self.size = 0

    def enqueue(self, item):
        """Adds students to the back of the waitlist"""
        new_node = Node(item)

        if self.tail is None:      
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def dequeue(self):
        """removing students from the front of the waitlist"""
        if self.head is None:
            raise ValueError("Queue is empty")

        value = self.head.data
        self.head = self.head.next

        if self.head is None:      
            self.tail = None

        self.size -= 1
        return value

    def is_empty(self):
        """checking if the list is empty"""
        return self.size == 0

    def __len__(self):
        """retuns the number of students"""
        return self.size
    
    # Mei Mei Task 5
def recursive_binary_search(records, target_id, low, high):
    """binary search to find a student by ID"""
    if low > high:
        return -1
    
    mid = (low + high) // 2 
    mid_id = records[mid].student.student_id

    if mid_id == target_id:
        return mid
    elif target_id < mid_id:
        return recursive_binary_search(records, target_id, low, mid - 1)
    else:
        return recursive_binary_search(records, target_id, mid + 1, high)

class Stack: #Mei Mei extra credit
    def __init__(self):
        """Stack ADT to add an undo feature """
        self._data = []

    def push(self, item):
        """add the action"""
        self._data.append(item)
    
    def pop(self):
        """remove action"""
        if not self._data:
            raise ValueError("Nothing to undo")
        return self._data.pop()
    
    def is_empty(self):
        return len(self._data) == 0 

class Course: #Amani
    def __init__(self, course_code, credits, capacity):
        """function representing a single course in the university catalog"""
        self.course_code = str(course_code)
        self.credits = int(credits)
        self.students = []
        #Mei Mei for task 3 methods
        self.capacity = int(capacity)
        self.roster = []
        self.waitlist = Queue()
        self.history = Stack() # Mei Extra cred
        
        
    def add_student(self, student):
       """adds a student obkect to the course roster"""
       if student not in self.students:
            self.students.append(student)
    def get_student_count(self):
        """returns the number of students currently enrolled"""
        return len(self.students)
    
    def is_enrolled(self, student): #Mei Mei extra credit
        """return student is enrolled"""
        return any(record.student == student for record in self.roster)

    def is_waitlisted(self, student): #Mei extra credit
        """check if student is waitlisted"""
        current = self.waitlist.head
        
        while current:
            if current.data[0] == student: 
                return True
            current = current.next
        return False
    
    
    def request_enroll(self, student, enroll_date): #Mei Mei
        """checks if already enrolled, if space advailable then enroll or add to waitlist if full"""
        if self.is_enrolled(student):
            
            raise ValueError(f"{student.name} is already enrolled in {self.course_code}.")

        if self.is_waitlisted(student):
            raise ValueError(f"{student.name} is already waitlisted for {self.course_code}.")

        if len(self.roster) < self.capacity:
            record = EnrollmentRecord(student, enroll_date)
            self.roster.append(record)
            self.students.append(student)
            self.history.push(("enroll", record))  
            print(f"{student.name} enrolled in {self.course_code}.")
        else:
            self.waitlist.enqueue((student, enroll_date))
            print(f"{student.name} added to waitlist for {self.course_code}.")

    def drop(self, student_id, enroll_date_for_replacement=None): #Mei Mei
        """removes a student from the enrolled roster by student id"""
        self.roster.sort(key=lambda r: r.student.student_id)
        
        index = recursive_binary_search(self.roster, student_id, 0, len(self.roster) - 1)
        
        if index == -1:
            print(f"Student ID {student_id} not found in {self.course_code}.")
            return
            

        removed = self.roster.pop(index)
        self.students.remove(removed.student)
        self.history.push(("drop", removed))
        print(f"{removed.student.name} dropped from {self.course_code}.")

        if not self.waitlist.is_empty():
            next_student, _ = self.waitlist.dequeue()
            new_enroll_date = enroll_date_for_replacement or date.today()
            self.request_enroll(next_student, new_enroll_date)
    
    def undo(self): #Mei Mei extra credit
        """Method to undo action"""
        if self.history.is_empty():
            print("No actions to undo.")
            return

        action, record = self.history.pop()
        if action == "enroll":
            self.roster = [r for r in self.roster if r.student != record.student]
            if record.student in self.students:
                self.students.remove(record.student)
            print(f"Undo: removed {record.student.name} from {self.course_code}")

        elif action == "drop":
            if len(self.roster) < self.capacity:
                self.roster.append(record)
                self.students.append(record.student)
                print(f"Undo: re-enrolled {record.student.name} in {self.course_code}")
            else:
                self.waitlist.enqueue((record.student, record.enroll_date))
                print(f"Undo: waitlisted {record.student.name} (course full)")
        




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
        """initialize student id and name to student object"""
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def enroll(self, course, grade:str): 
        """ enrolls the student in a course with the givin grade and update course roster"""
        self.courses[course] = grade
        if self not in course.students:
            course.students.append(self)
    
    def update_grade(self, course, grade:str):
        """modify  the student grade for a course"""
        if course in self.courses:
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
            raise ValueError

        return total_points / total_credits
    
    def get_courses(self):
        """returns a list of course object taken by the student"""
        return list(self.courses.keys())
    
    def get_course_info(self): 
        """ returns a structured summary of all enrollments"""
        table = []
    
        header = f"{'Course Code':<15}{'Credits':<10}{'Grade':<10}"
        separator = "-" * 35
    
        table.append(header)
        table.append(separator)

        for course, grade in self.courses.items():
            row = f"{course.course_code:<15}{course.credits:<10}{grade:<10}"
            table.append(row)

        return "\n".join(table)
     
class University: #Amani
    def __init__(self):
        """stores all students and courses"""
        self.students = {}
        self.courses = {}

    def add_course(self, course_code, credits, capacity):
        """adds courses and returns them as objects"""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits, capacity)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        """creates and returns student objects"""
        if len(student_id) != 8:
            raise ValueError("Id's are 8 character length")
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):
        """returns the student object for that ID"""
        return self.students.get(student_id)

    def get_course(self, course_code):
        """returns the course object"""
        return self.courses.get(course_code)

    def get_course_enrollment(self, course_code):
        """returns the number of students enrolled in the given course"""
        course = self.get_course(course_code)
        if course is None:
            return 0
        return len(course.students)

    def get_students_in_course(self, course_code):
        """returns the number of students enrolled in the given course"""
        course = self.get_course(course_code)
        if course is None:
            return []
        return list(course.students)
    
    def students_in_course(self, course_code):
        """Gets the list of students enrolled in a course"""
        course = self.get_course(course_code)

        if not course:
            print("Course not found")
            return[]
        return [student.name for student in course.students]

    def print_student_gpa(self, student_id):
        """Prints GPA of a student"""
        student = self.get_student(student_id)
        if student:
            return student.calculate_gpa()
        return None
    
    def print_student_courses(self, student_id):
        """prints course info for a student"""
        student = self.get_student(student_id)
        if student:
            return student.get_course_info()
        return None
    
    def course_grade_stats(self, course_code):
        """returns mean median and mode of grades for a course"""
        course = self.get_course(course_code)
        if not course:
            return None

        grades = []

        for student in course.students:
            grade = student.courses.get(course)
            if grade in Student.GRADE_POINTS:
                grades.append(Student.GRADE_POINTS[grade])

        if len(grades) == 0:
            return None
        
        mean = sum(grades) / len(grades)
        grades.sort()
        n = len(grades)

        if n % 2 == 1:
            median = grades[n // 2]
        else:
            median = (grades[n//2 - 1] + grades[n//2]) / 2

        counts = {}
        for g in grades:
            counts[g] = counts.get(g, 0) + 1

        mode = max(counts, key=counts.get)
        return {"mean": mean, "median": median, "mode": mode}
    
    def university_gpa_stats(self):
        """Mean and median GPA of all students"""
        gpas = []

        for student in self.students.values():
            if len(student.courses) > 0:
                gpas.append(student.calculate_gpa())

        if len(gpas) == 0:
            return None
        
        mean = sum(gpas) / len(gpas)
        gpas.sort()
        n = len(gpas)

        if n % 2 == 1:
            median = gpas[n // 2]
        else:
            median = (gpas[n//2 - 1] + gpas[n//2]) / 2
        return {"mean": mean, "median": median}
    
    
    
    def common_students(self, course_code1, course_code2):
        """returns common students in two different courses"""
        course1 = self.get_course(course_code1)
        course2 = self.get_course(course_code2)

        if not course1 or not course2:
            return[]
        students1 = set(course1.students)
        students2 = set(course2.students)

        common = students1.intersection(students2)
        return [student.name for student in common]


    
    #Mei Mei
    """functions to open and read the csv files"""

    def load_university_data_csv(self):
        """open and reads university_data.csv"""
        with open("university_data.csv", mode = "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_id = row["student_id"]
                name = row["name"]
                courses_string = row["courses"]

                student = self.add_student(student_id, name)

                if courses_string:
                    courses_pairs = courses_string.split(";")

                    for pair in courses_pairs:
                        course_code, grade = pair.split(":")

                        course = self.get_course(course_code)

                        if course:
                            student.enroll(course, grade)
   
    def load_courses_csv_with_capacity(self, filename="course_catalog_CSE10_with_capacity.csv"):
        """ open and reads course_catalog.csv """
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                course_code = row["course_code"]
                credits = int(row["credits"])
                capacity = int(row["capacity"]) if "capacity" in row and row["capacity"] else 30
            
                self.add_course(course_code, credits, capacity)

class Record: #Amani
    """records the name, student id and date enrolled"""
    def __init__(self, name, student_id, date):
            self.name = name
            self.student_id = student_id
            self.date = date

    def __str__(self):
            """returns name, id, and date"""
            return f"{self.name}, ID: {self.student_id}, Date: {self.date}"

def get_key(record, by):
    """gets a specific student's name, record, and date"""
    if by == 'name':
        return record.name
    elif by == 'id':
        return record.student_id
    elif by == 'date':
        return record.date
    else:
        raise ValueError("Invalid sort key")

def insertion_sort(arr, by):
    """sorts students in the roster using insertion sort"""
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and get_key(arr[j], by) > get_key(current, by):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current

def selection_sort(arr, by):
    """sorts students by using selection sort"""
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if get_key(arr[j], by) < get_key(arr[min_index], by):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

class CourseWithSort:
    def __init__(self):
        """Sorting the enrolled roster"""
        self.enrolled = []
        self.enrolled_sorted_by = None

    def add_student(self, record):
        """adds students to the roster"""
        self.enrolled.append(record)

    def sort_enrolled(self, by, algorithm):
        """sorting the enrolled students using insertion and selection"""
        if algorithm == 'insertion':
            insertion_sort(self.enrolled, by)
        elif algorithm == 'selection':
            selection_sort(self.enrolled, by)
        else:
            raise ValueError("Invalid sorting algorithm")
        self.enrolled_sorted_by = by

    def print_roster(self):
        """prints the sorted roster"""
        print(f"Roster sorted by: {self.enrolled_sorted_by}")
        for record in self.enrolled:
            print(record)
    

if __name__ == "__main__": #Amani (demo)  

    uni = University()
    uni.load_courses_csv_with_capacity()
    uni.load_university_data_csv()
    

    print("Total students:", len(uni.students))
    print("Total courses:", len(uni.courses))

    for student in uni.students.values():
        print(student.name, "enrolled in:")
        for course, grade in student.courses.items():
            print("  ", course.course_code, "-", grade)

    course_code = "CSE1010"
    students = uni.get_students_in_course(course_code)

    print("\nStudents enrolled in", course_code)
    for s in students:
        print(s.name)

    student_id = list(uni.students.keys())[0]
    student = uni.get_student(student_id)

    print("\nGPA of", student.name, ":", student.calculate_gpa())

    print("\nCourses for", student.name)
    print(student.get_course_info())

    stats = uni.course_grade_stats(course_code)

    print("\nGrade statistics for", course_code)
    print("Mean:", stats["mean"])
    print("Median:", stats["median"])
    print("Mode:", stats["mode"])

    gpa_stats = uni.university_gpa_stats()

    print("\nUniversity GPA statistics")
    print("Mean GPA:", gpa_stats["mean"])
    print("Median GPA:", gpa_stats["median"])

    course1 = "CSE1010"
    course2 = "CSE2050"

    common = uni.common_students(course1, course2)

    print("\nCommon students in", course1, "and", course2)
    for name in common:
        print(name)

    course = CourseWithSort()
    course.add_student(Record("Alice", 102, "2026-01-15"))
    course.add_student(Record("Bob", 101, "2026-01-12"))
    course.add_student(Record("Charlie", 103, "2026-01-14"))

    course.sort_enrolled('name', 'insertion')
    course.print_roster()
    print()

    course.sort_enrolled('id', 'selection')
    course.print_roster()
    print()

    course.sort_enrolled('date', 'insertion')
    course.print_roster()

    #Nana



            

