from result.models import Result


class AutoCorrection:

    def __init__(self, anwser, question_type):
        if question_type != 'Multiple':
            raise TypeError
        self.answer = anwser
    
    def get_anwser_question(self):
        return self.answer, self.answer.multiple_questionID

    def correct(self):
        answer, question = self.get_anwser_question()
        c = self.correct_answer(question.answer)
        match = self.match_num(answer.answer_choice, question.answer)
        return (match/c) * question.mark

    def correct_answer(self, correct_answer):
        num = 0
        for each in correct_answer:
            if each == "1":
                num += 1
        return num
    
    def match_num(self, answer_choise, correct_answer):
        num = 0
        for i in range(len(answer_choise)):
            if answer_choise[i] == '1':
                if answer_choise[i] == correct_answer[i]:
                    num += 1
        return num

    def save(self):
        mark = self.correct()
        result = Result(answer_id=self.answer.pk, mark=mark, question_type="Multiple")
        result.save()
