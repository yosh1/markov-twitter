from flask import *
from jinja2 import *
import test3

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "GET":
        return render_template("main.html")
    else:
        return render_template("markov.html", mark=test3.mar(request.form["userid"]))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
