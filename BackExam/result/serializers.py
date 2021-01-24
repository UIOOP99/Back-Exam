from rest_framework import serializers
from .models import Result
from answerexam.models import MultipleAnswer, DescriptiveAnswer
from .utility.answer_obj_checker import is_exist_answer


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


class ResultListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
