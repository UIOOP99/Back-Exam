from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:pk>/', views.ResultViewSet.as_view({
        'get': "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    path('result/', views.ResultViewSet.as_view({'post': 'create'})),
    path('results-stu/<int:exam_id>/', views.ResultExamList.as_view()),
    path('results/<int:student_id>/', views.ResultStudentList.as_view()),
    path('results/<int:exam_id>/<int:student_id>/', views.ResultDetailList.as_view()),
]
