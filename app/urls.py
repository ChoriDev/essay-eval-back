from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import Evaluator

# APIView로 구현한 CURD에 대한 URL
urlpatterns = [
    path('result/', Evaluator.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)