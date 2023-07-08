from django.urls import path

from . views import (Dashboard, ManageUsers,FillForm,
                     AccusedList, DeleteAccused, UpdateAccusedStatus, 
                     TrackAccusedView, AccusedDetailView, SearchResult)

app_name = 'malpractice'
urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard"),
    path('manage-users/', ManageUsers.as_view(), name="manage_users"),
    path('fill-form/', FillForm.as_view(), name="fill_form"),
    path('accused-list/', AccusedList.as_view(), name="accused_list"),
    path('accused-list/delete/<str:pk>/', DeleteAccused.as_view(), name="delete_accused"),
    path('accused-list/update/<str:pk>/', UpdateAccusedStatus.as_view(), name="update_accused"),
    path('track-accused/', TrackAccusedView.as_view(), name="track_accused"),
    path('accused-detail/<str:pk>/', AccusedDetailView.as_view(), name="accused_detail"),
    path('search/', SearchResult.as_view(), name="search_accused"),
]
