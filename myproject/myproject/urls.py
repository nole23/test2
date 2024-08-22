"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.urls import path, re_path
from users import views as users
from repository import views as repository
from files import views as files
from issues import views as issues
from statistic import views as statistic

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', users.Index.as_view()),
    path('login', users.Login.as_view()),
    path('registration', users.Registration.as_view()),
    path('user-filter/<str:text>', users.User1.as_view()),
    path('user-edit', users.User1.as_view()),
    path('user-information/<str:id>', users.UserInformation1.as_view()),

    path('all-repository/<int:id>', repository.Repository.as_view()),
    path('new-repository', repository.Repository.as_view()),
    path('repository/<int:id>', repository.RepositoryData.as_view()),
    path('update-repository/general', repository.Repository.as_view()),
    path('repository/collaboators', repository.RepositoryData.as_view()),
    path('add-user-repository/<int:userId>/<int:projectUd>', repository.RepositoryUser.as_view()),

    path('files', files.File.as_view()),
    path('remove-file/<int:id>', files.File.as_view()),
    path('update-file', files.File.as_view()),

    path('filter/<str:status>/<str:nameUser>/<str:params>/<int:id>', issues.Issues.as_view()),
    path('add-issue', issues.Issues.as_view()),
    path('close-issue', issues.Issues.as_view()),

    path('add-issue-comment', issues.IssuesComment.as_view()),
    path('update-issue', issues.IssuesComment.as_view()),

    path('issue/<int:id>', issues.IssuesGet.as_view()),
    path('assigne-issue', issues.IssuesGet.as_view()),
    path('update-issue-labels', issues.IssuesLanles.as_view()),

    path('statistic/<int:id>', statistic.Statistic.as_view()),


    # region Templateview
    path('', TemplateView.as_view(template_name="ang_index.html"), name='home'),
    re_path(r'^.*$', TemplateView.as_view(template_name="ang_index.html"), name='index'),
    
]
