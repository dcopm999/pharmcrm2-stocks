from rest_framework.routers import SimpleRouter

from stocks.api import views

router = SimpleRouter()
router.register("stocks", views.StockViewSet)
router.register("batch", views.BatchViewSet)
router.register("batchpharmitem", views.BatchPharmItemViewSet)
router.register("balance", views.BalanceViewSet)
router.register("order", views.OrderViewSet)

app_name = "stocks-api"
urlpatterns = router.urls
