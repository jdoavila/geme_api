from msjs.views import NearMessages, UserMessages, NewMessage
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('near', NearMessages, basename='NearMessages')
router.register('user', UserMessages, basename='UserMessages')
router.register('new', NewMessage, basename='NewMessage')

app_name = 'msjs'

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
