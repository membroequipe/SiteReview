
import os
import re
import csv
import json
import html
import smtplib
import logging
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage
from urllib.parse import urlparse

import yaml
import requests
from bs4 import BeautifulSoup

# --------------------------------------------------
# CONFIGURAÇÃO
# --------------------------------------------------

PRODUCTS_FILE = Path(os.getenv("PRODUCTS_FILE", "_data/produtos.yml"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "monitor-afiliados/relatorios"))
HISTORY_FILE = OUTPUT_DIR / "history.csv"
LATEST_FILE = OUTPUT_DIR / "latest.json"

REQUEST_DELAY = float(os.getenv("REQUEST_DELAY_SECONDS", "1.2"))
TIMEOUT = 25

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
})

MARKETPLACES = {
    "mercadolivre": "Mercado Livre",
    "amazon": "Amazon",
    "shopee": "Shopee"
}

CSV_FIELDS = [
    "data", "produto_id", "produto", "marketplace",
    "url", "status", "detalhe"
]


# --------------------------------------------------
# UTILITÁRIOS
# --------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(
        timespec="seconds"
    )


def normalize_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def load_products():
    if not PRODUCTS_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de produtos não encontrado: {PRODUCTS_FILE}"
        )

    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        products = yaml.safe_load(file) or {}

    if not isinstance(products, dict):
        raise ValueError("A raiz do produtos.yml precisa ser um objeto YAML.")

    return products


def load_previous():
    if not LATEST_FILE.exists():
        return {}

    try:
        with LATEST_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("results", {})
    except (OSError, json.JSONDecodeError):
        return {}


def append_history(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = HISTORY_FILE.exists()

    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)

        if not file_exists:
            writer.writeheader()

        for item in results:
            writer.writerow({
                key: item.get(key, "")
                for key in CSV_FIELDS
            })


def save_latest(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "updated_at": now_iso(),
        "total": len(results),
        "results": {
            item["key"]: item for item in results
        }
    }

    with LATEST_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def safe_request(url):
    try:
        response = SESSION.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        return response, None
    except requests.RequestException as exc:
        return None, str(exc)


def make_result(product_id, product_name, marketplace, url,
                status, detail):
    return {
        "key": f"{product_id}|{marketplace}",
        "data": now_iso(),
        "produto_id": str(product_id),
        "produto": str(product_name),
        "marketplace": marketplace,
        "url": url,
        "status": status,
        "detalhe": detail
    }


# --------------------------------------------------
# MERCADO LIVRE
# --------------------------------------------------

def check_mercadolivre(product_id, name, url):
    response, error = safe_request(url)

    if error:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "erro", error
        )

    if response.status_code >= 400:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "link_quebrado",
            f"Página respondeu HTTP {response.status_code}"
        )

    final_url = response.url
    item_match = re.search(r"\b(MLB\d{6,})\b", final_url, re.I)

    if not item_match:
        item_match = re.search(r"\b(MLB\d{6,})\b", response.text, re.I)

    if not item_match:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "verificar_manual",
            "Não foi possível identificar o código do anúncio."
        )

    item_id = item_match.group(1).upper()
    api_url = f"https://api.mercadolibre.com/items/{item_id}"

    api_response, api_error = safe_request(api_url)

    if api_error:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "verificar_manual",
            f"Não foi possível consultar a API: {api_error}"
        )

    if api_response.status_code == 404:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "anuncio_indisponivel",
            "A API não encontrou o anúncio."
        )

    if api_response.status_code != 200:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "verificar_manual",
            f"API respondeu HTTP {api_response.status_code}"
        )

    try:
        item = api_response.json()
    except ValueError:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "verificar_manual",
            "Resposta da API não reconhecida."
        )

    listing_status = item.get("status", "")
    quantity = item.get("available_quantity")
    sub_status = item.get("sub_status") or []

    if listing_status != "active":
        return make_result(
            product_id, name, "Mercado Livre", url,
            "anuncio_indisponivel",
            f"Status do anúncio: {listing_status or 'desconhecido'}"
        )

    if quantity is not None and quantity <= 0:
        return make_result(
            product_id, name, "Mercado Livre", url,
            "sem_estoque",
            "Anúncio ativo, mas quantidade disponível igual a zero."
        )

    detail = "Anúncio ativo."
    if quantity is not None:
        detail += f" Quantidade informada pela API: {quantity}."
    if sub_status:
        detail += f" Substatus: {', '.join(map(str, sub_status))}."

    return make_result(
        product_id, name, "Mercado Livre", url,
        "disponivel", detail
    )


