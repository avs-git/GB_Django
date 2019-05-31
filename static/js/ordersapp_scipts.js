window.onload = function () {
  var _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
  quantityArr = [];
  priceArr = [];
  
  var totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
  var orderTotalQuantity = parseInt($('.order_total_quantity').text()) || 0;
  var orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
  var $orderForm = $('.order_form');
  
  function form_init() {
    quantityArr = [];
    priceArr = [];
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    for (i = 0; i < totalForms; i++) {
      _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
      _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
      quantityArr[i] = _quantity;
      priceArr[i] = (_price) ? _price : 0;
    }
    
    
    $orderForm.on('change', 'input[type="number"]', function (event) {
      orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''));
      if (!isNaN(priceArr[orderitemNum])) {
        orderitemQuantity = parseInt(event.target.value);
        deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
        quantityArr[orderitemNum] = orderitemQuantity;
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
      }
    });
    
    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
      orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
      if (event.target.checked) {
        deltaQuantity = -quantityArr[orderitemNum];
      } else {
        deltaQuantity = quantityArr[orderitemNum];
      }
      orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });
    
  }
  
  function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
    orderitemPrice = orderitemPrice ? orderitemPrice : 0;
    deltaQuantity = deltaQuantity ? deltaQuantity : 0;
    deltaCost = orderitemPrice * deltaQuantity;
    orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
    orderTotalQuantity = orderTotalQuantity + deltaQuantity;
    
    $('.order_total_cost').html(orderTotalCost.toString());
    $('.order_total_quantity').html(orderTotalQuantity.toString());
  }
  
  function orderSummaryRecalc() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;
    
    for (i = 0; i < totalForms; i++) {
      orderTotalQuantity += quantityArr[i];
      orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $('.order_total_quantity').html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
  }
  
  function deleteOrderItem(row) {
    var targetName = row[0].querySelector('input[type="number"]').name;
    orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderitemNum] ? -quantityArr[orderitemNum] : 0;
    orderSummaryUpdate(priceArr[orderitemNum] ? priceArr[orderitemNum] : 0, deltaQuantity);
  }
  
  if (!orderTotalQuantity) {
    for (i = 0; i < totalForms; i++) {
      orderTotalQuantity += quantityArr[i];
      orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $('.order_total_quantity').html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
  }
  
  form_init();
  
  $('.formset_row').formset({
    addText: 'добавить продукт',
    deleteText: 'удалить',
    prefix: 'orderitems',
    keepFieldValues: 'input[type="number"]',
    added: form_init,
    removed: deleteOrderItem,
  });
  
  $orderForm.on('change', 'select', function (event) {
    target = event.target;
    orderitemNum = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
    // orderitemProductPK = target.options[target.selectedIndex].value;
    orderitemProductPK = target.value;
    
    if (orderitemProductPK) {
      $.ajax({
        url: "/orders/product/" + orderitemProductPK + "/price/",
        success: function (data) {
          if (data.price) {
            priceArr[orderitemNum] = parseFloat(data.price);
            if (isNaN(quantityArr[orderitemNum])) {
              quantityArr[orderitemNum] = 0;
            }
            priceHtml = '<span>' + data.price.toString().replace('.', ',') + '</span> руб';
            currentTR = $('.order_form table').find('tr:eq(' + (orderitemNum + 1) + ')');
            
            currentTR.find('td:eq(2)').html(priceHtml);
            
            if (isNaN(currentTR.find('input[type="number"]').val())) {
              currentTR.find('input[type="number"]').val(0);
            }
            orderSummaryRecalc();
          }
        }
      });
    }
  });
  
};