
from django.contrib import admin
from django.urls import path,include
from accounts.views import register,home_page
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',home_page,name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls')),
    path('images/',include(('images.urls','images'),namespace='images')),
    path('social-auth/', include('social.apps.django_app.urls'),name='social'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
