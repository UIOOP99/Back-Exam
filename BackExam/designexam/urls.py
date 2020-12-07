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
        "delete": "delete_file"})),
    path("exam/", views.ExamViewSet.as_view({"post": "create", })),
    path("exams/", views.ExamViewSet.as_view({"get": "get_exams",})),
    path("get-course-exams/<int:course_id>/", views.get_course_exams),
]