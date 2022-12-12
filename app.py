import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        product = request.form["product"]
        feature = request.form["feature"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(product, feature),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(product, feature):
    return """Suggest three names for a product that has the following feature. Blend the result with a well known movie character.

Product: Container Orchestration
Feature: Scale well, resilient
Names: Happy Helios, Mighty manager, Solid Vessel
Product: Core Banking
Feature: Monolith, complicated system, proprietary  
Names: Mighty abyss, Transactional booker, Precise Moneystracker
Product: {}
Feature: {}
Names:""".format(
        product.capitalize(), feature.capitalize()
    )
