// Auto-dismiss alert messages after a few seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // Live subtotal / total recalculation on the cart page.
  // This gives instant feedback while the quantity input's own
  // "onchange" submits the form to persist the change on the server.
  const cartTable = document.getElementById('cart-table');
  if (cartTable) {
    const qtyInputs = cartTable.querySelectorAll('.qty-input');

    function recalcTotals() {
      let grandTotal = 0;
      cartTable.querySelectorAll('tbody tr').forEach(function (row) {
        const price = parseFloat(row.dataset.price);
        const qtyInput = row.querySelector('.qty-input');
        const quantity = parseInt(qtyInput.value, 10) || 0;
        const subtotal = price * quantity;
        row.querySelector('.row-subtotal').textContent = subtotal.toFixed(2);
        grandTotal += subtotal;
      });
      const totalEl = document.getElementById('cart-total');
      if (totalEl) {
        totalEl.textContent = grandTotal.toFixed(2);
      }
    }

    qtyInputs.forEach(function (input) {
      input.addEventListener('input', recalcTotals);
    });
  }
});
