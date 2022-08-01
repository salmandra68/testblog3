from distutils.command.upload import upload
from shutil import register_unpack_format
from django.utils import timezone
from django.utils import timezone
from django.contrib.auth.models import User


from django.db import models
from django.urls import reverse


# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars',blank=True)
    
    def __str__(self):
        return self.user.username





class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    text=models.TextField()
    post_pic= models.ImageField(upload_to='post_pic',blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
        
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
     
    def get_absolute_url(self):
        return reverse('myblog:post_detail',kwargs={'pk':self.pk})
     

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey('Post',related_name="comments",on_delete=models.CASCADE)
    author =models.CharField(max_length=200)
    text =models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment =models.BooleanField(default=False)
    
    
    def approve(self):
        self.approved_comment=True
        self.save()
    
    def get_absolute_url(self):
        return reverse('post_list')
    
    
    
    def __str__(self):
        return self.text
      
        
    
            
    