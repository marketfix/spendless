
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
    const split = Math.floor(p.code.length / 2);
    const visible = p.code.slice(0, split);
    const hidden = p.code.slice(split);
    li.className = 'promo-code';
    li.innerHTML = `
      <div>
        <div><strong>${p.label || 'Code'}</strong> – <span class="store">${p.store || ''}</span></div>
        <div><span class="visible">${visible}</span><span class="code-mask" data-hidden="${hidden}">${'•'.repeat(hidden.length)}</span></div>
      </div>
      <button class="reveal-btn" data-url="${p.affiliateUrl}" aria-label="Reveal code and open deal">Reveal</button>
    `;
    list.appendChild(li);
  }
  qsa('.reveal-btn').forEach(btn => {
    btn.addEventListener('click', (e)=>{
      const promo = e.target.closest('.promo-code');
      const codeWrap = promo.querySelector('.visible').parentElement;
      const mask = promo.querySelector('.code-mask');
      const full = promo.querySelector('.visible').textContent + mask.dataset.hidden;
      codeWrap.textContent = full;
      const url = e.target.getAttribute('data-url');
      window.open(url, '_blank', 'noopener');
    });
  });
}

async function init(){
  const slug = getSlug();
  const articles = await loadArticles();
  const article = articles.find(a => a.slug === slug);
  renderArticle(article);
}
document.addEventListener('DOMContentLoaded', init);
