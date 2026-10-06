from rest_framework.routers import DefaultRouter
from .views import JugadorViewSet

router = DefaultRouter()
router.register('', JugadorViewSet)

urlpatterns = router.urls