from rest_framework.routers import DefaultRouter
from .views import TorneoViewSet, PartidoViewSet

router = DefaultRouter()
router.register('torneos', TorneoViewSet)
router.register('partidos', PartidoViewSet)

urlpatterns = router.urls