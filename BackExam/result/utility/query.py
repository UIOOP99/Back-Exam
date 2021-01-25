from answerexam.models import DescriptiveAnswer, MultipleAnswer
from designexam.models import DescriptiveQuestion, MultipleQuestion, Exam
from account.models import User
from client_process.get_classes import get_classes


def get_users(exam_id):
    
    questions = DescriptiveQuestion.objects.filter(examID__pk=exam_id)
    users_id = DescriptiveAnswer.objects.filter(descriptive_questionID__in=questions).values_list('studentID', flat=True)
    users = User.objects.filter(pk__in=users_id)
    users = list(users)
    questions = MultipleQuestion.objects.filter(examID__pk=exam_id)
    users += list(MultipleAnswer.objects.filter(multiple_questionID__in=questions).values_list('studentID', flat=True))
    
    return list(set(users))


def get_exams(user_id):
    courses = get_classes(user_id)
    exams = Exam.objects.filter(courseID__in=courses).order_by('-start_date')
    return exams


def get_mul_answers(exam_id, user_id):
    questions = DescriptiveQuestion.objects.filter(examID__pk=exam_id)
    answers = DescriptiveAnswer.objects.filter(descriptive_questionID__in=questions, studentID__id=user_id)
    return answers


def get_p_answers(exam_id, user_id):
    questions = MultipleQuestion.objects.filter(examID__pk=exam_id)
    answers = MultipleAnswer.objects.filter(multiple_questionID__in=questions, studentID__id=user_id)
    return answers
