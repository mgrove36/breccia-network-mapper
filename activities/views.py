"""
Views for displaying / manipulating models within the Activities app.
"""
from django.views.generic import DetailView, ListView

from . import models


class ActivitySeriesListView(ListView):
    """
    View displaying a list of :class:`ActivitySeries`.
    """
    model = models.ActivitySeries
    template_name = 'activities/activity_series/list.html'
    context_object_name = 'activity_series_list'


class ActivitySeriesDetailView(DetailView):
    """
    View displaying details of a single :class:`ActivitySeries`.
    """
    model = models.ActivitySeries
    template_name = 'activities/activity_series/detail.html'
    context_object_name = 'activity_series'


class ActivityListView(ListView):
    """
    View displaying a list of :class:`Activity`.
    """
    model = models.Activity
    template_name = 'activities/activity/list.html'
    
    
class ActivityDetailView(DetailView):
    """
    View displaying details of a single :class:`Activity`.
    """
    model = models.Activity
    template_name = 'activities/activity/detail.html'
