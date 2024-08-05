from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404

from pip._vendor.requests import post

from .models import Picture, Comment, PictureLike
from .forms import PictureForm, CommentForm, UserForm, PictureLikeForm


# For accessing the index page
def index(request):
    context_dict = {}
    return render(request, 'index.html', context=context_dict)


# For user registration
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = user_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                  'register.html',
                  context={'user_form': user_form,
                           'registered': registered})


# For user logins
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('nowandthen:index'))
            else:
                return HttpResponse("Your nowandthen account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html')


# For adding pictures.
@login_required
def add_picture(request):
    form = PictureForm()
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('index'))
        else:
            print(form.errors)
    return render(request, 'templates/add_picture.html', {'form': form})


def photo_feed(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                image_id = form.cleaned_data['image_id']
                image = get_object_or_404(Picture, id=image_id)
                comment.image = image
                comment.user = request.user
                comment.save()

        elif 'add_like' in request.POST:
            form = PictureLikeForm(request.POST)
            if form.is_valid():
                image_id = form.cleaned_data['image_id']
                user_id = form.cleaned_data['user_id']

                # Check if the user has already liked this image
                if not PictureLike.objects.filter(image_id=image_id, user_id=user_id).exists():
                    like = form.save(commit=False)
                    image = get_object_or_404(Picture, id=image_id)
                    like.image = image
                    like.user = request.user
                    like.save()

    # Always fetch pictures to display
    pictures = Picture.objects.all()

    # Initialize forms for GET requests or rendering forms on the page
    comment_form = CommentForm()
    picture_like_form = PictureLikeForm()
    picture_likes = PictureLike.objects.all()

    return render(request, 'photo_feed.html', {
        'pictures': pictures,
        'comment_form': comment_form,
        'picture_like_form': picture_like_form,
        'picture_likes': picture_likes
    })
# For accessing the 1970s photo feed (functionality not completed)
def photo70(request):
    picture_list_70 = Picture.objects.filter(era=1970)

    context_dict = {}
    context_dict['pictures70'] = picture_list_70

    return render(request, '1970.html', context=context_dict)


# For accessing the 1980s photo feed (functionality not completed)
def photo80(request):
    picture_list_80 = Picture.objects.filter(era=1980)

    context_dict = {}
    context_dict['pictures80'] = picture_list_80

    return render(request, '1980.html', context=context_dict)


# For accessing the 2010s photo feed (functionality not completed)
def photo10(request):
    picture_list_10 = Picture.objects.filter(era=2010)

    context_dict = {}
    context_dict['pictures10'] = picture_list_10

    return render(request, '2010.html', context=context_dict)


# For search results (functionality not completed)
def search_results(request):
    return render(request, 'search_results.html')


# For logging out.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('templates:index'))
