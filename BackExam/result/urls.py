from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:pk>/', views.ResultViewSet.as_view({
        'get': "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    path('result/', views.ResultViewSet.as_view({'post': 'create'})),
    path('results-stu/<int:exam-id>', views.ResultExamList.as_view()),
    path('results/<int:student-id>/', views.ResultStudentList.as_view()),
]
