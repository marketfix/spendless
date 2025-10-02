(function(){
  function enablePreview(){
    const template = document.getElementById('homepage-template');
    const placeholder = document.getElementById('maintenance');
    if (!template || !placeholder) return;

    const fragment = template.content.cloneNode(true);
    placeholder.replaceWith(fragment);
    document.body.classList.remove('maintenance-mode');
    document.body.classList.add('preview-mode');

    const root = document.querySelector('[data-homepage-root]');
    if (!root) return;

    const inlineScripts = Array.from(root.querySelectorAll('script[data-preview-inline]'));
    inlineScripts.forEach((oldScript) => {
      const script = document.createElement('script');
      if (oldScript.id) script.id = oldScript.id;
      const type = oldScript.getAttribute('type');
      if (type && type !== 'application/json') script.type = type;
      script.textContent = oldScript.textContent;
      document.body.appendChild(script);
      oldScript.remove();
    });

    const externalScripts = Array.from(root.querySelectorAll('script[data-preview-external]')).map((oldScript) => {
      const src = oldScript.getAttribute('src');
      const attrs = Array.from(oldScript.attributes).filter(attr => !['data-preview-external', 'src'].includes(attr.name));
      oldScript.remove();
      return { src, attrs };
    }).filter(script => script.src);

    externalScripts.reduce((promise, item) => {
      return promise.then(() => new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = item.src;
        item.attrs.forEach(attr => {
          if (attr.name === 'defer') { script.defer = true; return; }
          if (attr.name === 'async') { script.async = true; return; }
          script.setAttribute(attr.name, attr.value);
        });
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`Failed to load ${item.src}`));
        document.body.appendChild(script);
      }));
    }, Promise.resolve()).catch((error) => {
      console.error(error);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const previewParam = params.get('preview');
    const shouldPreview = previewParam === '1' || previewParam === 'true';

    if (shouldPreview) {
      enablePreview();
    } else {
      document.body.classList.add('maintenance-mode');
    }
  });
})();
