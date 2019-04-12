'use strict';

window.onload = function () {
  const addButton = document.getElementById('addToBasketButton');
  const productId = addButton.dataset.productId;
  addButton.addEventListener('click', (event) => {
    const hReq = new XMLHttpRequest();
    hReq.open('GET', '/basket/add/' + productId + '/', true);
    hReq.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    hReq.onreadystatechange = function () {
      let hResp = JSON.parse(hReq.response, 'totalCost');
      console.log(hResp['totalCost']);
      
      if (hReq.readyState !== 4) return;
      const basketSumIndicator = document.getElementById('basketSum');
      basketSumIndicator.textContent = hResp.totalCost;
    }
    hReq.send();
    
    event.preventDefault();
  });
}