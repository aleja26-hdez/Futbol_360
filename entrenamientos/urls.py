from rest_framework.routers import DefaultRouter
from .views import EntrenamientoViewSet

router = DefaultRouter()
router.register('', EntrenamientoViewSet)

urlpatterns = router.urls