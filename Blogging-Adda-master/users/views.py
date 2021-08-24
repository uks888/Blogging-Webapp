from django.shortcuts import render, redirect
from .form import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! Now you can login')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # userform m details filled hokar aayegi
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # profile form m details filled hokar aayegi
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def forgot_pass(request):

    if request.method == "POST":
        # Handle and send reset email if email is valid

        email = request.POST['email']

        # if email exists
        send_mail(
            'Password Reset',
            'Reset your password from here',
            'princepraa@gmail.com',
            ['email'],
            fail_silently=False,
        )
    else:
        # render form
        return render(request, 'users/password_reset.html')


