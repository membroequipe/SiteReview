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
    
    <div class="reviews-grid" style="margin-top: 1.5rem;">
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">
        
        {% assign guias_posts = site.posts | where_exp: "post", "post.category == 'guias' or post.categories contains 'guias'" %}
        
        {% if guias_posts.size > 0 %}
          {% for post in guias_posts %}
            <article class="review-card" style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: #ffffff;">
              <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: inherit; display: block;">
                
                <!-- Imagem do Post -->
                {% if post.image %}
                  <div class="review-card-img" style="width: 100%; height: 160px; overflow: hidden; background: #f1f5f9;">
                    <img src="{{ post.image | relative_url }}" alt="{{ post.title }}" style="width: 100%; height: 100%; object-fit: cover;">
                  </div>
                {% endif %}

                <div class="review-content" style="padding: 16px;">
                  <span class="review-badge" style="font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase;">{{ post.categories | join: " / " | default: "Guias" }}</span>
                  <h3 class="review-card-title" style="font-size: 1.1rem; margin: 8px 0; color: #0f172a; line-height: 1.4;">{{ post.title }}</h3>
                  <div class="review-date" style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">{{ post.date | date: "%d/%m/%Y" }}</div>
                </div>
              </a>
            </article>
          {% endfor %}
        {% else %}
          <p style="grid-column: 1 / -1; color: #64748b; text-align: center; padding: 30px 0;">Em breve novos guias e tutoriais publicados.</p>
        {% endif %}
        
      </div>
    </div>

  </div>
</div>
