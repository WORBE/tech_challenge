(function(){
  const API_VALIDATE = "http://localhost:8000/api/validate/";

  function createWidgetModal() {
    const modal = document.createElement('div');
    modal.id = 'superpayment-modal';

    //Crear el fondo para el modal
    Object.assign(modal.style, {
      position: 'fixed',
      left: '0', top: '0',
      width: '100%', height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'rgba(0,0,0,0.45)',
      zIndex: 99999,
      fontFamily: 'system-ui, Arial, sans-serif'
    });

    //Div para contener la modal
    const box = document.createElement('div');
    Object.assign(box.style, {
      width: '320px',
      padding: '20px',
      background: '#fff',
      borderRadius: '10px',
      boxShadow: '0 8px 24px rgba(0,0,0,0.15)'
    });

    // Helpers
    const inputStyle =
      "width:100%; padding:10px; border:1px solid #ccc; border-radius:6px; font-size:14px; margin-top:4px;";
    const btnBase =
      "padding:8px 14px; border-radius:6px; cursor:pointer; font-size:14px; border:none;";

    box.innerHTML = `
      <h3 style="margin:0 0 15px 0; font-size:18px; text-align:center;">
        Pagar con SuperPayment
      </h3>

      <label style="display:block; margin-bottom:10px;margin-right:10px;">
        Cupón
        <input id="sp_voucher" style="${inputStyle}">
      </label>

      <label style="display:block; margin-bottom:10px;margin-right:10px;">
        Código
        <input id="sp_code" style="${inputStyle}">
      </label>

      <div style="text-align:right; margin-top:10px;">
        <button id="sp_cancel"
          style="${btnBase} background:#e0e0e0; margin-right:6px;">
          Cancelar
        </button>

        <button id="sp_submit"
          style="${btnBase} background:#007bff; color:white;">
          Enviar
        </button>
      </div>

      <div id="sp_msg" style="margin-top:12px; font-size:13px; color:#555;"></div>
    `;

    modal.appendChild(box);
    document.body.appendChild(modal);

    // Boton Cancelar
    modal.querySelector('#sp_cancel').onclick = () => {
      closeModal();
      triggerHost('cancelled');
    };

    // Bonton Enviar
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
		 
		//Peticion al API Backend
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
          msg.style.color = "green";
          msg.textContent = "¡Autorizado! Cerrando widget...";
          closeModal();
          triggerHost('authorized', j);
        } else {
          msg.style.color = "red";
          msg.textContent = "No autorizado: " + (j.reason || 'error');
          triggerHost('denied', j);
        }

      } catch(err) {
        msg.style.color = "red";
        msg.textContent = "Error de red";
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
