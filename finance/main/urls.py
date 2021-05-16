from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("quote", views.quote, name="quote"),
    path("buy", views.buy, name="buy"),
    path("sell", views.sell, name="sell"),
    path("history", views.history, name="history"),
]