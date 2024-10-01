from django.shortcuts import render, redirect
from app.models import post, Comments, Tag, Profile, WebsiteMeta
from app.forms import commentForm,SubscibeForm,NewUserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login

# Create your views here.

def index(request):
    Posts = post.objects.all()
    top_Posts = post.objects.all().order_by('-views_count')[0:3]
    recent_posts = post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = post.objects.filter(is_featured = True)
    Subscribe_form = SubscibeForm()
    website_info = ''
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]
    
    subscribe_successful = None
    if request.POST:
        Subscribe_form = SubscibeForm(request.POST)
        if Subscribe_form.is_valid:
            Subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_successful = 'subscribed successfully'
            Subscribe_form = SubscibeForm()  # For resetting the form after message print
  
    context = {'posts': Posts, 'top_posts':top_Posts, 'recent_posts':recent_posts, 'Subscribeform':Subscribe_form ,'subscribe_successful':subscribe_successful, 'featured_blog':featured_blog, 'website_info':website_info}
    return render(request, 'app/index.html', context)
    

def post_page(request, slug):
    Posts = post.objects.get(slug=slug)
    comments = Comments.objects.filter(Post=Posts, parent=None)
    form = commentForm()
    
    if request.POST:
        comment_form = commentForm(request.POST)
        if comment_form.is_valid:
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.Post = Posts
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))
   

            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                Postv = post.objects.get(id = postid)
                comment.Post = Postv
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    if Posts.views_count == None:
        Posts.views_count = 1
    else:
        Posts.views_count += 1
    Posts.save()
       
    context = {'post':Posts, 'form':form, 'comments':comments}
    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug = slug)
    
    top_posts = post.objects.filter(tags__in = [tag.id]).order_by('-views_count')[0:2]
    recent_posts = post.objects.filter(tags__in = [tag.id]).order_by('-last_updated')[0:2]
    
    tags = Tag.objects.all()

    context = {'tag':tag, 'top_post':top_posts ,'recent_posts':recent_posts, 'tags':tags}
    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    profile = Profile.objects.get(slug = slug)
    
    top_posts = post.objects.filter(author = profile.user).order_by('-views_count')[0:2]
    recent_posts = post.objects.filter(author = profile.user).order_by('-last_updated')[0:2]
    
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')


    context = {'profile':profile, 'top_post':top_posts ,'recent_posts':recent_posts, 'top_authors':top_authors}
    return render(request, 'app/author.html', context)

def search_post(request):
    search_query = ' '
    if request.GET.get('q'):
        search_query = request.GET.get('q').replace("/",'')
    posts = post.objects.filter(title__icontains = search_query) #icontains is look up for case insensitive search, It is a efficient way.
    context = {'posts':posts, 'search_query':search_query}
    return render(request, 'app/search.html', context)

def about(request):
    website_info = ''
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {'website_info':website_info}
    return render(request, 'app/about.html', context)

def register_user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
      
    context = {'form':form}
    return render(request, 'registration/registration.html', context)
