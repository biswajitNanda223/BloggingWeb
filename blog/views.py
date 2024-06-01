from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
def blogHome(request):
    allPost=Post.objects.all()
    print(allPost)
    context={'allposts':allPost}
    # return HttpResponse("This is blogHome . we will keep all the blog posts here ")
    return render(request,'blog/blogHome.html',context)

# def blogPost(request,slug):
#       post = Post.objects.filter(slug=slug).first()
#       context={'post':post}
#     # return HttpResponse(f"This is blogPost : {slug}")
#       return render(request,'blog/blogPost.html',context)
def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post)
    context={'post':post, 'comments': comments, 'user': request.user,}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        comment=BlogComment(comment= comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")