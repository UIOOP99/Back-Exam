from client_process.get_classes import get_common_classes
from designexam.models import Exam

class ExamConflictChecker:

    def __init__(self, start_time, end_time, course_id, exam_id=-1):
        self.start_time = start_time
        self.end_time = end_time
        self.course_id = course_id
        self.exam_id = exam_id
    
    def get_class_list(self):
        classes = get_common_classes(self.course_id)
        return classes

    def has_conflict(self):
        course_list = self.get_class_list()

        if Exam.objects.filter(courseID__in=course_list, start_date__lt=self.end_time, 
                                    end_date__gte=self.end_time).exclude(id=self.exam_id) or \
            Exam.objects.filter(courseID__in=course_list, start_date__lte=self.start_time, 
                                    end_date__gt=self.start_time).exclude(id=self.exam_id):

            return True
        
        return False
        