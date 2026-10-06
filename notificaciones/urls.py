from rest_framework.routers import DefaultRouter
from .views import NotificacionViewSet

router = DefaultRouter()
router.register('', NotificacionViewSet)

urlpatterns = router.urls