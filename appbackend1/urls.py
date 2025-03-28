from django.urls import path
from appbackend1.views import RegisterView, LoginView
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns.append(path('register/', RegisterView.as_view(), name='register'))
urlpatterns.append(path('login/', LoginView.as_view(), name='login'))