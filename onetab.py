from flask import Flask, request, render_template_string
import requests
from lxml import html

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template_string(open("index.html").read())


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form["search_term"]
    response = requests.get("https://www.one-tab.com/page/sUT47ugRTz6Qd8X8r5C1RQ")
    tree = html.fromstring(response.content)

    # Encontrar todos os elementos com o XPath fornecido
    elements = tree.xpath('//div[@class="tabGroupLabel"]')

    # Filtrar os elementos que contêm o termo de pesquisa
    filtered_elements = [
        el for el in elements if search_term.lower() in el.text_content().lower()
    ]

    # Preparar os resultados para exibição
    results = [el.text_content() for el in filtered_elements]
    return f"Resultados encontrados: {results}"


if __name__ == "__main__":
    app.run(debug=True)
