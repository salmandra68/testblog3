
from operator import imod
import pkgutil
from .models import UserProfileInfo
from django.shortcuts import render,get_object_or_404,redirect
from myblog.forms import UserForm,UserProfileInform
from myblog.models import Post,Comment
from myblog.forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
#afficher tous les articles

class PostListView(ListView):
    model = Post
    
    def get_queryset(self):
        #requette sql: __lte: __ permet d 'ajouter un filtrte à ujn champ /lte :less than equal to ( plus petit que)
        #-published_date: - =DESC
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    


#afficher le detail d un article 
class PostDetailView(DetailView):
    model = Post


#créer un article 
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url= 'login/'
    redirect_field_name='myblog/post_detail.html'
    form_class = PostForm
    model = Post
    
    
#mettre à jour un article 
class UpdatePostView(UpdateView):
    login_url= 'login/'
    redirect_field_name='myblog/post_detail.html'
    form_class = PostForm
    model = Post


#supprimer un article 
class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url =reverse_lazy('myblog:post_list')


##gérer les brouillons
class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name ='myblog/post_list.html'
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    
    
    #############################################
    #########COMMENTAIRES################
    ##################################
    
@login_required    
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('myblog:post_detail',pk=pk)
    
    
@login_required    
def add_comment_to_post(request,pk):
    post =get_object_or_404(Post,pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('myblog:post_detail',pk=post.pk)
    else:
        form = CommentForm
    
    return render (request,'myblog/comment_form.html',{'form':form})       
    


@login_required
def comment_approve(request,pk):
    comment =get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect ('myblog:post_detail',pk=comment.post.pk)



@login_required    
def comment_remove(request,pk):
    comment =get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('myblog:post_detail',pk=post_pk)


# def register(request):
#     registered=False
    
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form =UserProfileInform(data=request.POST)
        
#         if user_form.is_valid() and profile_form.is_valid():
#             #sauvegarde dans le BDD
#             user = user_form.save() 
#             #cryptage MDP
#             user.set_password(user.password)
#             #sauvegarde MDP
#             user.save()
            
#             #donnée du profile 
#             profile = profile_form.save(commit=False)
#             #relie les 2 formulaires ( One to One)
#             profile.user = user
#             #avatar ok ou non 
#             if 'avatar' in request.FILES:
#                 profile.avatar = request.FILES['avatar']
#                #sauvegarde avatar
#             profile.save()
#             #tout ets ok dans la BDD +> registeree true
#             registered = True
#         else: #on affiche les erreurs
#             print(user_form.errors,profile_form.errors)            
#     else:
#         user_form=UserForm()
#         profile_form=UserProfileInform()    
        
#     return render(request,'myblog/register.html',{'user_form':user_form,'profile_form':profile_form})    
        
# def user_login(request):
#     if request.method =='POST':
        
#         username = request.POST.get('username')
#         password=request=request.POST.get('password')
    
#         #poiur authentifier l utilisateur 
#         user = authenticate(username=username,password=password)
    
#         if user:
#         #on verifie que le compte soit actif
#             if user.is_active:
#         #pn le logue 
#                 login(request,user)
#         #on le redirige 
#                 return HttpResponseRedirect(reverse('myblog:post_list'))

#             else:
#                 return HttpResponse("Le compte n'\est pas actif") 
#         else: 
#             print('Un individu a essayé de se connecter et a échoué')  
#             print('Pseudo: {} et mdp : {}'.format(username,password)) 
#             return HttpResponse('Information invalides') 
#     else:
#         return render(request,'myblog/login.html',{})                      
    
def register (request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("myblog:post_list")
		
	form = UserForm()
	return render (request=request, template_name="myblog/register.html", context={"register_form":form}) 
    
def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')

			password = form.cleaned_data.get('password')
         
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("myblog:post_list")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="myblog/login.html", context={"login_form":form})    
    
    
    
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myblog:post_list'))