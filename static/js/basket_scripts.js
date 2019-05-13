'use strict';

window.onload = function () {
  document.querySelector('.basket_list').addEventListener('change', (event) => {
    if (event.target.tagName === 'INPUT' && event.target.type === 'number') {
      const t_href = event.target;
      const HttpRequest = new XMLHttpRequest();
      
      HttpRequest.open('GET', '/basket/edit/' + t_href.name + '/' + t_href.value + '/', true);
      HttpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      
      HttpRequest.onreadystatechange = function () {
        const hResp = JSON.parse(HttpRequest.response);
        const basketInnerTemplate = document.querySelector('.basket_list');
        const basketSumIndicator = document.getElementById('basketSum');
        const inBasketTotalCost = document.getElementById('inBasketTotalCost');
        
        basketInnerTemplate.innerHTML = hResp['result'];
        basketSumIndicator.textContent = inBasketTotalCost.textContent;
      };
      
      HttpRequest.send();
    }
    
  });
}