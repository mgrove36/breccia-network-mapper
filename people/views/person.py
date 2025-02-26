"""
Views for displaying or manipulating instances of :class:`Person`.
"""

import typing

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from people import forms, models, permissions
from .map import get_map_data


class PersonCreateView(LoginRequiredMixin, CreateView):
    """View to create a new instance of :class:`Person`.

    If 'user' is passed as a URL parameter - link the new person to the current user.
    """
    model = models.Person
    template_name = 'people/person/create.html'
    form_class = forms.PersonForm

    def form_valid(self, form):
        if 'user' in self.request.GET:
            form.instance.user = self.request.user

        return super().form_valid(form)


class PersonListView(LoginRequiredMixin, ListView):
    """View displaying a list of :class:`Person` objects - searchable."""
    model = models.Person
    template_name = 'people/person/list.html'

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)

        existing_relationships = set()
        try:
            existing_relationships = set(
                self.request.user.person.relationships_as_source.filter(
                    answer_sets__replaced_timestamp__isnull=True
                ).values_list('target_id', flat=True)
            )

        except ObjectDoesNotExist:
            # No linked Person yet
            pass

        context['existing_relationships'] = existing_relationships

        return context


class ProfileView(LoginRequiredMixin, DetailView):
    """View displaying the profile of a :class:`Person` - who may be a user."""
    model = models.Person

    def get(self, request: HttpRequest, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        try:
            self.object = self.get_object()  # pylint: disable=attribute-defined-outside-init

        except ObjectDoesNotExist:
            # User has no linked Person yet
            return redirect('index')

        if self.object.user == self.request.user and self.object.current_answers is None:
            return redirect('people:person.update', pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_template_names(self) -> typing.List[str]:
        """Return template depending on level of access."""
        if (self.object.user == self.request.user) or self.request.user.is_superuser:
            return ['people/person/detail_full.html']

        return ['people/person/detail_partial.html']

    def get_object(self, queryset=None) -> models.Person:
        """Get the :class:`Person` object to be represented by this page.

        If not determined from url get current user.
        """
        try:
            return super().get_object(queryset)

        except AttributeError:
            # pk was not provided in URL
            return self.request.user.person

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        """Add current :class:`PersonAnswerSet` to context."""
        context = super().get_context_data(**kwargs)

        answer_set = self.object.current_answers
        context['answer_set'] = answer_set
        context['map_markers'] = [get_map_data(self.object)]

        context['question_answers'] = {}
        if answer_set is not None:
            show_all = (self.object.user == self.request.user) or self.request.user.is_superuser
            context['question_answers'] = answer_set.build_question_answers(show_all)

        context['relationship'] = None
        try:
            relationship = models.Relationship.objects.get(
                source=self.request.user.person, target=self.object
            )

            if relationship.is_current:
                context['relationship'] = relationship

        except models.Relationship.DoesNotExist:
            pass

        return context


class PersonUpdateView(permissions.UserIsLinkedPersonMixin, UpdateView):
    """View for updating a :class:`Person` record."""
    model = models.Person
    context_object_name = 'person'
    template_name = 'people/person/update.html'
    form_class = forms.PersonAnswerSetForm

    def get(self, request: HttpRequest, *args: str, **kwargs: typing.Any) -> HttpResponse:
        self.object = self.get_object()

        try:
            if (self.object.user == self.request.user) and not self.request.user.consent_given:
                return redirect('consent')

        except AttributeError:
            # No linked user
            pass

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)

        context['map_markers'] = [get_map_data(self.object)]

        return context

    def get_initial(self) -> typing.Dict[str, typing.Any]:
        try:
            previous_answers = self.object.current_answers.as_dict()

        except AttributeError:
            previous_answers = {}

        previous_answers.update({
            'person_id': self.object.id,
        })

        return previous_answers

    def get_form_kwargs(self) -> typing.Dict[str, typing.Any]:
        """Remove instance from form kwargs as it's a person, but expects a PersonAnswerSet."""
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance')

        return kwargs

    def form_valid(self, form):
        """Mark any previous answer sets as replaced."""
        response = super().form_valid(form)
        now_date = timezone.now().date()

        # Saving the form made self.object a PersonAnswerSet - so go up, then back down
        # Shouldn't be more than one after initial updates after migration
        for answer_set in self.object.person.answer_sets.exclude(pk=self.object.pk):
            answer_set.replaced_timestamp = now_date
            answer_set.save()

        return response
