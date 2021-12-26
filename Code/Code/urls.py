from django.contrib import admin
from django.urls import path
from UI import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("courses/", views.courses, name="Courses"),
    path("courses/create", views.create, name="Create Courses"),
    path("explore/", views.explore, name="Explore"),
    path("video/", views.video, name="Video"),
    path("video/upload", views.upload, name="Upload Video"),
    path("settings/", views.settings, name="Settings"),
    path("settings/delete_course", views.delete_course, name="Delete Courses"),
    path("account/", views.account, name="Accounts Center"),
    path("signin/", views.signin, name="Sign In"),
    path("signup/", views.signup, name="Sign Up"),
    path("signout/", views.signout, name="Sign Out"),
    path('admin/', admin.site.urls),
]