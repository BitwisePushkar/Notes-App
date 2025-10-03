from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView
from .models import Notes 
from .forms import NotesForm


class NotesCreateView(CreateView):
    model=Notes
    success_url='/smart/notes/'
    form_class=NotesForm
    template_name = "notes_form.html"


class NotesList(ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes_list.html"

class NoteDetailView(DetailView):
    model = Notes
    template_name = 'notes_details.html' 
    context_object_name = 'note'