# --------------------------------------------------
# AMAZON E SHOPEE
# --------------------------------------------------

def check_store_page(product_id, name, marketplace, url):
    response, error = safe_request(url)

    if error:
        return make_result(
            product_id, name, marketplace, url,
            "erro", error
        )

    if response.status_code in (404, 410):
        return make_result(
            product_id, name, marketplace, url,
            "link_quebrado",
            f"Página respondeu HTTP {response.status_code}"
        )

    if response.status_code in (401, 403, 429):
        return make_result(
            product_id, name, marketplace, url,
            "verificar_manual",
            f"Marketplace bloqueou a consulta (HTTP {response.status_code})."
        )

    if response.status_code >= 400:
        return make_result(
            product_id, name, marketplace, url,
            "verificar_manual",
            f"Resposta HTTP {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    page_text = normalize_text(soup.get_text(" ", strip=True))

    unavailable_phrases = [
        "produto indisponível",
        "produto não está disponível",
        "item indisponível",
        "out of stock",
        "currently unavailable",
        "sold out",
        "este produto não está disponível",
        "não temos previsão de quando este produto estará disponível"
    ]

    for phrase in unavailable_phrases:
        if phrase in page_text:
            return make_result(
                product_id, name, marketplace, url,
                "possivelmente_sem_estoque",
                f"Encontrado indicador textual: {phrase}"
            )

    if not page_text or len(page_text) < 100:
        return make_result(
            product_id, name, marketplace, url,
            "verificar_manual",
            "Página sem conteúdo suficiente para análise."
        )

    return make_result(
        product_id, name, marketplace, url,
        "verificar_manual",
        "Página acessível, mas não foi possível confirmar o estoque."
    )


# --------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------

def run_monitor():
    products = load_products()
    previous = load_previous()
    results = []

    for product_id, product in products.items():
        if not isinstance(product, dict):
            continue

        name = product.get("nome", product_id)
        links = product.get("links") or {}

        if not isinstance(links, dict):
            continue

        for marketplace, display_name in MARKETPLACES.items():
            url = str(links.get(marketplace) or "").strip()

            if not url:
                continue

            if not url.startswith(("https://", "http://")):
                results.append(make_result(
                    product_id, name, display_name, url,
                    "link_invalido",
                    "O endereço não começa com HTTP ou HTTPS."
                ))
                continue

            logging.info("Verificando %s — %s", name, display_name)

            if marketplace == "mercadolivre":
                result = check_mercadolivre(product_id, name, url)
            else:
                result = check_store_page(
                    product_id, name, display_name, url
                )

            results.append(result)

            import time
            time.sleep(REQUEST_DELAY)

    append_history(results)
    save_latest(results)
    generate_html(results)
    send_alerts(results, previous)

    logging.info("Monitoramento concluído: %s links.", len(results))


# --------------------------------------------------
# PAINEL HTML
# --------------------------------------------------

def generate_html(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    counts = {}
    for item in results:
        status = item["status"]
        counts[status] = counts.get(status, 0) + 1

    labels = {
        "disponivel": "Disponível",
        "sem_estoque": "Sem estoque",
        "possivelmente_sem_estoque": "Possivelmente sem estoque",
        "anuncio_indisponivel": "Anúncio indisponível",
        "link_quebrado": "Link quebrado",
        "link_invalido": "Link inválido",
        "erro": "Erro de consulta",
        "verificar_manual": "Verificar manualmente"
    }

    cards = []
    for status, label in labels.items():
        cards.append(
            f'<div class="stat"><span>{html.escape(label)}</span>'
            f'<strong>{counts.get(status, 0)}</strong></div>'
        )

    rows = []
    for item in results:
        status = item["status"]
        label = labels.get(status, status)
        url = html.escape(item["url"], quote=True)

        rows.append(f"""
        <tr data-market="{html.escape(item['marketplace'])}"
            data-status="{html.escape(status)}">
          <td>{html.escape(item['produto'])}</td>
          <td>{html.escape(item['marketplace'])}</td>
          <td><span class="status">{html.escape(label)}</span></td>
          <td>{html.escape(item['detalhe'])}</td>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">Abrir anúncio</a></td>
        </tr>
        """)

    updated = now_iso()

    document = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Monitor de Afiliados</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:Arial,sans-serif;background:#f4f6fa;color:#202938;margin:0;padding:28px}}
main{{max-width:1200px;margin:auto}}
h1{{margin-bottom:5px}}
.muted{{color:#667085}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:12px;margin:25px 0}}
.stat{{background:white;padding:18px;border-radius:12px;box-shadow:0 2px 8px #0000000a}}
.stat span{{display:block;color:#667085;font-size:13px}}
.stat strong{{display:block;font-size:28px;margin-top:8px}}
.filters{{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}}
select,input{{padding:11px;border:1px solid #d0d5dd;border-radius:8px;background:white}}
.table-wrap{{overflow-x:auto;background:white;border-radius:12px}}
table{{border-collapse:collapse;width:100%;min-width:850px}}
th,td{{padding:13px;text-align:left;border-bottom:1px solid #eaecf0;font-size:14px}}
th{{background:#f9fafb}}
.status{{font-weight:bold}}
a{{color:#175cd3}}
footer{{margin-top:25px;color:#667085;font-size:12px}}
@media(max-width:600px){{body{{padding:15px}}}}
</style>
</head>
<body>
<main>
<h1>Monitor de Afiliados</h1>
<p class="muted">Última verificação: {html.escape(updated)}</p>

<section class="stats">
{''.join(cards)}
<div class="stat"><span>Total de links</span><strong>{len(results)}</strong></div>
</section>

<div class="filters">
<input id="search" placeholder="Buscar produto...">
<select id="market">
<option value="">Todos os marketplaces</option>
<option>Mercado Livre</option>
<option>Amazon</option>
<option>Shopee</option>
</select>
<select id="status">
<option value="">Todas as situações</option>
{''.join(f'<option value="{html.escape(k)}">{html.escape(v)}</option>' for k,v in labels.items())}
</select>
</div>

<div class="table-wrap">
<table>
<thead><tr>
<th>Produto</th><th>Marketplace</th><th>Situação</th>
<th>Detalhes</th><th>Link</th>
</tr></thead>
<tbody id="rows">
{''.join(rows)}
</tbody>
</table>
</div>
<footer>
Monitor independente do site. Estoque confirmado somente quando
a fonte consultada fornece informação suficiente.
</footer>
</main>
<script>
const search=document.getElementById('search');
const market=document.getElementById('market');
const status=document.getElementById('status');
function filterRows(){{
 const q=search.value.toLowerCase();
 document.querySelectorAll('#rows tr').forEach(row=>{{
  const matchText=row.innerText.toLowerCase().includes(q);
  const matchMarket=!market.value||row.cells[1].innerText===market.value;
  const matchStatus=!status.value||row.dataset.status===status.value;
  row.style.display=matchText&&matchMarket&&matchStatus?'':'none';
 }});
}}
search.addEventListener('input',filterRows);
market.addEventListener('change',filterRows);
status.addEventListener('change',filterRows);
</script>
</body>
</html>
"""

    (OUTPUT_DIR / "index.html").write_text(
        document, encoding="utf-8"
    )


# --------------------------------------------------
# ALERTAS POR E-MAIL
# --------------------------------------------------

def send_alerts(results, previous):
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("ALERT_EMAIL_FROM")
    recipient = os.getenv("ALERT_EMAIL_TO")

    if not all([host, user, password, sender, recipient]):
        logging.info("E-mail não configurado. Alertas ignorados.")
        return

    changes = []

    for item in results:
        old = previous.get(item["key"])
        if not old:
            continue

        old_status = old.get("status")
        new_status = item["status"]

        if old_status != new_status:
            changes.append(
                f"{item['produto']} — {item['marketplace']}: "
                f"{old_status} → {new_status}\n"
                f"{item['url']}\n"
                f"Detalhe: {item['detalhe']}"
            )

    if not changes:
        logging.info("Nenhuma mudança de status para alertar.")
        return

    message = EmailMessage()
    message["Subject"] = (
        f"Monitor de afiliados: {len(changes)} alteração(ões)"
    )
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Foram detectadas mudanças nos links monitorados:\n\n"
        + "\n\n".join(changes)
    )

    port = int(os.getenv("SMTP_PORT", "587"))

    try:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(message)

        logging.info("Alerta enviado para %s.", recipient)

    except Exception as exc:
        logging.error("Falha ao enviar e-mail: %s", exc)


if __name__ == "__main__":
    run_monitor()
