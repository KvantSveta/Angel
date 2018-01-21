import os
import random

from flask import Flask, render_template, request, session, redirect, flash

try:
    from logger import Logger
    from mongo import Mongo
except ImportError:
    from main.logger import Logger
    from main.mongo import Mongo

app = Flask(__name__, static_url_path="")

web_log = Logger("web.log")

mongodb = Mongo(
    db_name="language",
    collection_name="english",
    ip_address=os.environ['DB'] if os.environ.get('DB') else "localhost"
)


@app.route("/", methods=["GET", "POST"])
def english():
    if request.method == "POST":
        russian_word = request.form["russian"].lower()

        doc = session["english_word"]
        if not doc:
            return redirect("/")

        changed_count = 0
        # correct answer
        if russian_word in doc["translation"]:
            changed_count = 10
            correct = True
        else:  # incorrect answer
            if doc["count"] > 0:
                changed_count = -10
            correct = False

        # update record when changed_count = 10 or -10
        if changed_count != 0:
            try:
                mongodb.collection.update_one(
                    {"word": doc["word"]},
                    {"$inc": {"count": changed_count}}
                )
            except Exception as e:
                web_log.error(e)
                raise e

        return render_template(
            "answer.html",
            english_word=doc["word"],
            russian_world=doc["translation"],
            correct=correct
        )

    # GET request
    try:
        # all records when count less than 100
        document = mongodb.collection.find({"count": {"$lt": 100}})
    except Exception as e:
        web_log.error(e)
        raise e

    if document.count() == 0:
        return render_template("english.html", english_word="", error=True)

    document = [doc for doc in document]

    while True:
        # chose random record
        doc = random.choice(document)

        # number between 0 and 100 with step 10
        if doc["count"] <= random.randrange(0, 100, 10):
            english_word = doc["word"]
            session["english_word"] = doc
            break

    return render_template(
        "english.html",
        english_word=english_word,
        error=False
    )


@app.route("/russian", methods=["GET"])
def russian():
    return render_template("russian.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        english_word = request.form["english"].lower()
        russian_word = request.form["russian"].lower()

        try:
            answer = mongodb.collection.find_one({"word": english_word})
            if answer:
                return render_template("add.html", repeat=True)
        except Exception as e:
            web_log.error(e)
            raise e

        try:
            new_doc_id = mongodb.collection.count() + 1
        except Exception as e:
            log.error(e)
            raise e

        document = {
            "_id": new_doc_id,
            "word": english_word,
            "translation": russian_word,
            "count": 0
        }

        try:
            mongodb.collection.insert_one(document=document)
        except Exception as e:
            web_log.error(e)
            raise e

        flash("New word \"{0}\" have added.".format(english_word))

    return render_template("add.html", repeat=False)


@app.route("/dictionary", methods=["GET"])
def dictionary():
    try:
        document = mongodb.collection.find().sort("word")
    except Exception as e:
        web_log.error(e)
        raise e

    return render_template("dictionary.html", document=document)


@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        "error.html",
        error=404,
        message="Неправильный адрес страницы. " + error
    ), 404


app.config.from_json("config.json")
app.secret_key = app.config.get("SECRET_KEY")
app.run(
    host=app.config.get("HOST"),
    port=app.config.get("PORT"),
    debug=app.config.get("DEBUG")
)
