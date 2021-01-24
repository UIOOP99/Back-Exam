from answerexam.models import MultipleAnswer, DescriptiveAnswer



def is_exist_answer(answer_id, type_q):
    if type_q == 'Descriptive':
        try:
            answer = DescriptiveAnswer.objects.get(pk=answer_id)
            return answer
        except DescriptiveAnswer.DoesNotExist:
            return None

    elif type_q == 'Multiple':
        try:
            answer = MultipleAnswer.objects.get(pk=answer_id)
            return answer
        except MultipleAnswer.DoesNotExist:
            return  None
    return None


def get_exam_obj(answer_id, type_q):
    answer = is_exist_answer(answer_id, type_q)
    if answer is None:
        return None
    if type_q == 'Descriptive':
        return answer.descriptive_questionID.examID

    else:
        return answer.multiple_questionID.examID
