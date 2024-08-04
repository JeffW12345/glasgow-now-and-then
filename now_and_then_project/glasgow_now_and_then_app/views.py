from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404

from pip._vendor.requests import post

from .models import Picture
from .forms import PictureForm, CommentForm, UserForm


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


# For use with the add_comments facility, which has not been completed.

@login_required
def photo_feed(request):
    if request.method == 'POST':
        if 'add_picture' in request.POST:
            picture_form = PictureForm(request.POST, request.FILES)
            if picture_form.is_valid():
                picture_form.save()
                messages.success(request, 'Picture added successfully!')
                return redirect('nowandthen:photo_feed')
        elif 'add_comment' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(Picture, id=image_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.picture = image
                new_comment.save()
                messages.success(request, 'Thank you for your comment!')
                return redirect('nowandthen:photo_feed')
    else:
        picture_form = PictureForm()
        comment_form = CommentForm()

    pictures = Picture.objects.all()
    return render(request, 'photo_feed.html', {
        'pictures': pictures,
        'picture_form': picture_form,
        'comment_form': comment_form
    })

# For accessing the photo feed.
def photo_feed(request):
    picture_list = Picture.objects.all().order_by('when_added')
    comment_form = CommentForm()

    context_dict = {}
    context_dict['pictures'] = picture_list
    context_dict['comment_form'] = comment_form

    return render(request, 'photo_feed.html', context=context_dict)


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
