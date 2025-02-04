from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForms

# Create your views here.
def index(req):
    return render(req, 'index.html')

def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(req, 'tweet_list.html', {'tweets': tweets})

def create_tweet(req):
    # giving form to the user
    if req.method == "POST":
        form = TweetForms(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()  # saving my tweet in a database
            return redirect('tweet_list')
    else:
        # giving empty form to user
        form = TweetForms()
    return render(req, 'tweet_form.html', {'form': form})

def tweet_edit(req, tweet_id):
    # getting tweets
    tweet = get_object_or_404(Tweet, id=tweet_id, user=req.user)  # Fixed 'primaryKey' to 'id'
    if req.method == "POST":
        form = TweetForms(req.POST, req.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForms(instance=tweet)
    return render(req, 'tweet_form.html', {'form': form})

def tweet_delete(req, tweet_id):
    # getting the tweet id and then deleting them
    tweet = get_object_or_404(Tweet, id=tweet_id, user=req.user)  # Fixed 'primaryKey' to 'id'
    if req.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(req, 'tweet_confirm_delete.html', {'tweet': tweet})
