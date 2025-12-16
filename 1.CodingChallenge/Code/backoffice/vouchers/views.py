import json
from django.utils import timezone
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from vouchers.models import InteractionLog, Voucher
from vouchers.forms import VoucherForm
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class VoucherLisView(generic.ListView):
    model=Voucher
    paginate_by=5
    
    def get_queryset(self)->QuerySet[Any] :
        q=self.request.GET.get('q')
        if q:
            return Voucher.objects.filter(voucher_code__icontains=q).order_by("-created_at")
        
        return super().get_queryset().order_by("-created_at")

class VoucherCreateView(generic.CreateView):
    model = Voucher
    #fields = ('voucher_code', 'secret_code', 'value', 'active', 'expires_at',)
    form_class = VoucherForm
    success_url = reverse_lazy('voucher_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["expires_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        return form

class VoucherUpdateView(generic.UpdateView):
    model = Voucher
    #fields = ('voucher_code', 'secret_code', 'value', 'active', 'expires_at',)
    form_class = VoucherForm
    success_url = reverse_lazy('voucher_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["expires_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        return form

class VoucherDeleteView(generic.DeleteView):
    model = Voucher
    success_url = reverse_lazy('voucher_list')

class InteractionLogLisView(generic.ListView):
    model=InteractionLog
    paginate_by=8
    
    def get_queryset(self)->QuerySet[Any] :
        q=self.request.GET.get('q')
        if q:
            return InteractionLog.objects.filter(voucher_code__icontains=q).order_by("-created_at")
        
        return super().get_queryset().order_by("-created_at")

def base(request):
    return render(request, "vouchers/base.html")  # tu archivo HTML

@csrf_exempt
def validate_voucher(request):
    if request.method != "POST":
         return JsonResponse({
            "success": False,
            "error": "Método no permitido. Usa POST."
        }, status=405)
    
     # Intentar cargar JSON, manejar error si el body está vacío o mal formado
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "El cuerpo de la petición debe ser JSON válido."
        }, status=400)
    
    # Validación de parámetros obligatorios
    required_fields = ["voucher_code", "secret_code", "order_id", "order_value"]
    #missing = [f for f in required_fields if not data.get(f) or not isinstance(data.get(f), str)]
    missing = [f for f in required_fields if data.get(f) in [None, ""]]

    if missing:
        # Registrar intento fallido
        InteractionLog.objects.create(
            voucher_code=data.get("voucher_code"),
            secret_code=data.get("secret_code"),
            order_id=data.get("order_id"),
            order_value=None,
            authorized=False,
            reason=f"missing_fields: {', '.join(missing)}",
            client_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        return JsonResponse(
            {"success": False, "error": "Ingresar los campos obligatorios", "missing": missing},
            status=400
        )

    voucher_code = data.get("voucher_code")
    secret_code = data.get("secret_code")
    order_id = data.get("order_id")
    order_value_raw = data.get("order_value")

     # Validar conversión a Decimal
    from decimal import Decimal, InvalidOperation

    try:
        order_value = Decimal(str(order_value_raw))
    except InvalidOperation:
        InteractionLog.objects.create(
            voucher_code=voucher_code,
            secret_code=secret_code,
            order_id=order_id,
            order_value=None,
            authorized=False,
            reason="invalid_order_value",
            client_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        return JsonResponse(
            {"success": False, "error": "order_value debe ser un número decimal válido"},
            status=400
        )
    
    # Crear log preliminar
    log = InteractionLog.objects.create(
        order_id=order_id,
        order_value=order_value,
        voucher_code=voucher_code,
        secret_code=secret_code,
        reason="pending",
        client_ip=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )

    # Validación
    try:
        voucher = Voucher.objects.get(voucher_code=voucher_code)
    except Voucher.DoesNotExist:
        log.authorized = False
        log.reason = "voucher_not_found"
        log.save()
        return JsonResponse({ "success": False,"authorized": False, "reason": "voucher_not_found"},status=400)

    if voucher.secret_code != secret_code:
        log.authorized = False
        log.reason = "wrong_code"
        log.save()
        return JsonResponse({ "success": False,"authorized": False, "reason": "wrong_code"},status=400)

    if not voucher.active:
        log.authorized = False
        log.reason = "inactive"
        log.save()
        return JsonResponse({ "success": False,"authorized": False, "reason": "inactive"},status=400)
    
    #print("expires_at:", voucher.expires_at)
    #print("now:", timezone.now())

    #print("expires_at (local):", timezone.localtime(voucher.expires_at))
    #print("now (local):", timezone.localtime(timezone.now()))
    
    if voucher.expires_at and voucher.expires_at < timezone.localtime(timezone.now()):
        log.authorized = False
        log.reason = "expired"
        log.save()
        return JsonResponse({ "success": False,"authorized": False, "reason": "expired"},status=400)
    
    # Si pasó todas las validaciones
    log.authorized = True
    log.reason = "authorized"
    log.save()

    return JsonResponse({ "success": True,"authorized": True, "reason": "authorized"})