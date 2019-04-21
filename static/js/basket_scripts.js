'use strict';

window.onload = function () {
  document.querySelector('.basket_list').addEventListener('click', (event) => {
    if (event.target.tagName === 'INPUT' && event.target.type === 'number') {
      const t_href = event.target;
      const HttpRequest = new XMLHttpRequest();
      HttpRequest.open('GET', '/basket/edit/' + t_href.name + '/' + t_href.value + '/', true);
      HttpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      HttpRequest.send();
    }
    
  });
}