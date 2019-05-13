'use strict';

window.onload = function () {
  document.querySelector('#addOrderItem').addEventListener('click', (event) => {
    const order_table = document.querySelector('#order_content_table');
    
    const last_tr = order_table.querySelectorAll('tr').item(order_table.querySelectorAll('tr').length - 1);
    const order_item_select = last_tr.querySelector('select');
    const last_order_item_id = order_item_select.name.replace('orderitems-', '').replace('-product', '');
    const new_order_item_id = +last_order_item_id + 1;
    const total_forms = document.querySelector('#id_orderitems-TOTAL_FORMS');
    
    console.log(last_order_item_id, new_order_item_id);
    const new_tr = last_tr.cloneNode(true);
    const inputs = new_tr.querySelectorAll('input');
    const selects = new_tr.querySelectorAll('select');
    
    
    inputs.forEach(element => {
      element.id = element.id.replace(last_order_item_id, new_order_item_id);
      element.name = element.name.replace(last_order_item_id, new_order_item_id);
    });
    
    selects.forEach(element => {
      element.id = element.id.replace(last_order_item_id, new_order_item_id);
      element.name = element.name.replace(last_order_item_id, new_order_item_id);
    });
    
    console.log(selects);
    
    order_table.appendChild(new_tr);
    total_forms.value = +total_forms.value + 1;
    
    console.log(last_tr);
    
  });
}