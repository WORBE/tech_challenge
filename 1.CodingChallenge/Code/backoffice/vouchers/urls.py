from django.urls import path
from vouchers import views

urlpatterns = [
    #Poner el nombre hace q mi codigo se mantenible,
    #xq mi ruta puede cambiar pero siempre le voy a llamar del 'name'
    path("",views.base, name="base"),
    path("interactionlogs/", views.InteractionLogLisView.as_view(), name="interactionlog_list"),
    path("vouchers/", views.VoucherLisView.as_view(), name="voucher_list"),
    path('vouchers/new/', views.VoucherCreateView.as_view(), name='voucher_new'),
    path('vouchers/<int:pk>/edit/', views.VoucherUpdateView.as_view(), name='voucher_edit'),
    path('vouchers/<int:pk>/delete/', views.VoucherDeleteView.as_view(), name='voucher_delete'),
]
