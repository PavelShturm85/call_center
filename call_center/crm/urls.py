from django.urls import path

from . import views

urlpatterns = [
    path('call/', views.call_list, name='calls_list'),
    path('activity/', views.activity_users, name='activity_users'),
    path('new_call/', views.call_update, name='call_update'),
    path('call/edit/<pk>/', views.CallEdit.as_view(), name='call_edit'),
    path('choice_phone/', views.PhoneNumberChoice.as_view(), name='choice_phone'),
    path('call/edit/<pk>/log', views.LogCallList.as_view(), name='log_call'),
]
