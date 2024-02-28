from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Entry
from django import forms



class EntryFrom(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content']

@login_required
def home(request):
    username = request.user.username
    query = f"SELECT * FROM diary_entry WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
    with connection.cursor() as cursor:
        cursor.execute(query)
        entry = cursor.fetchall()
    
    if request.method == 'POST':
        form = EntryFrom(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.user = request.user
            new_entry.save()
            return redirect('/') 
    else:
        form = EntryFrom()

    return render(request, 'diaryPage.html', {'diary':entry, 'form': form})

@login_required
@csrf_exempt
def edit(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    if request.method == 'POST':
        form = EntryFrom(request.POST, instance=entry)
        if form.is_valid():
            edited_entry = form.save(commit=False)
            edited_entry.user = request.user
            edited_entry.save()
            return redirect('/')
    else:
        form = EntryFrom(instance=entry)

    context = {
        'entry': entry,
        'form': form    
    }
    return render(request, 'registration/edit.html', context)

@login_required
@csrf_exempt
def delete(request, entry_id):
    entry=Entry.objects.get(pk=entry_id)
    entry.delete()
    return redirect('/')
