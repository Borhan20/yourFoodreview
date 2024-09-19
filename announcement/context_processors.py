from django import forms
from .models import Announcement
from django.core.paginator import Paginator


def message_processor(request):
    

    
    announcement = Announcement.objects.all()
    paginator = Paginator(announcement, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return {
        'announcement' : page_obj
        
    }