from django.urls import path 

from diary.views import home, edit, delete, signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', home, name='home'),
    path('edit/<int:entry_id>', edit, name='edit'),
    path('delete/<int:entry_id>/', delete, name='delete')
]