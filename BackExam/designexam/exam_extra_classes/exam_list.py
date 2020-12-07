from designexam.model import Exam
from client_process.get_classes import get_classes


class ExamList:

    def __init__(self, id):
        self.user_id = id
        self.role = None

    def get_role(self):
        pass

    def admin_list(self):
        exams = Exam.objects.all().order_by('start_date')
        return exams

    def get_course_list(self):
        course_list = get_classes(self.user_id)
        #check the type of course_list
        return course_list

    def student_teacher_list(self):
        course_list = self.get_course_list()
        exams = Exam.objects.filter(courseId__in=course_list).order_by('start_date')
        return exams

    def get_exams(self):
        self.get_role()
        if self.role == 'ADMIN':
            exams = self.admin_list()

        else:
            exams = self.student_teacher_list()

        return exams
        

class CourseExamList:
    
    def __init__(self, course_id):
        self.course_id = course_id

    def get_exams(self):
        exams = Exam.objects.filter(courseID=self.course_id)
        return exams