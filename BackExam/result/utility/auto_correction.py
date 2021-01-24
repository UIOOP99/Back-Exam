from answerexam.models import MultipleAnswer
from result.models import Result

class AutoCorrection:

    def __init__(self, anwser_id, question_type):
        if question_type != 'Multiple':
            raise TypeError
        self.answer_id = anwser_id
    
    def get_anwser_question(self):
        answer = MultipleAnswer.objects.get(id=self.answer_id)
        return answer, answer.multiple_questionID

    def correct(self):
        answer, question = self.get_anwser_question()
        match = self.match_num(answer.answer_choice, question.answer)
        return (match/len(question.answer)) * question.mark
    
    def match_num(self, answer_choise, correct_answer):
        num = 0
        for i in range(len(answer_choise)):
            if answer_choise[i] == correct_answer[i]:
                num += 1
        return num

    def save(self):
        mark = self.correct()
        result = Result(answer_id=self.answer_id,mark=mark, question_type="Multiple")
        result.save