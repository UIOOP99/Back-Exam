from rest_framework import serializers
import datetime
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = "__all__"
        read_only_fields = ('author', 'file_URL', 'have_file')

    def __init__(self, author):
        self.author = author
        super().__init__()

    def validate_start_date(self, value):
        if value > datetime.datetime.now():
            return value
        raise serializers.ValidationError('start date must be less than now')

    def validate_end_date(self, value):
        try:
            start_time = datetime.datetime.strptime(self.initial_data['start_date'], format='%Y-%m-%dT%H:%M:%S.%f')
        except:
            raise serializers.ValidationError('the format of time is invalid')
        if value > datetime.datetime.now() and value > start_time:
            return value

        raise serializers.ValidationError('end date must be less than start time')

    def validate_duration(self, value):
        try:
            start_time = datetime.datetime.strptime(self.initial_data['start_date'], format='%Y-%m-%dT%H:%M:%S.%f')
            end_time = datetime.datetime.strptime(self.initial_data['end_date'], format='%Y-%m-%dT%H:%M:%S.%f')
        except:
            raise serializers.ValidationError('the format of datetime id invalid')

        start_plus_duration = start_time + datetime.timedelta(minutes=value)
        if start_plus_duration <= end_time:
            return value
        
        raise serializers.ValidationError('start_time + duration is not less than end_time')

    def create(self, validated_data):
        exam = super().create(validated_data)
        exam.author = self.author
        exam.save()
        return exam
