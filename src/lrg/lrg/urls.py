"""
URL configuration for lrg project.

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
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include(("homepage.urls", "homepage"), namespace="homepage")),
    path('posts/', include(("posts.urls", "posts"), namespace="posts")),
    path('community/', include(("community.urls", "community"), namespace="community")),
    path('profiles/', include(("profiles.urls", "profiles"), namespace="profiles")),
    path('media/', include(("media.urls", "media"), namespace="media")),
    path('admin/', admin.site.urls),
]
