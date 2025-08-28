
const categoryImages = {
  "Fashion": "assets/images/fashion.jpg",
  "Travel": "assets/images/travel.jpg",
  "Marketplace": "assets/images/marketplace.jpg",
  "Automotive": "assets/images/automotive.jpg",
  "Health": "assets/images/health.jpg",
  "Tech": "assets/images/tech.jpg"
};
function qs(sel){ return document.querySelector(sel); }
function qsa(sel){ return [...document.querySelectorAll(sel)]; }

async function loadArticles(){
  const res = await fetch('data/articles.json', {cache:'no-store'});
  return (await res.json()).articles;
}
function getSlug(){
  const params = new URLSearchParams(location.search);
  return params.get('slug');
}

function renderArticle(article){
  if(!article){ qs('main').innerHTML = '<p>Article not found.</p>'; return; }
  document.title = article.title + ' – SpendLess!';
  qs('#article-title').textContent = article.title;
  const imgSrc = categoryImages[article.category] || 'assets/images/marketplace.jpg';
  qs('#article-img').src = imgSrc;
  qs('#article-img').alt = article.category + ' illustration';
  qs('#article-meta').textContent = `${article.category} · ${new Date(article.date).toLocaleDateString()}`;
  qs('#article-excerpt').textContent = article.excerpt;

  if(article.contentPath){
    fetch(article.contentPath).then(r=>r.text()).then(md=>{
      qs('#article-content').innerHTML = marked.parse(md);
    });
  }else{
    qs('#article-content').innerHTML = '<p class="prose">Content coming soon.</p>';
  }

  const list = qs('.promo-list');
  for(const p of (article.promoCodes || [])){
    const li = document.createElement('div');
    const visible = p.code.slice(0, -4);
    const masked = p.code.slice(-4);
    li.className = 'promo-code';
    li.innerHTML = `
      <div>
        <div><strong>${p.label || 'Code'}</strong> – <span class="store">${p.store || ''}</span></div>
        <div><span class="visible">${visible}</span><span class="code-mask">${masked}</span></div>
      </div>
      <button class="reveal-btn" data-url="${p.affiliateUrl}" aria-label="Reveal code and open deal">Reveal</button>
    `;
    list.appendChild(li);
  }
  qsa('.reveal-btn').forEach(btn => {
    btn.addEventListener('click', (e)=>{
      const codeEl = e.target.closest('.promo-code').querySelector('.code-mask');
      codeEl.classList.remove('code-mask');
      const url = e.target.getAttribute('data-url');
      const w = window.open(url, '_blank', 'noopener');
      if(!w){ setTimeout(()=>{ location.href = url; }, 500); }
    });
  });
}

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

async function init(){
  setupHeader();
  const slug = getSlug();
  const articles = await loadArticles();
  const article = articles.find(a => a.slug === slug);
  renderArticle(article);
}
document.addEventListener('DOMContentLoaded', init);
