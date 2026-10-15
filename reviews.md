---
layout: default
title: "Reviews e Artigos Recentes"
description: "Confira todas as nossas análises, reviews e guias publicados."
---

<h1>Nossos Reviews e Análises</h1>
<p style="color: #64748b; margin-bottom: 2rem;">Explore todos os artigos publicados em nosso portal:</p>

<div class="posts-list">
  {% for post in site.posts %}
    <article style="margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0;">
      <h2 style="font-size: 1.4rem; margin-bottom: 0.5rem;">
        <a href="{{ post.url | relative_url }}" style="color: #0f172a; text-decoration: none;">{{ post.title }}</a>
      </h2>
      <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 0.75rem;">Publicado em {{ post.date | date: "%d/%m/%Y" }}</p>
      <p style="color: #334155; margin-bottom: 1rem;">{{ post.excerpt | strip_html | truncate: 150 }}</p>
      <a href="{{ post.url | relative_url }}" style="color: #0d9488; font-weight: 600; text-decoration: none; font-size: 0.95rem;">Ler review completo &rarr;</a>
    </article>
  {% endfor %}
</div>
