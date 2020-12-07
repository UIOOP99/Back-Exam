from client_process.get_classes import get_common_classes
from designexam.models import Exam

class ExamConflictChecker:

    def __init__(self, start_time, end_time, course_id):
        self.start_time = start_time
        self.end_time = end_time
        self.course_id = course_id
    
    def get_class_list(self):
        classes = get_common_classes(self.course_id)
        #check the type of classes
        return classes

    def has_conflict(self):
        course_list = self.get_class_list()
        if Exam.objects.filter(courseID__in=course_list, start_date__gt=self.end_time, 
                                    end_date__lte=self.end_time) or \
            Exam.objects.filter(courseID__in=course_list, start_date__gte=self.start_time, 
                                    end_date__lt=self.start_time):
            return True
        
        return False
        