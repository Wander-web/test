from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from main import models as MMODEL


def user_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'user/userclick.html')


def user_signup_view(request):
    subj_user_form = forms.SubjUserForm()
    subj_form = forms.SubjForm()
    mydict = {'userForm': subj_user_form, 'SubjForm': subj_form}
    if request.method == 'POST':
        subj_user_form = forms.SubjUserForm(request.POST)
        subj_form = forms.SubjForm(request.POST, request.FILES)
        if subj_user_form.is_valid() and subj_form.is_valid():
            user = subj_user_form.save()
            user.set_password(user.password)
            user.save()
            subj = subj_form.save(commit=False)
            subj.user = user
            subj.save()
            my_subj_group = Group.objects.get_or_create(name='USER')
            my_subj_group[0].user_set.add(user)
        return HttpResponseRedirect('userlogin')
    return render(request, 'user/usersignup.html', context=mydict)


def is_user(user):
    return user.groups.filter(name='USER').exists()


@login_required(login_url='userlogin')
@user_passes_test(is_user)
def user_dashboard_view(request):
    dict = {

        'total_course': MMODEL.Course.objects.all().count(),

    }
    return render(request, 'user/user_dashboard.html', context=dict)


@login_required(login_url='userlogin')
@user_passes_test(is_user)
def user_course_view(request):

    prof = models.Subj.objects.get()

    profa = {
        'prof_real': prof.prof_real,
        'prof_social': prof.prof_social,
        'prof_intellect': prof.prof_intellect,
        'prof_initiative': prof.prof_initiative,
        'prof_conventional': prof.prof_conventional,
        'prof_art': prof.prof_art
    }
    sorted_tuples = sorted(profa.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}

    main = '-' + list(sorted_dict.keys())[0]
    sec = '-' + list(sorted_dict.keys())[1]

    courses = MMODEL.Course.objects.all().order_by(main, sec)

    return render(request, 'user/user_course.html', {'courses': courses})


@login_required(login_url='userlogin')
@user_passes_test(is_user)
def user_test_view(request):

    return render(request, 'user/user_test.html')


@login_required(login_url='userlogin')
@user_passes_test(is_user)
def user_exam_view(request):

    subj = models.Subj.objects.get()
    subjtForm = forms.SubjForm(instance=subj)

    print(subj)

    if request.method == 'POST' and request.is_ajax():
        subjtForm = forms.SubjForm(request.POST, instance=subj)
        if subjtForm.is_valid():
            subjtForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/user/user-course')

    return render(request, 'user/user_exam.html', {'SubjForm': subjtForm})


