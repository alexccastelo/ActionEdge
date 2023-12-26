from flask import Flask, request, render_template_string, redirect, url_for
import requests
from lxml import html

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # Retornar o formulário de pesquisa
    return render_template_string(
        """
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
    )


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form["search_term"]
    response = requests.get("https://www.one-tab.com/page/sUT47ugRTz6Qd8X8r5C1RQ")
    tree = html.fromstring(response.content)

    # Encontrar todos os elementos 'tabGroupTitleText' e seus links associados
    groups = tree.xpath('//div[contains(@class, "tabGroup")]')

    results = []
    for group in groups:
        title = group.xpath('.//div[contains(@class, "tabGroupLabel")]/text()')
        if not title:
            continue
        title = title[0].strip()
        links = group.xpath('.//a[contains(@class, "tabLink")]/@href')

        # Filtrar os links com base no termo de pesquisa
        filtered_links = [link for link in links if search_term.lower() in link.lower()]

        if filtered_links:
            results.append({"title": title, "links": filtered_links})

    # Construir a página de resultados
    results_html = """
    <html>
    <body>
        <h1>RESULTADOS</h1>
        {% for result in results %}
        <div>
            <h2>{{ result.title }}</h2>
            {% for link in result.links %}
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
