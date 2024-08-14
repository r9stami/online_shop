import uuid
from random import randint
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from .models import Otp, User
from account.forms import AddressForm , ContactUsForm , LoginForm , SignUpForm , VerifyPhoneForm , UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request ,'account/login.html',{'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000,9999)
            token = uuid.uuid4()
            next = request.GET.get('next')
            Otp.objects.create(code=random_code,phone=cd['phone'],token=token)
            print(random_code)
            # sms
            return redirect(reverse('account:verify') + f'?token={token}&next={next}')
        else:
            form.add_error('phone','phone is not valid')
        return render(request , 'account/login.html',{'form':form})


class VerifyOtpView(View):
    def get(self, request):
        form = VerifyPhoneForm()
        token = request.GET.get('token')
        next = request.GET.get('next')
        return render(request , 'account/verify.html',{'form':form})

    def post(self, request):
        form = VerifyPhoneForm(request.POST)

        # print(token)
        if form.is_valid():
            # print(token)
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code']).exists():
                otp = Otp.objects.get(code=cd['code'])
                user = User.objects.get(phone=otp.phone)
                login(request, user)
                next = request.GET.get('next')
                otp.delete()
                if next:
                    return redirect(next)

                return redirect(reverse('account:user_profile'))
            else:
                form.add_error('code','code is not valid')
        else:
            form.add_error('code','phone is not valid')
        return render(request , 'account/verify.html',{'form':form})


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request , 'account/signup.html',{'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(phone=cd['phone_number'],email=cd['email'],first_name=cd['first_name'],last_name=cd['last_name'],password=cd['pwd'])
            login(request, user)
            return redirect('account:user_profile')
        else:
            form.add_error('phone','something wrong')
        return render(request , 'account/signup.html',{'form':form})


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home:home')


class AddressCreateView(View):
    def post(self, request):
        form = AddressForm(request.POST)
        next_page = request.GET.get('next')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            if next_page:
                return redirect(next_page)
        else:
            form.add_error('phone','something wrong')

        return render(request,'account/address.html',{'form':form})

    def get(self,request):
        form = AddressForm()
        return render(request,'account/address.html',{'form':form})


class ContactView(View):
    def get(self,request):
        form = ContactUsForm()
        return render(request , 'account/contact.html',{'form':form})

    def post(self,request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
        return render(request , 'account/contact.html',{'form':form})


class UserProfileView(LoginRequiredMixin,View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request,'account/user_profile.html',{'form':form})

    def post(self, request):
        form = UserProfileForm(request.POST,instance=request.user)
        if request.user.is_authenticated:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.password = request.user.password
                instance.save()
                return redirect('home:home')
            else:
                form.add_error('phone','somethings wrong')
        else:
            form.add_error('phone','user is not authenticated')

        return render(request,'account/user_profile.html',{'form':form})

