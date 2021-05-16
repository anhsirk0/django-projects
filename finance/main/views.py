from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib import messages

from .models import *
import os
import urllib.parse
import requests

@login_required(login_url='login')
def index(request):
    shares = Share.objects.filter(user=request.user)
    spent = 0
    for share in shares:
        spent += share.total
    
    left = round(request.user.cash, 2)
    total = round(spent + left, 2)
    return render(request, "main/index.html", {
        "shares": shares,
        "left": left,
        "total": total
    })

def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        symbol = urllib.parse.quote_plus(symbol)
        url = f"https://cloud-sse.iexapis.com/stable/stock/{symbol}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None

@login_required(login_url='login')
def quote(request):
    if request.method == "POST":
        symbol = request.POST["symbol"].upper()
        result = lookup(symbol)

        if result is not None:
            return render(request, "main/quote.html", {
                "result": result
            })
        return render(request, "main/apology.html")
    return render(request, "main/quote.html")

@login_required(login_url='login')
def buy(request):
    if request.method == "POST":
        symbol = request.POST["symbol"].upper()
        no_of_share = int(request.POST["share"])
        result = lookup(symbol)

        if result is not None:
            price = result["price"]
            symbol = result["symbol"]
            name = result["name"]

            total = round(price * no_of_share, 2)

            if total > request.user.cash:
                return render(request, "main/apology.html", {
                    "error": "Not enough money to buy shares"
                })

            try:
                already = Share.objects.get(symbol=symbol)
            except:
                already = None

            if already is not None:
                already.total += total
                already.no_of_share += no_of_share
                already.price = price
                already.save()
            
            else:
                share = Share(user=request.user, symbol=symbol, total=total,
                                name=name , no_of_share=no_of_share, price=price)
                share.save()

            hist = History(user=request.user, symbol=symbol,
                            no_of_share=no_of_share, price=price)
            hist.save()

            request.user.cash -= total
            request.user.save()
            messages.add_message(request, messages.INFO, 'Bought!')
            return HttpResponseRedirect(reverse("index"))

        return render(request, "main/apology.html")

    return render(request, "main/buy.html")

@login_required(login_url='login')
def sell(request):
    if request.method == "POST":
        symbol = request.POST["symbol"].upper()
        share_to_sell = int(request.POST["share"])

        result = lookup(symbol)
        if result is None:
            return render(request, "main/apology.html")

        try:
            share = Share.objects.get(user=request.user, symbol=symbol)
        except:
            share = None
        
        if share is not None:
            total_shares = share.no_of_share
            price = result["price"]
            total = round(share_to_sell * price, 2)

            if share_to_sell > total_shares :
                return render(request, "main/apology.html", {
                    "error": "Not enough shares to sell"
                })
            
            elif share_to_sell == total_shares:
                share.delete()
            
            else:
                share.no_of_share -= share_to_sell
                share.price = price
                share.total -= total
                share.save()
            
            hist = History(user=request.user, symbol=symbol,
                            no_of_share=-share_to_sell, price=price)
            hist.save()

            request.user.cash += total
            request.user.save()
            messages.add_message(request, messages.INFO, 'Sold!')
            return HttpResponseRedirect(reverse("index"))

        return render(request, "main/apology.html")

    all_shares = Share.objects.filter(user=request.user)
    symbols = []
    for share in all_shares:
        symbols.append(share.symbol)
    return render(request, "main/sell.html", {
        "symbols": symbols
    })

@login_required(login_url='login')
def history(request):
    all_history = History.objects.filter(user=request.user).order_by('-id')
    return render(request, "main/history.html", {
        "all_history": all_history
    })


def login_view(request):
    if request.user.is_authenticated:
        return render(request, "main/apology.html", {
            "message": "Already logged in"
        })
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.user.is_authenticated:
        return render(request, "main/apology.html", {
            "message": "Already logged in"
        })
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "main/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "main/register.html", {
                "message": "Email address/ Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/register.html")
