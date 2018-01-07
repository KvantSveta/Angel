from flask import Flask, render_template, request, session

try:
    from logger import Logger
    from mongo import Mongo
except ImportError:
    from main.logger import Logger
    from main.mongo import Mongo

app = Flask(__name__, static_url_path="")

web_log = Logger("web.log")

mongodb = Mongo(db_name="language", collection_name="english")


def words_count(session, mongodb, log):
    if "words_count" not in session:
        try:
            session["words_count"] = mongodb.collection.count()
        except Exception as e:
            log.error(e)
            raise e

    return session["words_count"]


@app.route("/", methods=["GET"])
def english():
    return render_template("english.html")


@app.route("/russian", methods=["GET"])
def russian():
    return render_template("russian.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        english_word = request.form["english"]
        russian_word = request.form["russian"]

        try:
            answer = mongodb.collection.find_one({"word": english_word})
            if answer:
                return render_template("add.html")
        except Exception as e:
            web_log.error(e)
            raise e

        doc_id = words_count(session, mongodb, web_log) + 1

        document = {
            "_id": doc_id,
            "word": english_word,
            "translation": russian_word,
            "count": 0
        }

        try:
            mongodb.collection.insert_one(document=document)
        except Exception as e:
            web_log.error(e)
            raise e

        session["words_count"] = doc_id

    return render_template("add.html")


@app.route("/dictionary", methods=["GET"])
def dictionary():
    try:
        document = mongodb.collection.find()
    except Exception as e:
        web_log.error(e)
        raise e

    return render_template("dictionary.html", document=document, a=True)


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
