from django.conf import settings
from django.conf.urls import patterns, url, include
from django.utils.importlib import import_module

def autodiscover_api(*args):
    """
    Auto discovers api.py modules in all of INSTALLED_APPS and fails silently
    if not present. This registers all the URLs specified in the api.py module. 
    """
        
    urlpatterns = patterns('')

    for app in args or settings.INSTALLED_APPS:
        try:
            mod = import_module('%s.api' % (app))
            urlpatterns += patterns('',
                url(r'^%s/' % (mod.API_URL_PREFIX), include(mod)),
            )
        except:
            pass
            
    return urlpatterns

if 'rest_framework' in settings.INSTALLED_APPS:
    from rest_framework.routers import DefaultRouter

    def autodiscover_drf(*args):
        """
        Auto discovers api.py modules in all of INSTALLED_APPS and fails 
        silently if not present. This registers all the viewsets specified in 
        the API_URL_VIEWSETS variable in the api.py module.
        """

        urlpatterns = patterns('')
        router = DefaultRouter(trailing_slash=False)

        for app in args or settings.INSTALLED_APPS:
            try:
                mod = import_module('%s.api' % (app))
                for model in mod.API_URL_VIEWSETS:
                    router.register(model, mod.API_URL_VIEWSETS[model])
            except:
                try:
                    # Fallback to the original so we don't lose any URLs during an upgrade
                    urlpatterns += autodiscover_api(app)
                except:
                    pass
                pass

        try:
            urlpatterns += patterns('',
                url(settings.API_AUTH_URL, include('rest_framework.urls', namespace='rest_framework'))
            )
        except:
            pass

        urlpatterns += patterns('',
            url(r'^', include(router.urls)),
        )

        return urlpatterns

    # We conditionally define autodiscover() to use the DRF-integrated version 
    # of autodiscover over the normal api_enabler version
    def autodiscover(*args, **kwargs):
        return autodiscover_drf(*args, **kwargs)
else:
    # If DRF isn't installed, then we simply wrap autodiscover_api()
    def autodiscover(*args, **kwargs):
        return autodiscover_api(*args, **kwargs)
