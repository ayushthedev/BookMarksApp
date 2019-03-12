from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile,Contact
from django.contrib import messages
from django.contrib.auth.models import User
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from actions.models import Action
from actions.utils import create_action


def home_page(request):
    if request.user.is_authenticated:
        return dashboard(request)
    else:
        return redirect('login')

def user_login(request):
    if request.method == 'POST':
        "_____________________________________________________________"
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(user=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        print('***********************************************')
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})




@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.all().exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    actions = actions[:10]

    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})



@login_required
def edit(request):
    print('______________________User_______________________',request.user.profile.photo.url)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'photo': request.user.profile.photo.url})


def register(request):
    if request.method == 'POST':
        print('_______________________________We are posting______________')
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)

        return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people',
                                                      'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user': user})
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                print('_______________________________________________----')
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})