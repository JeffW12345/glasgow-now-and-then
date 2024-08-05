from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Picture, PictureLike, ImageTag
from .forms import PictureForm, CommentForm, UserForm, PictureLikeForm, ImageTagForm


def index(request):
    context_dict = {}
    return render(request, 'index.html', context=context_dict)

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

@login_required
def add_picture(request):
    PictureTagFormSet = modelformset_factory(ImageTag, form=ImageTagForm, extra=3)  # Adjust the extra parameter as needed
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        formset = PictureTagFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            for form in formset:
                if form.cleaned_data:
                    tag = form.save(commit=False)
                    tag.picture = picture
                    tag.save()
            return redirect(reverse('nowandthen:index'))
        else:
            print(form.errors, formset.errors)
    else:
        form = PictureForm()
        formset = PictureTagFormSet(queryset=ImageTag.objects.none())
    return render(request, 'add_picture.html', {'form': form, 'formset': formset})

@login_required
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

                if not PictureLike.objects.filter(image_id=image_id, user_id=user_id).exists():
                    like = form.save(commit=False)
                    image = get_object_or_404(Picture, id=image_id)
                    like.image = image
                    like.user = request.user
                    like.save()

    pictures = Picture.objects.all()

    comment_form = CommentForm()
    picture_like_form = PictureLikeForm()
    picture_likes = PictureLike.objects.all()

    tags = ImageTag.objects.all()

    return render(request, 'photo_feed.html', {
        'pictures': pictures,
        'comment_form': comment_form,
        'picture_like_form': picture_like_form,
        'picture_likes': picture_likes,
        'tags': tags,
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


def search_results(request):
    return render(request, 'search_results.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')
