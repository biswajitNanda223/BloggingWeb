from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def home(request):
    # messages.error(request, "Document deleted.")
    # return HttpResponse("This is Home Page")
    allPost=Post.objects.all()
    print(allPost)
    context={'allposts':allPost}
    return render(request,'home/home.html',context)
def contact(request):
    #  messages.success(request,'Welcome to Contact')
    # messages.warning(request, "Your account expires in three days.")
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        # print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form Correctly !")
        else:         
         contact=Contact(name=name,email=email,phone=phone,content=content)
         contact.save()
         messages.success(request,"Your Message has been succesfully sent ! ")
    # return HttpResponse("This is contact Page")
    return render(request,'home/contact.html')
def about(request):
    # return HttpResponse("This is about Page")
         return render(request,'home/about.html')


def search(request):
    query=request.GET['query']
    if len(query)>78:
        # allPosts=[]
        allPosts=Post.objects.none()
    # allPosts=Post.objects.all()
    else:
     allPostsTitle=Post.objects.filter(title__icontains = query)
     allPostsContent=Post.objects.filter(content__icontains = query)
     allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
      messages.warning(request, "No search Results Found")
    params={'allposts':allPosts , 'query':query}
    # return HttpResponse("This is a search Page")
    return render(request,'home/search.html',params)

def handleSignup(request):    
    if request.method == 'POST':
        # get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
    # check for errorneous input
        if pass1 != pass2 or len(username)>10:
         messages.error(request,"Your pass doesnot match or username doesnot match")
         return redirect('home')
        if not username.isalnum():
         messages.error(request,"Your UserName Must be AlphaNumeric")
         return redirect('home')
    #Create the user]
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your Acccount has been successfuly Created")
        return redirect('home')

    else:
        return HttpResponse('404- Not Found')
    
def handleLogin(request):
   Loginusername=request.POST['Loginusername']
   Loginpassword=request.POST['Loginpassword']
   user=authenticate(username=Loginusername,password=Loginpassword)
   if user is not None:
      login(request,user)
      messages.success(request,"Congrats ! Login Successfull")
      return redirect('home')
   else:
      messages.error(request,"Invalid Credentials, please Try Again")
      return redirect('home')
   
    # return HttpResponse('404- Not Found')   

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Successfull")
    return redirect('home')

    # return HttpResponse('404- Not Found')