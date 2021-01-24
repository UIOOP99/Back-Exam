from answerexam.models import DescriptiveAnswer, MultipleAnswer
from designexam.models import DescriptiveQuestion, MultipleQuestion, Exam
from client_process.get_classes import get_classes


def get_users(exam_id):
    
    questions = DescriptiveQuestion.objects.filter(examID__pk=exam_id).values_list('id', flat=True)
    users = DescriptiveAnswer.objects.filter(descriptive_questionID__pk__in=questions).values_list('studentID', flat=True)
    questions = MultipleQuestion.objects.filter(examID__pk=exam_id).values_list('id', flat=True)
    users += MultipleAnswer.objects.filter(multiple_questionID__pk__in=questions).values_list('studentID', flat=True)

    return list(set(users))


def get_exams(user_id):
    courses = get_classes(user_id)
    exams = Exam.objects.filter(courseID__in=courses)
    return exams