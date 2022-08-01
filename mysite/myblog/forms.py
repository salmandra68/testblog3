from django import forms
from myblog.models import Post,Comment
from django.contrib.auth.models import User
from myblog.models import UserProfileInfo

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text','post_pic')
        widgets={
            'author':forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text' : forms.Textarea(attrs={'class':'form-control'}),
            #'post_pic':forms.ImageField()    
            }
    
class CommentForm(forms.ModelForm):
    class Meta():
        model =Comment 
        fields=('author','text')
        widgets={
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control'}), 
        }    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    fields=('avatar',)  
    
    class Meta():
        model = User
        fields=('username','email','password')


class UserProfileInform(forms.ModelForm):
    class Meta():
        model =UserProfileInfo
        fields=('avatar',)    