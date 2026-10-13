from django.urls import path

from tracker.views import SignUpView,GetMeView
from tracker.views import FoodlogCreateListView,FoodlogRetrieveUpdateDeleteView
from tracker.views import FoodlogSummaryView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin-register/',SignUpView.as_view()),
    path('getme/',GetMeView.as_view()),
    
    path('foodlogs/',FoodlogCreateListView.as_view()),
    path('foodlogs/<int:pk>/',FoodlogRetrieveUpdateDeleteView.as_view()),
    path('foodlogs/summary/',FoodlogSummaryView.as_view()),

    path('token/',ObtainAuthToken.as_view())
    
    
]