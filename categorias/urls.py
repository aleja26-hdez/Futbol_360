from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet

router = DefaultRouter()
router.register('', CategoriaViewSet)

urlpatterns = router.urls