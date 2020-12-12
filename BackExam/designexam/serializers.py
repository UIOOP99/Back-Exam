from rest_framework import serializers
import datetime
from client_process.file_management import create_file
from client_process.get_classes import is_exist
from django.utils import timezone
from .exam_extra_classes.check_conflict import ExamConflictChecker
from .models import Exam, DescriptiveQuestion, MultipleQuestion


class ExamFileSerializer(serializers.Serializer):
    questions_file = serializers.FileField(write_only=True, allow_null=True)

    def __init__(self, exam_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exam_obj = Exam.objects.get(id = exam_id)

    def validate_questions_file(self, value):
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
            raise serializers.ValidationError('start date must be less than now')
        return value

    def validate_end_date(self, value):
        try:
            start_time = datetime.datetime.strptime(self.initial_data['start_date'], '%Y-%m-%dT%H:%M:%S.%f')
        except:
            raise serializers.ValidationError('the format of time is invalid')

        if value <= timezone.now() or value <= start_time:
            raise serializers.ValidationError('end date must be less than start time and now')

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
        print(validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description) 
        instance.author = validated_data.get('author', instance.author) 

        if instance.start_date > datetime.datetime.now():
            instance.start_date = validated_data.get('start_date', instance.start_date)
        if instance.end_date > datetime.datetime.now():
            instance.end_date = validated_data.get('end_date', instance.end_date)

        instance.save()

        return instance



class ExamListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('set_status')

    class Meta:
        model = Exam
        fields = ('id', 'title', 'courseID', 'start_date', 'end_date', 'status')

    def set_status(self, obj):
        if datetime.datetime.now() < obj.start_date:
            return 'not held'
        elif datetime.datetime.now() > obj.end_date:
            return 'finished'
        else:
            return 'holding'



    


    
