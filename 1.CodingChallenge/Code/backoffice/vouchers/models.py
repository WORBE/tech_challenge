from django.db import models

# Create your models here.
class Voucher(models.Model):
    #Representa un voucher válido en el sistema.
    #'voucher_code' -> lo que el comprador pone en el input "cupón"
    #'secret_code'  -> lo que el comprador pone en el input "código"
    voucher_code = models.CharField(max_length=100, unique=True)
    secret_code = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.voucher_code} ({'active' if self.active else 'inactive'})"
    
class InteractionLog(models.Model):
    #Registra cada intento desde el widget (éxitos y fallos).

    # Datos recibidos desde el e-commerce
    order_id = models.CharField(max_length=200, null=True, blank=True)
    order_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Lo que el usuario ingresó
    voucher_code = models.CharField(max_length=100, null=True, blank=True)
    secret_code = models.CharField(max_length=100, null=True, blank=True)

    # Resultado de la validación
    authorized = models.BooleanField(null=True)
    reason = models.CharField(max_length=255, null=True, blank=True)

    # Metadatos operativos
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at.isoformat()} - {self.voucher_code} -> {'OK' if self.authorized else 'NOK'}"