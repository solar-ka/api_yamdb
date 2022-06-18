from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, RegistrationAPIView, GetToken

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view(), name='user_signup'),
    path('v1/auth/token/', GetToken.as_view(), name='token_get'),

]
