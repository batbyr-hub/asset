
from django.urls import include, path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'asset', views.DataViewSet)
#router.register(r'asset/', views.DataViewSet, base_name='Data')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url('', include(router.urls)), # url('api', include('myapi.urls'))
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/asset/', views.saveDataAsset),
    #url('app', views.DataViewSet.dat),
]