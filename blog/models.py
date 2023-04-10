from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_images = models.ImageField(default='pizza.jpg',upload_to = 'post_images')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

    
    def save(self, *args, **kwargs):
        super(Post,self).save(*args,**kwargs)

        img = Image.open(self.post_images.path)

        if img.height > 400 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.post_images.path)
         
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    



