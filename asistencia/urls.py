from rest_framework.routers import DefaultRouter
from .views import AsistenciaViewSet

router = DefaultRouter()
router.register('', AsistenciaViewSet)

urlpatterns = router.urls