from django.db import router
from django.urls import path
from appbackend1.views import RegisterView


#urlpatterns = router.urls
#urlpatterns.append(path('register/', RegisterView.as_view(), name='register'))

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register')
               ]