from django.urls import path
from . import views

urlpatterns=[
    path('descriptive-answer/', views.DescriptiveAnswerViewSet.as_view({
        'post': "create",
    })),
    path('multiple-answer/', views.MultipleAnswerViewSet.as_view({
        'post': "create",
    })),
    path('descriptive-answer/file/<int:pk>/', views.MultipleAnswerViewSet.as_view({
        "post": "create_file",
        "get": "get_file_url"})),
    path("answers/<int:examID>/<int:studentID>/", views.answers_list),
    path("answers/<int:examID>/", views.answers_list2),
]