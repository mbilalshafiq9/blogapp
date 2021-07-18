from django.shortcuts import redirect, render

# Create your views here.
from django.db.models import Count
from datetime import datetime
from home.models import Blog, Category, Comment
from django.contrib import messages
from django.contrib.auth import authenticate,login as authlogin,logout as authlogout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives
# Create your views here.
# Home Page
def index(request):
    context={
        "blogs":Blog.objects.all().order_by('-id')[:3][::-1],
        "post1":Blog.objects.all()[0],
        "post2":Blog.objects.all()[1],
        "post3":Blog.objects.all()[2] 
    }
    return render(request,"index.html",context)

def forgot_pass(request):
    if request.GET['email']:
        email=request.GET['email']
    email=request.POST['email']
    find_user=User.objects.filter(email=email)
    body='<h3>Hi, Click on the following link to reset. <br> <a href="http://127.0.0.1:8000/reset_password?email='+email+'&pass='+find_user[0].password+'">Click Here</a> Dont Share this link with anyone. Thanks</h3> <br><h4> Best Regards: Blog to Glob</h4>'
    if find_user:
        msg=EmailMultiAlternatives('Reset Password Link',body,'Blog to Glob',[email])
        msg.attach_alternative(body, "text/html")
        msg.send()
        messages.success(request, 'Password Reset link is sent to your mail Sucessfully.')
        return render(request,"login.html")
    else:
        messages.error(request, 'Email is not registered. Type Carefully!')
        return render(request,"login.html")

def reset_pass(request):
    if request.method=='GET':
        email=request.GET['email']
        password=request.GET['pass']
        user=User.objects.filter(email=email,password=password)
        if user:
            messages.error(request, 'Email is not registered. Type Carefully!')
            return render(request,"login.html")
    messages.error(request, 'Email is not registered. Type Carefully!')
    return render(request,"login.html")

# Blog Page
def blog(request):
    blog_list=Blog.objects.filter().annotate(comment_count=Count('blog')).order_by('-id')
    categories = Category.objects.all().annotate(posts_count=Count('cat'))
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 4)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    
    return render(request,"blogs.html",{ 'blogs': blogs,'categories':categories,})

def post(request,id):
    if request.method=="POST":
        uid=request.POST['user']
        user=User.objects.get(id=uid)
        blogid=request.POST['blog']
        blog=Blog.objects.get(id=blogid)
        comment=request.POST['comment']
        comment =Comment(user=user, blog=blog,comment=comment,parent=0)
        comment.save()
        messages.success(request, 'Comment is Posted Sucessfully.')
    post=Blog.objects.get(id=id)
    comments=Comment.objects.filter(blog=post)
    blogs=Blog.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('cat'))
    return render(request,"blog_post.html",{ 'post': post,'comments': comments,'categories': categories,'blogs': blogs,})

def dashboard(request):
    return render(request,"dashboard/dashboard.html")

def search(request):
    query=request.GET['query']
    context={
        "query":request.GET['query'],
        "blogs":Blog.objects.filter(title__icontains=query).annotate(comment_count=Count('blog')),
        "categories" :Category.objects.all().annotate(posts_count=Count('cat')),
    }

    return render(request,"search.html",context)

def dashboard_blogs(request):
    context={
        "blogs":Blog.objects.all(),

    }
    return render(request,"dashboard/blogs.html",context)
# User Dashboard
def dashboard_addblog(request):
    if request.method=="POST":
        title=request.POST['title']
        categoryid=request.POST['category']
        category=Category.objects.get(id=categoryid)
        image=request.FILES.get('image', 'images/blog-1.jpg')
        content=request.POST['content']
        authorid=request.POST['author']
        author=User.objects.get(id=authorid)
        blog =Blog(title=title, category=category,image=image,content=content,author=author)
        blog.save()
        messages.success(request, 'Blog Added.')
    context={
        "category":Category.objects.all(),
    }
    return render(request,"dashboard/add_blog.html",context)

def edit_blog(request,id):
    if request.method=="POST":
        blog = Blog.objects.get(id=id) 
        blog.title=request.POST['title']
        categoryid=request.POST['category']
        blog.category=Category.objects.get(id=categoryid)
        blog.image = request.FILES.get('image', blog.image)
        blog.content=request.POST['content']
        authorid=request.POST['author']
        blog.author=User.objects.get(id=authorid)
        blog.save()  
        messages.warning(request, 'Blog is Updated Successfully')
        return redirect("/dashboard/blogs") 
    context={
       "blog" : Blog.objects.get(id=id),
       "category": Category.objects.all(),
    }
    return render(request,"dashboard/edit_blog.html",context)

def delete_blog(request,id):
    blog = Blog.objects.get(id=id)  
    blog.delete()  
    messages.error(request, 'Blog is Deleted!')
    return redirect("/dashboard/blogs")

def dashboard_profile(request):
    if request.method=="POST":
        uid=request.POST['uid']
        user = User.objects.get(id=uid) 
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.save()
        messages.warning(request, 'Profile is Updated!')
        return redirect("/dashboard/profile")
    return render(request,"dashboard/profile.html")

def change_pass(request):
    if request.method=="POST":
        old_pass=request.POST['old_pass']
        old_pass=request.POST['old_pass']
        old_pass=request.POST['old_pass']
        messages.warning(request, 'Password is Updated!')
        return redirect("/dashboard/profile")

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username, password=password)
        if user is not None:
            authlogin(request,user)
            messages.success(request, 'Your are login Successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid login Details. Please Try Again!')
            return redirect('login')
    return render(request,"login.html")

def logout(request):
    authlogout(request)
    messages.warning(request, 'Your are logout successfully')
    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        #check fields
        if len(username)<6 or not username.isalnum():
            messages.error(request, 'Username must contain 6 or more Letters and numerbers')
            return redirect('register')
        if pass1!=pass2:
            messages.error(request, 'Password and Confirm pass  does not match')
            return redirect('register')
        nuser =User.objects.create_user(username,email,pass1)
        nuser.first_name=fname
        nuser.last_name=lname
        nuser.save()
        messages.success(request, 'Your Account is created sucessfully.')
    
    return render(request,"register.html")

# def contact(request):
#     if request.method=="POST":
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         message=request.POST.get('message')
#         contact =Contact(name=name, email=email,message=message,date=datetime.today())
#         contact.save()
#         messages.success(request, 'Your message is sent succesfully.')
#     return render(request,"contact.html")
