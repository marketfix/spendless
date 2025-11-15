---
layout: default
title: "Brands"
description: "Browse all brands with active discount codes on Spendless."
---

<h1 class="text-2xl font-semibold tracking-tight mb-4">Brands</h1>

<ul class="grid gap-3 md:grid-cols-2">
  {% assign sorted_brands = site.brands | sort: "title" %}
  {% for brand in sorted_brands %}
    <li>
      <a href="{{ brand.url | relative_url }}"
         class="block bg-white border border-slate-200 rounded-xl px-4 py-3 hover:border-slate-400 transition">
        <div class="flex items-center justify-between">
          <span class="font-medium">{{ brand.title }}</span>
          <span class="text-xs text-slate-500">
            {{ site.coupons | where: "brand_slug", brand.brand_slug | size }} offers
          </span>
        </div>
        {% if brand.description_short %}
          <p class="mt-1 text-xs text-slate-500">{{ brand.description_short }}</p>
        {% endif %}
      </a>
    </li>
  {% endfor %}
</ul>
