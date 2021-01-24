from rest_framework import serializers
from .models import Result
from answerexam.models import MultipleAnswer, DescriptiveAnswer


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"

    def validate(self, attr):
        answer_id = attr['answer_id']
        if attr['question_type'] == 'Descriptive':
            try:
                answer = DescriptiveAnswer.objects.get(pk=answer_id)
            except DescriptiveAnswer.DoesNotExist:
                return serializers.ValidationError("anwser doesn't exist")

        elif attr['question_type'] == 'Multiple':
            try:
                answer = MultipleAnswer.objects.get(pk=answer_id)
            except MultipleAnswer.DoesNotExist:
                return serializers.ValidationError("anwser doesn't exist")

        return attr

    def update(self, instance, validated_data):
        instance.mark = validated_data.get('mark', instance.mark)
        instance.save()
        return instance
