from flask import Flask, request, render_template_string, redirect, url_for
import requests
from lxml import html

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # Retornar o formulário de pesquisa
    form_html = """
    <html>
    <body>
        <form action="/search" method="post">
            <label for="search_term">Digite o termo de pesquisa:</label>
            <input type="text" id="search_term" name="search_term">
            <input type="submit" value="Buscar">
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form["search_term"]
    response = requests.get("https://www.one-tab.com/page/sUT47ugRTz6Qd8X8r5C1RQ")
    tree = html.fromstring(response.content)

    # Encontrar todos os elementos 'tabGroupTitleText'
    group_titles = tree.xpath('//div[@class="tabGroupTitleText"]')

    # Dicionário para armazenar os títulos e seus links correspondentes
    results = {}

    for title in group_titles:
        # Presumindo que os links estão dentro de um elemento imediatamente após o título
        sibling_links = title.xpath('following-sibling::div[1]//a[@class="tabLink"]')
        results[title.text_content()] = [
            link.get("href")
            for link in sibling_links
            if search_term.lower() in link.text_content().lower()
        ]

    # Construir a página de resultados
    results_html = """
    <html>
    <body>
        <h1>RESULTADOS</h1>
        {% for title, links in results.items() %}
        <div>
            <h2>{{ title }}</h2>
            {% for link in links %}
                <a href="{{ link }}">{{ link }}</a><br>
            {% endfor %}
        </div>
        {% endfor %}
        <form action="/">
            <input type="submit" value="Nova Pesquisa">
        </form>
    </body>
    </html>
    """
    return render_template_string(results_html, results=results)


if __name__ == "__main__":
    app.run(debug=True)
