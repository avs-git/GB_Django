'use strict';

window.onload = function () {
  const addButton = document.getElementById('addToBasketButton');
  const productId = addButton.dataset.productId;
  addButton.addEventListener('click', (event) => {
    const hReq = new XMLHttpRequest();
    
    hReq.open('GET', '/basket/add/' + productId + '/', true);
    hReq.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    hReq.onreadystatechange = function () {
      if (hReq.readyState !== 4) return;
      const hResp = JSON.parse(hReq.response);
      const basketSumIndicator = document.getElementById('basketSum');
      
      basketSumIndicator.textContent = hResp['totalCost'];
    };
    
    hReq.send();
  });
};