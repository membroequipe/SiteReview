---
layout: default
title: "Contato"
permalink: /contato/
---

<style>
  .contact-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 40px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid #edf2f7;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }

  .contact-header {
    margin-bottom: 30px;
  }

  .contact-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 8px 0;
  }

  .contact-header p {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
  }

  @media (max-width: 640px) {
    .form-grid {
      grid-template-columns: 1fr;
    }
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .form-group.full-width {
    grid-column: 1 / -1;
  }

  .form-group label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #1e293b;
  }

  .form-control {
    width: 100%;
    padding: 12px 16px;
    background-color: #f1f5f9;
    border: 1px solid transparent;
    border-radius: 12px;
    font-size: 0.95rem;
    color: #334155;
    outline: none;
    box-sizing: border-box;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .form-control:focus {
    background-color: #ffffff;
    border-color: #0284c7;
    box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
  }

  .form-control::placeholder {
    color: #94a3b8;
  }

  select.form-control {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%20334155' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 14px center;
    background-size: 16px;
    padding-right: 40px;
  }

  textarea.form-control {
    resize: vertical;
    min-height: 140px;
  }

  .btn-submit {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background-color: #005f87;
    color: #ffffff;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 12px 28px;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.1s ease;
  }

  .btn-submit:hover {
    background-color: #004b6e;
  }

  .btn-submit svg {
    width: 16px;
    height: 16px;
    fill: currentColor;
  }
</style>

<div class="contact-container">
  <div class="contact-header">
    <h1>Envie sua mensagem</h1>
    <p>Preencha o formulário abaixo e nossa equipe responderá em breve.</p>
  </div>

  <!-- Substitua a URL do action pela sua chave gratuita do Formspree (ex: https://formspree.io/f/seu-id) -->
  <form action="https://formspree.io/f/xbjnqerw" method="POST">
    
    <div class="form-grid">
      <!-- Nome -->
      <div class="form-group">
        <label for="nome">Nome completo</label>
        <input type="text" id="nome" name="nome" class="form-control" placeholder="Seu nome" required>
      </div>

      <!-- E-mail -->
      <div class="form-group">
        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" class="form-control" placeholder="seu.email@exemplo.com" required>
      </div>

      <!-- Assunto -->
      <div class="form-group">
        <label for="assunto">Assunto</label>
        <input type="text" id="assunto" name="assunto" class="form-control" placeholder="Resumo do assunto" required>
      </div>

      <!-- Categoria -->
      <div class="form-group">
        <label for="categoria">Categoria</label>
        <select id="categoria" name="categoria" class="form-control">
          <option value="Dúvida Geral">Dúvida Geral</option>
          <option value="Sugestão de Review">Sugestão de Review</option>
          <option value="Parcerias / Anúncios">Parcerias / Anúncios</option>
          <option value="Reportar Erro">Reportar Erro</option>
        </select>
      </div>

      <!-- Mensagem -->
      <div class="form-group full-width">
        <label for="mensagem">Mensagem</label>
        <textarea id="mensagem" name="mensagem" class="form-control" placeholder="Escreva sua mensagem detalhadamente..." required></textarea>
      </div>
    </div>

    <!-- Botão de Envio -->
    <button type="submit" class="btn-submit">
      <svg viewBox="0 0 24 24">
        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
      </svg>
      Enviar Mensagem
    </button>

  </form>
</div>
