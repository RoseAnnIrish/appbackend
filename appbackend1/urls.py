from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, RegisterView, LoginView, LogoutView

# Initialize router for Todo API
router = DefaultRouter()
router.register(r'todo', TodoViewSet)

# Define URL patterns
urlpatterns = [
    path('todo/', include(router.urls)),  # Include Todo URLs
    path('register/', RegisterView.as_view(), name='register'),  # Register route
    path('login/', LoginView.as_view(), name='login'),  # Login route
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout route
]
