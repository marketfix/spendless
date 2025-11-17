---
layout: default
title: "Brands"
---

<h1 class="text-2xl font-semibold tracking-tight mb-4">Brands</h1>

<ul class="grid gap-3 md:grid-cols-2">
  {% assign sorted_brands = site.brands | sort: "title" %}
  {% for brand in sorted_brands %}
    {% assign logo_path = '/media/brand_logos/' | append: brand.brand_slug | append: '.jpg' %}
    <li>
      <a href="{{ brand.url | relative_url }}"
         class="block bg-white border border-slate-200 rounded-xl px-4 py-3 hover:border-slate-400 transition">
        <div class="flex items-start gap-3">
          <div class="w-12 h-12 flex items-center justify-center rounded-lg border border-slate-200 bg-white p-2">
            <img src="{{ logo_path | relative_url }}"
                 alt="{{ brand.title }} logo"
                 class="max-w-full max-h-full object-contain"
                 loading="lazy">
          </div>
          <div class="flex-1 space-y-1">
            <div class="flex items-start justify-between gap-2">
              <span class="font-medium text-sm text-slate-900">{{ brand.title }}</span>
              <span class="text-[11px] text-slate-500 whitespace-nowrap">
                {{ site.coupons | where: "brand_slug", brand.brand_slug | size }} offers
              </span>
            </div>
            {% if brand.description_short %}
              <p class="text-xs text-slate-500">{{ brand.description_short }}</p>
            {% endif %}
          </div>
        </div>
      </a>
    </li>
  {% endfor %}
</ul>
