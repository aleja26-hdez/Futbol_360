from rest_framework.routers import DefaultRouter
from .views import EstadoPagoViewSet, AbonoViewSet

router = DefaultRouter()
router.register('estados', EstadoPagoViewSet)
router.register('abonos', AbonoViewSet)

urlpatterns = router.urls