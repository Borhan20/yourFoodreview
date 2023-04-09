from django.shortcuts import render, redirect
from .forms import MessageForm
from django.contrib import messages

def submit_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'your message has been set. Thanks to you to co-operate with us.')
            return redirect('blog-home')
    else:
        form = MessageForm()
    return render(request, 'usermessage/submit_message.html', {'message_form': form})
