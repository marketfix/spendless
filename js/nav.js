function setupHeader(){
  const openBtn = document.querySelector('.js-open');
  const sheetWrap = document.querySelector('.mobile-nav');
  const closeBtn = document.querySelector('.js-close');
  if (!openBtn || !sheetWrap) return;
  openBtn.addEventListener('click', ()=>{
    openBtn.classList.add('burger-open');
    sheetWrap.classList.add('is-open');
    sheetWrap.setAttribute('aria-hidden','false');
  });
  const close = ()=>{
    openBtn.classList.remove('burger-open');
    sheetWrap.classList.remove('is-open');
    sheetWrap.setAttribute('aria-hidden','true');
  };
  closeBtn?.addEventListener('click', close);
  sheetWrap.addEventListener('click', (e)=>{ if(e.target === sheetWrap) close(); });
  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') close(); });
}

document.addEventListener('DOMContentLoaded', setupHeader);
