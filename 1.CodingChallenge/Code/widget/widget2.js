(function(){
  const API_VALIDATE = "http://localhost:8000/api/validate/";

  function createWidgetModal() {
    const modal = document.createElement('div');
    modal.id = 'superpayment-modal';
    modal.className = "position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-dark bg-opacity-50";
    modal.style.zIndex = 99999;

    const box = document.createElement('div');
    box.className = "card p-4 shadow-lg";
    box.style.maxWidth = "380px";
    box.style.width = "100%";

    box.innerHTML = `
      <h4 class="mb-3 text-center">Pagar con SuperPayment</h4>

      <div class="mb-3">
        <label class="form-label">Cupón</label>
        <input id="sp_voucher" class="form-control">
      </div>

      <div class="mb-3">
        <label class="form-label">Código</label>
        <input id="sp_code" class="form-control">
      </div>

      <div class="d-flex justify-content-end gap-2">
        <button id="sp_cancel" class="btn btn-outline-secondary btn-sm">Cancelar</button>
        <button id="sp_submit" class="btn btn-primary btn-sm">Enviar</button>
      </div>

      <div id="sp_msg" class="mt-3 small text-muted"></div>
    `;

    modal.appendChild(box);
    document.body.appendChild(modal);

    // Cancelar
    modal.querySelector('#sp_cancel').onclick = () => { closeModal(); triggerHost('cancelled'); };

    // Enviar
    modal.querySelector('#sp_submit').onclick = async () => {
      const voucher = document.getElementById('sp_voucher').value;
      const code = document.getElementById('sp_code').value;

      let order = { order_id: null, order_value: null };
      if (window.SuperPayment?.getOrderData) {
        try { order = window.SuperPayment.getOrderData(); } catch(e) {}
      }

      const msg = document.getElementById('sp_msg');
      msg.textContent = 'Validando...';

      try {
        const res = await fetch(API_VALIDATE, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
            order_id: order.order_id,
            order_value: order.order_value,
            voucher_code: voucher,
            secret_code: code
          })
        });

        const j = await res.json();

        if (j.authorized) {
          msg.classList.remove("text-danger");
          msg.classList.add("text-success");
          msg.textContent = '¡Autorizado! Cerrando widget...';

          closeModal();
          triggerHost('authorized', j);
        } else {
          msg.classList.remove("text-success");
          msg.classList.add("text-danger");
          msg.textContent = 'No autorizado: ' + (j.reason || 'error');

          triggerHost('denied', j);
        }

      } catch(err) {
        msg.classList.add("text-danger");
        msg.textContent = 'Error de red';
        triggerHost('error', { error: err.toString() });
      }
    };

    function closeModal(){
      const m = document.getElementById('superpayment-modal');
      if (m) m.remove();
    }

    function triggerHost(event, payload){
      if (window.SuperPayment?.onEvent) {
        window.SuperPayment.onEvent(event, payload || {});
      } else {
        window.postMessage({ source:'superpayment', event, payload }, '*');
      }
    }
  }

  window.SuperPayment = window.SuperPayment || {};
  window.SuperPayment.open = () => createWidgetModal();

})();
