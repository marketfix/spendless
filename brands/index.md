---
layout: default
title: "Brands"
---

<section class="bg-slate-900 text-white rounded-3xl px-6 py-10 mb-8">
  <p class="text-sm uppercase tracking-[0.3em] text-slate-300">Spendlesso</p>
  <h1 class="text-3xl md:text-4xl font-semibold tracking-tight mt-3">Browse trusted brands</h1>
  <p class="text-base text-slate-200 mt-4 max-w-2xl">
    We curate a tidy list of brands we love and keep every discount code honest and up to date.
    Use the search below to jump straight to your favorite store or discover something new.
  </p>
</section>

<div class="mb-6">
  <label for="brand-search" class="sr-only">Search brands</label>
  <div class="relative">
    <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none text-slate-400">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.9 14.32a6.5 6.5 0 111.414-1.414l3.387 3.387a1 1 0 01-1.414 1.414l-3.387-3.387zM13 8.5a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z" clip-rule="evenodd" />
      </svg>
    </div>
    <input id="brand-search"
           type="search"
           placeholder="Search by brand name"
           class="w-full border border-slate-300 rounded-2xl py-3 pl-10 pr-4 text-sm focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
           autocomplete="off">
  </div>
  <p id="brand-search-helper" class="text-xs text-slate-500 mt-2">
    Showing <span id="brand-visible-count">0</span> brands
  </p>
</div>

<ul id="brand-grid" class="grid gap-3 md:grid-cols-2">
  {% assign sorted_brands = site.brands | sort: "title" %}
  {% for brand in sorted_brands %}
    {% assign logo_path = '/media/brand_logos/' | append: brand.brand_slug | append: '.jpg' %}
    <li data-brand-card data-brand-name="{{ brand.title | downcase }}">
      <a href="{{ brand.url | relative_url }}"
         data-surface-card
         class="block bg-white border border-slate-200 rounded-xl px-4 py-3 hover:border-slate-400 transition">
        <div class="flex items-start gap-3">
          <div class="w-14 h-14 flex items-center justify-center rounded-xl border border-slate-200 bg-white overflow-hidden">
            <img src="{{ logo_path | relative_url }}"
                 alt="{{ brand.title }} logo"
                 class="w-full h-full object-cover"
                 style="transform: scale(1.2);"
                 loading="lazy">
          </div>
          <div class="flex-1 space-y-1">
            <div class="flex items-start justify-between gap-2">
              <span class="font-medium text-sm text-slate-900">{{ brand.title }}</span>
              <span class="text-[11px] text-slate-500 whitespace-nowrap">
                {{ site.coupons | where: "brand_slug", brand.brand_slug | size }} offers
              </span>
            </div>
            <p class="text-xs text-slate-500">Latest {{ brand.title }} discount codes and promotions</p>
          </div>
        </div>
      </a>
    </li>
  {% endfor %}
</ul>

<div id="brand-empty-state" class="hidden text-center py-12">
  <p class="text-sm text-slate-500">No brands matched your search. Try a different name.</p>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('brand-search');
    const cards = Array.from(document.querySelectorAll('[data-brand-card]'));
    const grid = document.getElementById('brand-grid');
    const emptyState = document.getElementById('brand-empty-state');
    const visibleCount = document.getElementById('brand-visible-count');

    function filterBrands() {
      const query = searchInput.value.trim().toLowerCase();
      let matches = 0;

      cards.forEach(function (card) {
        const name = card.dataset.brandName;
        const isMatch = name.includes(query);
        card.classList.toggle('hidden', !isMatch);
        matches += isMatch ? 1 : 0;
      });

      visibleCount.textContent = matches;
      emptyState.classList.toggle('hidden', matches !== 0);
      grid.classList.toggle('hidden', matches === 0);
    }

    filterBrands();
    searchInput.addEventListener('input', filterBrands);
  });
</script>
