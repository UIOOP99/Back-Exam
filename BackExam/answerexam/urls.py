from django.urls import path
from . import views

urlpatterns=[
    path('dscriptive_answer/', views.DescriptiveAnswerViewSet.as_view({
        'post': "create",
    })),
    path('file/<int:pk>/', views.DescriptiveAnswerViewSet.as_view({
        "post": "create_file",
        "get": "get_file_url"})),
]