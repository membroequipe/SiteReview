---
layout: default
title: "Guias de Compra e Tutoriais de Ferramentas"
description: "Dicas de uso, manutenção, segurança e guias completos para ajudar você a escolher e utilizar suas ferramentas."
permalink: /guias/
---

<style>
  /* Ajuste cirúrgico do título no Mobile para esta página */
  @media (max-width: 768px) {
    .page-header h1, 
    .category-container h1,
    h1 {
      font-size: 1.6rem !important;
      line-height: 1.25 !important;
    }
  }
</style>

<div class="site-content">
  <div class="post-content">

    <h1>Guias e Tutoriais de Ferramentas</h1>
    <p>Aprenda a escolher, manusear com segurança e tirar o máximo proveito das suas ferramentas elétricas e a bateria.</p>

    <!-- VITRINE DINÂMICA DE GUIAS E TUTORIAIS -->
    <h2 id="artigos-guias" style="margin-top: 2rem;">Todos os Guias e Dicas Práticas</h2>
    
    <div class="reviews-grid" style="margin-top: 1.5rem; padding: 0 12px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); justify-content: center; gap: 20px; max-width: 1200px; margin-left: auto; margin-right: auto;">
    
    {% assign furadeiras_posts = site.posts | where_exp: "post", "post.category == 'furadeiras' or post.categories contains 'furadeiras'" %}
    
    {% if furadeiras_posts.size > 0 %}
      {% for post in furadeiras_posts %}
        <article class="review-card" style="border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: transform 0.2s ease;">
          <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: inherit; display: block;">
            
            <!-- Exibe a imagem APENAS se ela existir no front matter -->
            {% if post.image and post.image != "" %}
              <div class="review-card-img" style="width: 100%; height: 160px; overflow: hidden; background: #f8fafc;">
                <img src="{{ post.image | relative_url }}" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block;">
              </div>
            {% endif %}

            <div class="review-content" style="padding: 16px;">
              <span class="review-badge" style="font-size: 0.72rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 0.5px;">{{ post.categories | join: " / " | default: "Furadeiras" }}</span>
              <h3 class="review-card-title" style="font-size: 1.05rem; margin: 6px 0 0 0; color: #0f172a; line-height: 1.35; font-weight: 700;">{{ post.title }}</h3>
              <div class="review-date" style="font-size: 0.78rem; color: #94a3b8; margin-top: 10px;">{{ post.date | date: "%d/%m/%Y" }}</div>
            </div>
          </a>
        </article>
      {% endfor %}
    {% else %}
      <p style="grid-column: 1 / -1; color: #64748b; text-align: center; padding: 30px 0;">Em breve novos artigos publicados.</p>
    {% endif %}
    
  </div>
</div>

  </div>
</div>
