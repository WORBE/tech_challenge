from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from vouchers.models import InteractionLog, Voucher
from vouchers.forms import VoucherForm
from django.db.models import QuerySet

# Create your views here.
class VoucherLisView(generic.ListView):
    model=Voucher
    paginate_by=5
    
    def get_queryset(self)->QuerySet[Any] :
        q=self.request.GET.get('q')
        if q:
            return Voucher.objects.filter(voucher_code__icontains=q)
        
        return super().get_queryset()

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
    paginate_by=10
    
    def get_queryset(self)->QuerySet[Any] :
        q=self.request.GET.get('q')
        if q:
            return InteractionLog.objects.filter(voucher_code__icontains=q)
        
        return super().get_queryset()

def base(request):
    return render(request, "vouchers/base.html")  # tu archivo HTML