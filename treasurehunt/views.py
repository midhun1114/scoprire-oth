from django.shortcuts import render,redirect
from . import forms
# Create your views here.
from treasurehunt import models
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from .forms import ProfileForm
import time
from termcolor import colored


def prfile_page(request):
    if request.method=="POST":
        if not models.userProfile.objects.filter(user=request.user):
            models.userProfile.objects.create(user=request.user, college = request.POST["college"], phone_number = request.POST["phone_number"])
        return redirect("/")

    return render(request,""'treasurehunt/profile.html',{"form":ProfileForm()})

def index(request):
    score = 0
    current_user = request.user
    current_user1 = str(current_user)

    if (current_user1 == "AnonymousUser"):
        return render(request, 'treasurehunt/index.html')

    else:
        if not models.userProfile.objects.all().filter(user=current_user):
            return redirect("profile_complete/")
        try:

            sc = models.Score.objects.get(user__exact=current_user)
            score = sc.score
        except:
            score = models.Score()
            score.user = current_user
            score.save()
            sc = models.Score.objects.get(user__exact=current_user)
            score = sc.score
        return render(request, 'treasurehunt/index.html', {'score': sc.score})


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('treasurehunt:question'))
    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        if user_form.is_valid():
            passmain = user_form.cleaned_data['password']
            passverify = user_form.cleaned_data['confirm_password']
            if passmain == passverify:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                score = models.Score()
                score.user = user
                score.save()

                registered = True
            else:
                return HttpResponse("Password Don't Match")
        else:
            print(user_form.errors)
    else:
        user_form = forms.UserForm()

    return render(request, 'treasurehunt/signup.html', {
        'user_form': user_form,
        'registered': registered
    })


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('treasurehunt:question'))
    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        if user_form.is_valid():
            passmain = user_form.cleaned_data['password']
            passverify = user_form.cleaned_data['confirm_password']
            if passmain == passverify:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                score = models.Score()
                score.user = user
                score.save()

                registered = True
            else:
                return HttpResponse("Password Don't Match")
        else:
            print(user_form.errors)
    else:
        user_form = forms.UserForm()

    return render(request, 'treasurehunt/signup.html', {
        'user_form': user_form,
        'registered': registered
    })


# def user_login(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('treasurehunt:question'))
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('treasurehunt:question'))
#             else:
#                 return HttpResponse("ACCOUNT NOT ACTIVE")
#         else:
#             print("Someone tried to login and failed")
#             print("UserName : {} and password {} ".format(username, password))
#             messages.error(request, "Invalid Login Details!")
#             return render(request, 'treasurehunt/login.html')
#     else:
#         return render(request, 'treasurehunt/login.html')

def invalid_login(request):
    return render(request, 'treasurehunt/invalidlogin.html')


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('treasurehunt:index'))


@login_required
def question(request):
    if not models.userProfile.objects.all().filter(user=request.user):
        return redirect("/profile_complete/")
#     ama.jpg
    question_fixed = [
        'coming.jpg', 'ana.jpg', 'nth.jpg', 'mid.jpg', 'ala.jpeg',
        'and.jpg', 'mhd.jpg','shf.jpeg', 'nsh.jpg', 'pry.jpeg',
        'anj.png','nna.png', 'sru.png', 'iry.jpg', 'ren.jpeg',
        'aar.png', 'any.jpeg', 'scr.jpeg','dac.png', 'nat.jpg',
        'kat.jpeg','leo.jpeg', 'kev.jpg', 'rob.jpeg','clo.jpeg']

    current_user = request.user
    try:
        sc = models.Score.objects.get(user__exact=current_user)
    except:
        score = models.Score()
        score.user = current_user
        score.save()
        sc = models.Score.objects.get(user__exact=current_user)
    try:
        ans_fixed = models.AnswerChecker.objects.get(index__exact=sc.score)
    except:
        return render(request, 'treasurehunt/hunt_win.html', {'score': sc.score})

    level = models.level.objects.get(l_number=sc.score + 1)
    if sc.ban == True:
        return render(request, 'treasurehunt/banned.html', {'score': sc.score})
    else:

        if int(sc.score) >= 25:
            return render(request, 'treasurehunt/hunt_win.html', {'score': sc.score})
        else:
            if request.method == 'POST':
                question_form = forms.Answer(data=request.POST)
                if question_form.is_valid():
                    ans = question_form.cleaned_data['answer']

                    if ans.lower() == ans_fixed.ans_value():
                        sc.score = sc.score + 1
                        sc.timestamp = datetime.datetime.now()
                        sc.save()
                        level.numuser = level.numuser + 1
                        level.accuracy = round(level.numuser / (float(level.numuser + level.wrong)), 2)
                        level.save()
                        anslog = 'Level: ' + str(sc.score + 1) + ' user: ' + str(current_user) + ' answer: ' + str(ans)
                        print(colored(anslog, 'green'))
                        return render(request, 'treasurehunt/level_transition.html', {'score': sc.score})

                    else:
                        level.wrong = level.wrong + 1
                        level.save()
                        anslog = 'Level: ' + str(sc.score + 1) + ' user: ' + str(current_user) + ' answer: ' + str(ans)
                        print(colored(anslog, 'red'))
                        return render(request, 'treasurehunt/level_fail.html', {'score': sc.score})
                else:

                    return render(
                        request, 'treasurehunt/question.html', {
                            'question_form': question_form,
                            'score': sc.score,
                            'question_fixed': question_fixed[sc.score],
                            'level': level
                        })
            else:
                question_form = forms.Answer()

            return render(
                request, 'treasurehunt/question.html', {
                    'question_form': question_form,
                    'score': sc.score,
                    'question_fixed': question_fixed[sc.score],
                    'level': level
                })


def leaderboard(request):
    leader = models.Score.objects.all().filter(ban=False).order_by('-score', 'timestamp')

    current_user = request.user

    rank = 0
    current_user1 = str(current_user)
    if (current_user1 == "AnonymousUser"):
        user_name = []
        i = 1

        for x in leader:
            # up = models.userProfile.objects.get(user=x.user.username)
            user_name.append((i, x.user.username, x.score, x.timestamp))
            i += 1

        return render(request, 'treasurehunt/leaderboard.html', {
            'user_name': user_name
        })
    else:
        try:
            sc = models.Score.objects.get(user__exact=current_user)

        except:
            score = models.Score()
            score.user = current_user
            score.save()
            sc = models.Score.objects.get(user__exact=current_user)
        user_name = []
        i = 1

        for x in leader:
            # print(x.user.username, current_user)
            # up = models.userProfile.objects.get(user =x.user.username)
            if (str(x.user.username) == current_user1):
                rank = i

            user_name.append((i, x.user.username, x.score, x.timestamp))
            i += 1

        return render(request, 'treasurehunt/leaderboard.html', {
            'user_name': user_name, 'score': sc.score, 'rank': rank
        })

# t = Score.objects.all().order_by('-score')
# t[0].user.username
