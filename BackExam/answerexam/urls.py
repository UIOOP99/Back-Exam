from django.urls import path
from . import views

urlpatterns=[
    path('descriptive-answer/', views.DescriptiveAnswerViewSet.as_view({
        'post': "create",
    })),
    path('multiple-answer/', views.DescriptiveAnswerViewSet.as_view({
        'post': "create",
    })),
    path('file/<int:pk>/', views.MultipleAnswerViewSet.as_view({
        "post": "create_file",
        "get": "get_file_url"})),
]