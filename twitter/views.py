from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import CreateUserForm, PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from requests_oauthlib import OAuth1Session
from django.http import HttpResponse
import os
# Create your views here.

request_token_url = 'https://api.twitter.com/oauth/request_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
access_token_url = 'https://api.twitter.com/oauth/access_token'
callback_uri = 'http://127.0.0.1:8000/twitter/'
api_key = os.environ["api_key"]
api_key_secret = os.environ["api_secret"]


def home(request):
    return redirect(reverse('dashboard'))


def signup(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('dashboard'))
    else:
        pass
    context = {
        "form": form
    }
    return render(request, 'registration/signup.html', context=context)


@login_required()
def dashboard(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
        return redirect(reverse('dashboard'))

    profile_info = Integration.objects.filter(user=request.user)
    if len(profile_info) == 1:
        posts = Post.objects.filter(user=request.user)
        context = {
            "name": profile_info[0].profile_name,
            "form": form,
            "posts": posts
        }
    else:
        context = {
            "name": "No integrations set",
        }
    return render(request, 'twitter/dashboard.html', context=context)


@login_required
def editpost(request, post_id):
    profile_info = Integration.objects.filter(user=request.user)
    if len(profile_info) == 1:
        post = Post.objects.filter(pk=post_id, user=request.user).first()
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.user = request.user
            edited_post.save()
            return redirect(reverse(dashboard))
        if post:
            context = {
                "name": profile_info[0].profile_name,
                "content": post.content,
                "form": form
            }
            return render(request, 'twitter/editpost.html', context=context)
        else:
            return HttpResponse("404 not found!")
    else:
        return redirect(reverse(dashboard))


@login_required
def deletepost(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    post.delete()
    return redirect(reverse('dashboard'))


@login_required
def history(request):
    posts = History.objects.filter(user=request.user)
    profile_info = Integration.objects.filter(user=request.user).first()
    context = {"posts": posts, "name": profile_info.profile_name}
    return render(request, 'twitter/history.html', context=context)


@login_required()
def integration(request):
    # Step 1: Getting the resource owners token and secret

    oauth = OAuth1Session(api_key, client_secret=api_key_secret, callback_uri=callback_uri)
    response = oauth.fetch_request_token(request_token_url)

    # Sample response
    # {
    #     "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #     "oauth_token_secret": "Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM"
    # }

    resource_owner_key = response.get('oauth_token')
    resource_owner_secret = response.get('oauth_token_secret')
    print(resource_owner_secret)
    # Step 2: Prompting the user for authorization

    final_auth_url = oauth.authorization_url(authorize_url)
    # print(final_auth_url)

    # return render(request, 'twitter/integration.html', context={"redirect_url": final_auth_url})
    return redirect(final_auth_url)


@login_required()
def twitter(request):
    oauth_denied = request.GET.get('denied', '')
    oauth_token = request.GET.get('oauth_token', '')
    oauth_verifier = request.GET.get('oauth_verifier', '')
    if oauth_denied == '':
        oauth = OAuth1Session(api_key, client_secret=api_key_secret, resource_owner_key=oauth_token,
                              verifier=oauth_verifier)
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        resource_owner_key = oauth_tokens.get('oauth_token')
        resource_owner_secret = oauth_tokens.get('oauth_token_secret')
        # print(resource_owner_key)
        print(resource_owner_secret)
        oauth = OAuth1Session(api_key, client_secret=api_key_secret, resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret)
        response = oauth.get("https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true")
        print(response.json())
        if response.status_code == 200 and resource_owner_key is not None and resource_owner_secret is not None:
            print(response.json()["name"])
            old = Integration.objects.filter(user=request.user)
            if len(old) == 1:
                old = old[0]
                old.token = resource_owner_key
                old.secret = resource_owner_secret
                old.profile_name = response.json()["screen_name"]
                old.save()
            else:
                credentials = Integration(token=resource_owner_key, secret=resource_owner_secret,
                                          profile_name=response.json()["screen_name"], user=request.user)
                credentials.save()
        return redirect(reverse('dashboard'))
    else:
        return HttpResponse("You haven't authorized the application")


def success(request):
    return render(request, 'registration/success.html')
