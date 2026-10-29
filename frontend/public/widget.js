(function () {
  const container = document.createElement('div');
  container.id = 'ai-helpdesk-widget-root';
  document.body.appendChild(container);

  const iframe = document.createElement('iframe');
  iframe.src = 'http://localhost:3000'; // Target React app origin
  iframe.style.position = 'fixed';
  iframe.style.bottom = '20px';
  iframe.style.right = '20px';
  iframe.style.width = '400px';
  iframe.style.height = '600px';
  iframe.style.border = 'none';
  iframe.style.zIndex = '999999';
  iframe.style.borderRadius = '12px';
  iframe.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.3)';

  document.body.appendChild(iframe);
})();