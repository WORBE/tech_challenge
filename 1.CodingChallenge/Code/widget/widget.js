(function(){
  const API_VALIDATE = "http://localhost:8000/api/validate/";

  function createWidgetModal() {
    const modal = document.createElement('div');
    modal.id = 'superpayment-modal';
    modal.style.position = 'fixed';
    modal.style.left = '0'; modal.style.top = '0';
    modal.style.width = '100%'; modal.style.height = '100%';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.background = 'rgba(0,0,0,0.4)';
    modal.style.zIndex = 99999;

    const box = document.createElement('div');
    box.style.width = '320px'; box.style.padding = '16px';
    box.style.background = 'white'; box.style.borderRadius = '8px';
    box.innerHTML = `
      <h3 style="margin-top:0">Pagar con SuperPayment</h3>
      <label>Cupón<br><input id="sp_voucher" style="width:100%"></label><br><br>
      <label>Código<br><input id="sp_code" style="width:100%"></label><br><br>
      <div style="text-align:right">
        <button id="sp_cancel">Cancelar</button>
        <button id="sp_submit">Enviar</button>
      </div>
      <div id="sp_msg" style="margin-top:8px;font-size:13px;color:#444"></div>
    `;

    modal.appendChild(box);
    document.body.appendChild(modal);

    modal.querySelector('#sp_cancel').onclick = () => { closeModal(); triggerHost('cancelled'); };

    modal.querySelector('#sp_submit').onclick = async () => {
      const voucher = document.getElementById('sp_voucher').value;
      const code = document.getElementById('sp_code').value;

      let order = { order_id: null, order_value: null };
      if (window.SuperPayment?.getOrderData) {
        try { order = window.SuperPayment.getOrderData(); } catch(e) {}
      }

      document.getElementById('sp_msg').textContent = 'Validando...';

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
          document.getElementById('sp_msg').textContent = '¡Autorizado! Cerrando widget...';
          closeModal();
          triggerHost('authorized', j);
        } else {
          document.getElementById('sp_msg').textContent = 'No autorizado: ' + (j.reason || 'error');
          triggerHost('denied', j);
        }

      } catch(err) {
        document.getElementById('sp_msg').textContent = 'Error de red';
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
