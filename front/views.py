# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.views.generic import FormView, TemplateView

import allauth.account.views
import forms


class SignupView(allauth.account.views.SignupView):

    def get_success_url(self):
        return reverse('cyclist_account_signup_complete',
                       kwargs={'role': self.kwargs.get('role')})

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        self.request.user.cyclist.role = self.kwargs.get('role')
        self.request.user.cyclist.save()
        return response


class SignupCompleteView(LoginRequiredMixin, TemplateView):
    success_url = '/'

    def get_template_names(self):
        role = self.kwargs.get('role')

        if role == 'volunteer':
            return ['bikeanjo_complete_signup.html']


class TrackRegisterView(LoginRequiredMixin, FormView):
    template_name = 'bikeanjo_routes_register_form.html'
    form_class = forms.TrackForm

    def get_success_url(self):
        return reverse('registered_tracks')

    def form_valid(self, form):
        form.save(cyclist=self.request.user.cyclist)
        return super(TrackRegisterView, self).form_valid(form)


class TrackListView(LoginRequiredMixin, TemplateView):
    template_name = 'bikeanjo_routes_list.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(TrackListView, self).get_context_data(**kwargs)
        context['form'] = True
        return context


class HomeView(TemplateView):
    template_name = 'home.html'
