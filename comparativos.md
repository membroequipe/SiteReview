---
layout: default
title: "Guias Comparativos e Melhores Opções"
permalink: /comparativos/
---

<style>
  .comparativos-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px 15px;
  }
  .comparativos-header {
    margin-bottom: 30px;
    text-align: left;
  }
  .comparativos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
  }
  .comparativo-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
  }
  .comparativo-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08);
  }
  .comparativo-card a {
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .comparativo-img-wrapper {
    width: 100%;
    height: 220px;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15px;
    border-bottom: 1px solid #edf2f7;
  }
  .comparativo-img-wrapper img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
  .comparativo-content {
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }
  .comparativo-content h2 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 10px 0;
    line-height: 1.4;
  }
  .comparativo-content p {
    font-size: 0.9rem;
    color: #4a5568;
    margin: 0;
    line-height: 1.5;
  }
</style>

<div class="comparativos-container">
  <div class="comparativos-header">
    <h1>Guias Comparativos e Melhores Opções</h1>
    <p>Confira nossos guias completos e comparações lado a lado para encontrar o produto ideal para o seu perfil e orçamento.</p>
  </div>

  <div class="comparativos-grid">
    {% for post in site.posts %}
      {% assign is_comparativo = false %}
      
      {% if post.category == "Comparativos" or post.title contains "Melhores" or post.title contains "vs" %}
        {% assign is_comparativo = true %}
      {% endif %}

      {% if is_comparativo %}
        <article class="comparativo-card">
          <a href="{{ post.url | relative_url }}">
            <div class="comparativo-img-wrapper">
              <img src="{{ post.image | relative_url }}" alt="{{ post.title }}" loading="lazy">
            </div>
            <div class="comparativo-content">
              <h2>{{ post.title }}</h2>
              <p>{{ post.description }}</p>
            </div>
          </a>
        </article>
      {% endif %}
    {% endfor %}
  </div>
</div>
