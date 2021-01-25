from django.db.models import Sum
from answerexam.models import DescriptiveAnswer, MultipleAnswer
from designexam.models import DescriptiveQuestion, MultipleQuestion
from result.models import Result


def get_mark(exam_id, user_id):
    questions_id = DescriptiveQuestion.objects.filter(examID__id=exam_id)
    answers = DescriptiveAnswer.objects.filter(studentID__id=user_id, descriptive_questionID__in=questions_id).values_list('id', flat=True)
    sum_descriptve = Result.objects.filter(
        answer_id__in=answers, question_type="Descriptive").aggregate(Sum('mark'))

    questions_id = MultipleQuestion.objects.filter(examID__id=exam_id)
    answers = MultipleAnswer.objects.filter(studentID__id=user_id, multiple_questionID__in=questions_id).values_list('id', flat=True)
    sum_multi = Result.objects.filter(answer_id__in=answers, question_type="Descriptive").aggregate(Sum('mark'))
    if sum_multi['mark__sum'] is None:
        sum_multi['mark__sum'] = 0
    if sum_descriptve['mark__sum'] is None:
        sum_descriptve['mark__sum'] = 0

    return sum_descriptve['mark__sum'] + sum_multi['mark__sum']
