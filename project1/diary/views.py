from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#FLAW 1 fix: import 'csrf_protect' to enable protection (from django.views.decorators.csrf import csrf_protect)
#FLAW 4 fix: imports
#from django.core.exceptions import ValidationError
#from django.contrib.auth.password_validation import validate_password
from .models import Entry
from django import forms


class EntryFrom(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content']

@login_required
@csrf_exempt
#FLAW 1: switch 'csrf_exempt' to 'csrf_protect' (@csrf_project)
def home(request):
    username = request.user.username
    query = f"SELECT * FROM diary_entry WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
    with connection.cursor() as cursor:
        cursor.execute(query)
        entry = cursor.fetchall()
        #FLAW 3: SQL injection
        #diary = Enty.objects.filter(user=request.user)
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
#FLAW 1: switch 'csrf_exempt' to 'csrf_protect' (@csrf_project)
def edit(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    #FLAW 2: Broken access Control
    #chech if the logged in user has written the diary entrys before allowing edits to be made
    #if entry.user != request.user:
    #return HttpResposse("You don't have the authorications to edit this enty")
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
#FLAW 1: switch 'csrf_exempt' to 'csrf_protect' (@csrf_project)
def delete(request, entry_id):
    entry=Entry.objects.get(pk=entry_id)
    entry.delete()
    return redirect('/')

#FLAW 4: Identification and Authentication Failures
#Create a registration function to awoid weak or common passwords. 
# def registration(username, password):
#     try:
#         validate_password(password)
#         user = User.objects.create_user(username=username, password=password)
#         return user
#     except ValidationError as e:
#         print("Error in validating your password:", e.messages)
#         return None