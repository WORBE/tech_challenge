from django import forms
from .models import Voucher

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ('voucher_code', 'secret_code', 'value', 'active', 'expires_at')

        widgets = {
            "value": forms.NumberInput(attrs={
                "type": "number",
                "step": "0.01",
                "class": "form-control",
            }),
            "expires_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }