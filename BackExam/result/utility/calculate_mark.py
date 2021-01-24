from answerexam.models import DescriptiveAnswer, MultipleAnswer
from designexam.models import DescriptiveQuestion, MultipleQuestion
from result.models import Result


def get_mark(exam_id, user_id):
    
    questions_id = DescriptiveQuestion.objects.filter(examID__id=exam_id).values_list('id', flat=True)
    answers = DescriptiveAnswer.objects.filter(studentID__id=user_id, descriptive_questionID__pk__in=questions_id).values_list('id', flat=True)
    sum_descriptve = Result.objects.filter(
        answer_id__in=answers, question_type="Descriptive").aggregate(sum('mark'))

    questions_id = MultipleQuestion.objects.filter(
        examID__id=exam_id).values_list('id', flat=True)
    answers = MultipleAnswer.objects.filter(studentID__id=user_id, multiple_questionID__pk__in=questions_id).values_list('id', flat=True)
    sum_multi = Result.objects.filter(answer_id__in=answers, question_type="Descriptive").aggregate(sum('mark'))

    return sum_descriptve + sum_multi