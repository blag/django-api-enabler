A Django helper app to let you specify API urls from within the apps.

Why?
====
- Do you use multiple apps in your django project?
- Do you use the conventional django way of managing your urlconfs (where you include other urlconfs to your apps)?
- Do you wish to have URL prefix like '/api/' followed by your custom app prefix, or do you want to include all model slugs after '/api/'?
- Do you like to keep the URLconf at the app level for individual mappings?

If your answer is Yes to all, then this app is for you.

What?
=====
In simplest way, when your have your urlconf like:

    urlpatterns = patterns('',
        # ... snip ...
        (r'^accounts/', include('accounts.urls')),
        (r'^analytics/', include('analytics.urls')),
        (r'^search/', include('search.urls')),
        (r'^r/', include('inventory.urls')),
        # ... snip ...
    )

And you want to have APIs associated with different apps in your project like:

    /api/accounts/
    /api/analytics/
    /api/search/
    # ... and more ...

or if you want to have APIs associated with each app's models like:

    /api/users/
    /api/users/?search=<search_query>
    /api/accounts/
    /api/projects/
    # ... and more ...

where the mapping to views remains within the individual apps.

How to use?
===========
- Include "api_enabler" in your INSTALLED_APPS.
- Add "url(r'^api/', include('api_enabler.urls'))" to your base urlconf. Preferably somewhere on top. (Optional: You can change the string 'api' to whatever else you want as your root API prefix)
- Add a api.py urlconf module to each of the apps where you want API urls enabled. (* See below)
- API_URL_PREFIX in {{ app_name }}/api.py should be set to a custom url-slug to use as prefix for the app, or API_URL_VIEWSETS in {{ app_name }}/api.py should include a mapping between app model slugs and model viewsets.

* If you want to enable APIs in your accounts app your `accounts/api.py` file should look like:

    from django.conf.urls.defaults import patterns, include, url
    
    urlpatterns = patterns('accounts.views.apis',
        ...
        url(r'^register/$', 'api_register_handler'),
        url(r'^login/$', 'api_login_handler'),
        url(r'^logout/$', 'api_logout_handler'),
        ...
    )
    
    API_URL_PREFIX = 'accounts'

* Or, if you are using viewsets and routers from Django REST Framework, you can utilize the API_URL_VIEWSETS variable in `accounts/api.py` like so:

    from django.conf.urls.defaults import patterns, include, url
    
    from rest_framework import permissions, viewsets
    
    from account.serializers import *
    from account.permissions import *
    
    class UserViewSet(viewsets.ModelViewSet):
        """
        This viewset wraps the User model used for authentication
        """
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = (
            IsUser,
        )
    
    class AccountViewSet(viewsets.ModelViewSet):
        """
        This viewset wraps account information not used for authentication
        """
        queryset = Account.objects.all()
        serializer_class = AccountSerializer
        permission_classes = (
            permissions.IsAuthenticated,
            IsUserOkayToEdit
        )


    API_URL_VIEWSETS = {
        'users': UserViewSet,
        'accounts': AccountViewSet,
    }

That's it! Now you can manage your API URLs with customizable slugs from within your app directory.

Features:
=========
- You can disable APIs associated with any particular app, by renaming your api.py of the app to anything else, or commenting out the API_URL_PREFIX and API_URL_VIEWSETS in the app's api.py.
- To disable APIs for the entire project, just remove 'api_enabler' from your INSTALLED_APPS.

