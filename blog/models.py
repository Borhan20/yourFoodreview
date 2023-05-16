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

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
    
    def get_likes_count(self):
        return self.likes.count()
    
    # def get_last_comment(self):
    #     last_comment = self.comments.filter(parent=None).order_by('-date_added').first()
    #     #print(last_comment)
    #     return last_comment
    

    
    def save(self, *args, **kwargs):
        super(Post,self).save(*args,**kwargs)

        img = Image.open(self.post_images.path)

        if img.height > 400 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.post_images.path)
         
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    parent = models.ForeignKey('self', null=True,blank=True,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.body
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
         
    
class About(models.Model):
    about_text = models.TextField()

    def __str__(self):
        return self.about_text