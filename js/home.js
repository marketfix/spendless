
const categoryImages = {
  "Fashion": "assets/images/fashion.jpg",
  "Travel": "assets/images/travel.jpg",
  "Marketplace": "assets/images/marketplace.jpg",
  "Automotive": "assets/images/automotive.jpg",
  "Health": "assets/images/health.jpg",
  "Tech": "assets/images/tech.jpg"
};
const API = {
  async loadArticles(){
    const res = await fetch('data/articles.json', {cache: 'no-store'});
    return res.json();
  }
};

function getColumns(){
  const w = window.innerWidth;
  if (w >= 1280) return 4;
  if (w >= 1024) return 3;
  if (w >= 640) return 2;
  return 1;
}
const MAX_ROWS = 5;

function renderPagination(total, perPage, currentPage){
  const pages = Math.max(1, Math.ceil(total / perPage));
  const container = document.querySelector('.pagination');
  container.innerHTML = '';
  for (let p=1; p<=pages; p++){
    const a = document.createElement('a');
    a.href = `?page=${p}`;
    a.textContent = p;
    if (p === currentPage){ a.classList.add('active'); a.setAttribute('aria-current','page'); }
    container.appendChild(a);
  }
}

function filterByCategory(articles){
  const params = new URLSearchParams(location.search);
  const cat = params.get('cat');
  if (!cat) return articles;
  return articles.filter(a => a.category === cat);
}

function renderGrid(articles, page){
  const grid = document.querySelector('.grid');
  grid.innerHTML = '';
  const perPage = getColumns() * MAX_ROWS;
  const start = (page-1) * perPage;
  const slice = articles.slice(start, start + perPage);
  for(const a of slice){
    const card = document.createElement('a');
    card.className = 'card';
    card.href = `article.html?slug=${encodeURIComponent(a.slug)}`;
    const imgSrc = categoryImages[a.category] || 'assets/images/marketplace.jpg';
    card.innerHTML = `
      <span class="badge">${a.badge || a.discount || ''}</span>
      <img class="card-thumb" src="${imgSrc}" alt="${a.category} illustration">
      <div class="card-body">
        <div class="meta"><span>${a.category}</span><time datetime="${a.date}">${new Date(a.date).toLocaleDateString()}</time></div>
        <h3>${a.title}</h3>
        <p class="excerpt">${a.excerpt}</p>
      </div>
    `;
    grid.appendChild(card);
  }
  renderPagination(articles.length, perPage, page);
}

function getPageFromQuery(){
  const params = new URLSearchParams(location.search);
  const p = parseInt(params.get('page') || '1', 10);
  return Math.max(1, p);
}

async function init(){
  const data = await API.loadArticles();
  const filtered = filterByCategory(data.articles);
  const page = getPageFromQuery();
  renderGrid(filtered, page);
  window.addEventListener('resize', ()=> renderGrid(filtered, getPageFromQuery()));
}
document.addEventListener('DOMContentLoaded', init);
