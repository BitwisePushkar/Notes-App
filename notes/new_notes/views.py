from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import Notes 
from .forms import NotesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model=Notes
    success_url = reverse_lazy('notes.list')
    login_url = reverse_lazy('login')
    template_name = "notes_delete.html"
        
    def get_queryset(self):
        return self.request.user.notes.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = context['object'] 
        return context

class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model=Notes
    success_url = reverse_lazy('notes.list')
    login_url = reverse_lazy('login')
    form_class=NotesForm
    template_name = "notes_form.html"
    
    def get_queryset(self):
        return self.request.user.notes.all()
    
class NotesCreateView(LoginRequiredMixin, CreateView):
    model=Notes
    success_url='/smart/notes/'
    form_class=NotesForm
    template_name = "notes_form.html"
    login_url="/login"

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user =self.request.user 
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesList(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes_list.html"
    login_url="/login"

    def get_queryset(self):
        return self.request.user.notes.all()

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = 'notes_details.html' 
    context_object_name = 'note'
    login_url="/login"

    def get_queryset(self):
        return self.request.user.notes.all()
