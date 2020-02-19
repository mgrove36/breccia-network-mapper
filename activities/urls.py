from django.urls import path

from . import views


app_name = 'activities'

urlpatterns = [
    path('activity-series',
         views.ActivitySeriesListView.as_view(),
         name='activity-series.list'),

    path('activity-series/<int:pk>',
         views.ActivitySeriesDetailView.as_view(),
         name='activity-series.detail'),

    path('activities',
         views.ActivityListView.as_view(),
         name='activity.list'),

    path('activities/<int:pk>',
         views.ActivityDetailView.as_view(),
         name='activity.detail'),
]
