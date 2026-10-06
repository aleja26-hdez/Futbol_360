from rest_framework.routers import DefaultRouter
from .views import EntrenadorViewSet

router = DefaultRouter()
router.register('', EntrenadorViewSet)

urlpatterns = router.urls