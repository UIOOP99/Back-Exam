from django.urls import path
from . import views

urlpatterns=[
    path('exam/<int:pk>/', views.ExamViewSet.as_view({
        'get': "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    path('exam/file/<int:pk>/', views.ExamViewSet.as_view({
        "post": "create_file",
        "delete": "delete_file",
        "get": "get_file_url"})),
    path("exam/", views.ExamViewSet.as_view({"post": "create", })),
    # path("exams/", views.ExamViewSet.as_view({"get": "get_exams",})),
    path("exams/", views.Exams.as_view()),
    path("exams/<str:course_id>/", views.CourseExams.as_view()),


    path('descriptive-question/', views.DescriptiveQuestionViewSet.as_view({
        'post': "create",
    })),
    path('multiple-question/', views.MultipleQuestionViewSet.as_view({
        'post': "create",
    })),
    path('descriptive-question/file/<int:pk>/', views.DescriptiveQuestionViewSet.as_view({
        "post": "create_file",
        "get": "get_file_url"})),

    path('multiple-question/file/<int:pk>/', views.MultipleQuestionViewSet.as_view({
        "post": "create_file",
        "get": "get_file_url"})),
    path("questions/<int:pk>/", views.questions_list),
    # path("descriptive-questions/<int:pk>/", views.DescriptiveQuestions.as_view()),
    # path("multiple-questions/<int:pk>/", views.MultipleQuestions.as_view()),
]