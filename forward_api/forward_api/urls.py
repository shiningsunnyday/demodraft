from django.urls import include, path
from rest_framework import routers
from forward_app import views

router = routers.DefaultRouter()
# router.register('signup', views.SignupViewSet, basename="signup")
# router.register('groups', views.GroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.Users.as_view(), name="users"),
    path('signup/', views.Signup.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('policies/', views.Policies.as_view(), name="policies"),
    path('policy/', views.PolicyV.as_view(), name="policy"),
    # path('threads/', views.Threads.as_view(), name="threads"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]