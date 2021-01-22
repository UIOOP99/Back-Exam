from rest_framework import serializers
import datetime
from client_process.file_management import create_file
from client_process.get_classes import is_exist
from django.utils import timezone
from drf_yasg.utils import swagger_serializer_method
from drf_yasg import openapi
from .exam_extra_classes.check_conflict import ExamConflictChecker
from .models import Exam, DescriptiveQuestion, MultipleQuestion, DescriptiveQuestionFile, MultipleQuestionFile


class ExamFileSerializer(serializers.Serializer):
    questions_file = serializers.FileField(write_only=True, allow_null=True)

    def __init__(self, exam_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if exam_id is not None:
            self.exam_obj = Exam.objects.get(id = exam_id)
        else:
            self.exam_obj = None

    def validate_questions_file(self, value):
        if self.exam_obj is None:
            raise serializers.ValidationError()
        if self.has_questions():
            raise serializers.ValidationError("this exam has questions")

        file = value
        if file.content_type not in ['application/pdf', ]:
            raise serializers.ValidationError("the format is invalid")

        if file.size > 10485760:
            raise serializers.ValidationError("the size of file is above of 10 MB")

        self.file = file
        return file

    def has_questions(self):
        if DescriptiveQuestion.objects.filter(examID=self.exam_obj) or \
             MultipleQuestion.objects.filter(examID=self.exam_obj):
            return True
        return False

    def save_file(self):
        return create_file(self.file)

    def update_instance(self):
        response = self.save_file()
        self.exam_obj.have_file = True
        self.exam_obj.file_id = response
        self.exam_obj.save()


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ('id', 'title', 'courseID', 'description', 'start_date', 'end_date', 'have_file', 'setting',
                    'created_date', 'author')
        read_only_fields = ('author', 'have_file', 'create_date')

    def validate_start_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('start date must be more than now')
        return value

    def validate_end_date(self, value):
        try:
            start_time = datetime.datetime.strptime(self.initial_data['start_date'], '%Y-%m-%dT%H:%M:%S.%f')
        except:
            raise serializers.ValidationError('the format of time is invalid')

        if value <= timezone.now() or value <= start_time:
            raise serializers.ValidationError('end date must be more than start time and now')

        return value

    def validate_courseID(self, value):
        if is_exist(value):
            return value
        else:
            return serializers.ValidationError('the course does not exist') 

    def validate(self, attr):
        if self.instance:
            start_date = attr.get('start_date', self.instance.start_date)
            end_date = attr.get("end_date", self.instance.end_date)
            course_id = self.instance.courseID
            exam_id = self.instance.id
        else:
            start_date = attr['start_date']
            end_date = attr['end_date']
            course_id = attr['courseID']
            exam_id = -1
        checker = ExamConflictChecker(start_date, end_date, course_id, exam_id).has_conflict()
        if checker:
            raise serializers.ValidationError('this time have conflict with other exams')

        return attr 

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description) 
        instance.author = validated_data.get('author', instance.author) 

        if instance.start_date > datetime.datetime.now():
            instance.start_date = validated_data.get('start_date', instance.start_date)
            instance.setting = validated_data.get('setting', instance.setting)
        if instance.end_date > datetime.datetime.now():
            instance.end_date = validated_data.get('end_date', instance.end_date)

        instance.save()

        return instance


class ExamListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('set_status')

    class Meta:
        model = Exam
        fields = ('id', 'title', 'courseID', 'start_date', 'end_date', 'status')

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def set_status(self, obj):
        if datetime.datetime.now() < obj.start_date:
            return 'not held'
        elif datetime.datetime.now() > obj.end_date:
            return 'finished'
        else:
            return 'holding'


class DescriptiveQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DescriptiveQuestion
        fields = '__all__'

    def validate_number(self, value):
        try:
            des = DescriptiveQuestion.objects.filter(number=value)
            raise serializers.ValidationError("the question number is a duplicate")
        except:
            pass

    def validate_examID(self, value):
        try:
            exam = Exam.objects.filter(examID=value)
        except:
            raise serializers.ValidationError("the exam does not exist")


class MultipleQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleQuestion
        fields = '__all__'

    def validate_number(self, value):
        try:
            mul = MultipleQuestion.objects.filter(number=value)
            raise serializers.ValidationError("the question number is duplicate")
        except:
            pass

    def validate_examID(self, value):
        try:
            exam = Exam.objects.filter(examID=value)
        except:
            raise serializers.ValidationError("the exam does not exist")


class DescriptiveQuestionFileSerializer(serializers.ModelSerializer):
    question_file = serializers.FileField(write_only=True, allow_null=True)

    class Meta:
        model = DescriptiveQuestionFile
        fields = '__all__'

    def __init__(self, descriptive_que_id=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if descriptive_que_id is not None:
            self.descriptiveQue_obj = DescriptiveQuestion.objects.get(id=descriptive_que_id)
        else:
            self.descriptiveQue_obj= None

    def validate_question_file(self, value):
        if self.descriptiveQue_obj is None:
            raise serializers.ValidationError("this question does not exist")

        file = value
        if file.content_type not in ['application/pdf', ]:
            raise serializers.ValidationError("the format is invalid")

        if file.size > 10485760:
            raise serializers.ValidationError("the size of file is above of 10 MB")

        if Exam.objects.filter(examID=self.descriptiveQue_obj.examID).setting:
            raise serializers.ValidationError("this exam has a file containing all the questions")

        self.file = file
        return file

    def save_file(self):
        return create_file(self.file)

    def create(self, validated_data):
        quefile = DescriptiveQuestionFile.objects.create(descriptive_questionID=validated_data["descriptive_questionID"],
                                                         file_id=self.save_file())
        return quefile.id


class MultipleQuestionFileSerializer(serializers.ModelSerializer):

    question_file = serializers.FileField(write_only=True, allow_null=True)

    class Meta:
        model = MultipleQuestionFile
        fields = '__all__'

    def __init__(self, multiple_que_id=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if multiple_que_id is not None:
            self.multipleQue_obj = MultipleQuestion.objects.get(id=multiple_que_id)
        else:
            self.multipleQue_obj= None

    def validate_question_file(self, value):
        if self.multipleQue_obj is None:
            raise serializers.ValidationError("this question does not exist")

        file = value
        if file.content_type not in ['application/pdf', ]:
            raise serializers.ValidationError("the format is invalid")

        if file.size > 10485760:
            raise serializers.ValidationError("the size of file is above of 10 MB")

        if Exam.objects.filter(examID=self.multipleQue_obj.examID).setting:
            raise serializers.ValidationError("this exam has a file containing all the questions")

        self.file = file
        return file

    def save_file(self):
        return create_file(self.file)

    def create(self, validated_data):
        quefile = MultipleQuestionFile.objects.create(descriptive_questionID=validated_data["descriptive_questionID"],
                                                      file_id=self.save_file())
        return quefile.id


class DescriptiveQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptiveQuestion
        fields = '__all__'


class MultipleQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleQuestion
        fields = '__all__'
