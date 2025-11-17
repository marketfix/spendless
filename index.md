---
layout: default
title: "Spendlesso"
---

<div class="py-12 text-center">
  <p class="text-sm text-slate-500">We moved!</p>
  <h1 class="text-2xl font-semibold tracking-tight text-slate-900 mt-2">You're being redirected…</h1>
  <p class="text-sm text-slate-500 mt-4 max-w-lg mx-auto">
    The Spendlesso home is now our brands directory. If you are not redirected automatically,
    <a href="{{ '/brands/' | relative_url }}" class="text-slate-900 font-medium underline">click here to browse brands</a>.
  </p>
</div>

<script>
  window.addEventListener('DOMContentLoaded', function () {
    window.location.href = '{{ '/brands/' | relative_url }}';
  });
</script>
