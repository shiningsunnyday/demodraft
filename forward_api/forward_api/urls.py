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
    path('signup/', views.Signup.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('users/', views.Users.as_view(), name="users"),
    path('policies/', views.Policies.as_view(), name="policies"),
    path('policy/', views.PolicyV.as_view(), name="policy"),
    path('thread/', views.ThreadV.as_view(), name="thread"),
    path('comment/', views.CommentV.as_view(), name="comment"),
    path('address/', views.Address.as_view(), name="address"),
    path('politician/', views.PoliticianV.as_view(), name="politician"),
    path('campaign/', views.CampaignV.as_view(), name="campaign"),
    path('stance/', views.StanceV.as_view(), name="stance"),
    # path('threads/', views.Threads.as_view(), name="threads"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]