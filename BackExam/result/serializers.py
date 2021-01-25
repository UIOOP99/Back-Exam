from rest_framework import serializers
from .models import Result
from designexam.models import Exam
from account.models import User
from answerexam.models import MultipleAnswer, DescriptiveAnswer
from .utility.answer_obj_checker import is_exist_answer
from .utility.calculate_mark import get_mark
from designexam.serializers import MultipleQuestionListSerializer, DescriptiveQuestionListSerializer


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"

    def validate(self, attr):
        if is_exist_answer(attr['answer_id'], attr['question_type']) is None:
            return serializers.ValidationError("anwser doesn't exist")
        return attr

    def update(self, instance, validated_data):
        instance.mark = validated_data.get('mark', instance.mark)
        instance.save()
        return instance


class ResultUserListSerializer(serializers.ModelSerializer):
    mark = serializers.SerializerMethodField('set_mark')

    def __init__(self, student_id=None):
        self.student_id = student_id
        
    class Meta:
        model = Exam
        fields = ('id', 'mark')

    def set_mark(self, obj):
        return get_mark(obj.id, self.student_id)


class ResultExamListSerializer(serializers.ModelSerializer):
    mark = serializers.SerializerMethodField('set_mark')

    def __init__(self, exam_id=None):
        self.exam_id = exam_id

    class Meta:
        model = User
        fields = ('id', 'mark')

    def set_mark(self, obj):
        return get_mark(obj.id, self.exam_id)


class MultiAnswerdetailSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField('set_result')
    multiple_questionID = MultipleQuestionListSerializer(read_only=True)

    class Meta:
        model = MultipleAnswer
        fields = ('id', 'multiple_questionID',
                  'studentID', 'answer_choice', 'created_date', 'result')

    def set_result(self, obj):
        try:
            result = Result.objects.get(obj.id, "Multiple")
            ser = ResultSerializer(result)
            return ser.data
        except:
            return {}


class DescriptiveAnswerdetailSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField('set_result')
    descriptive_questionID = DescriptiveQuestionListSerializer(read_only=True)

    class Meta:
        model = MultipleAnswer
        fields = ('id', 'descriptive_questionID',
                  'studentID', 'file_id', 'text', 'created_date', 'result')

    def set_result(self, obj):
        try:
            result = Result.objects.get(obj.id, "Descriptive")
            ser = ResultSerializer(result)
            return ser.data
        except:
            return {}


class Details:
    def __init__(self, multiple, descriptive):
        self.descriptive = descriptive
        self.multiple = multiple
        

class ResultDetailSerializer(serializers.Serializer):
    multiple = MultiAnswerdetailSerializer(many=True)
    descriptive = DescriptiveAnswerdetailSerializer(many=True)
