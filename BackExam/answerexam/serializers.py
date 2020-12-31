from rest_framework import serializers
from django.utils import timezone
from designexam.models import Exam, DescriptiveQuestion, MultipleQuestion
from .models import DescriptiveAnswer, MultipleAnswer
from client_process.file_management import create_file
from accounts.models import User


class DescriptiveFileSerializer(serializers.Serializer):
    answer_file = serializers.FileField(write_only=True, allow_null=True)

    def __init__(self, descriptive_answer_id=None,descriptive_que_id=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if descriptive_answer_id is not None:
            self.descriptiveAnswer_obj = DescriptiveAnswer.objects.get(id=descriptive_answer_id)
        else:
            self.descriptiveAnswer_obj = None
        if descriptive_que_id is not None:
            self.descriptiveQue_obj = DescriptiveQuestion.objects.get(id=descriptive_que_id)
        else:
            self.descriptiveQue_obj= None

    def validate_answer_file(self, value):
        if self.descriptiveQue_obj or self.descriptiveAnswer_obj is None:
            raise serializers.ValidationError()

        if self.no_file():
            raise serializers.ValidationError("this answer doesn't allow to send the file")

        file = value
        if file.content_type not in ['application/pdf', ]:
            raise serializers.ValidationError("the format is invalid")

        if file.size > 10485760:
            raise serializers.ValidationError("the size of file is above of 10 MB")

        self.file = file
        return file

    def no_file(self):
        if DescriptiveQuestion.objects.get(descriptive_questionID=self.descriptiveQue_obj).setting is False:
            return True
        return False

    def save_file(self):
        return create_file(self.file)

    def update_instance(self):
        response = self.save_file()
        self.descriptiveAnswer_obj.file_id= response
        self.descriptiveAnswer_obj.save()


class DescriptiveAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptiveAnswer
        fields = ('text', 'studentID', 'descriptive_questionID ', 'create_date')
        read_only_fields = ('studentID', 'created_date')

    def __init__(self, descriptive_que_id=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descriptiveQue_obj = DescriptiveQuestion.objects.get(id=descriptive_que_id)
        self.exam_obj = Exam.objects.get(id=self.descriptiveQue_obj.examID)

    def validate_descriptive_questionID(self, value):
        try:
            DescriptiveQuestion.objects.get(id=value)
            return value
        except:
            return serializers.ValidationError('the question does not exist')

    def validate_studentID(self, value):
        try:
            User.objects.get(id=value)
            return value
        except:
            return serializers.ValidationError('the student does not exist')

    def validate(self, attr):
        if self.exam_obj.end_date < timezone.now():
            raise serializers.ValidationError('time is over')
        return attr


class MultipleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleAnswer
        fields = ('answer_choice', 'studentID', 'multiple_questionID ', 'create_date')
        read_only_fields = ('studentID', 'created_date')

    def __init__(self, multiple_que_id=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multipleQue_obj = MultipleQuestion.objects.get(id=multiple_que_id)
        self.exam_obj = Exam.objects.get(id=self.multipleQue_obj.examID)

    def validate_multiple_questionID(self, value):
        try:
            MultipleQuestion.objects.get(id=value)
            return value
        except:
            return serializers.ValidationError('the question does not exist')

    def validate_studentID(self, value):
        try:
            User.objects.get(id=value)
            return value
        except:
            return serializers.ValidationError('the student does not exist')

    def validate(self, attr):

        if self.exam_obj.end_date < timezone.now():
            raise serializers.ValidationError('time is over')

        return attr

