from flask import Flask, render_template, request
import sys
import io
import re

app = Flask(__name__)

# Manglish -> Python mapping
MAPPING = {
    "ipo": "if",
    "alenki": "else",
    "nadakumbo": "while",
    "kaniku": "print",
    "kanik": "print",
    "nirthu": "break",
    "elenki": "else",
    "koduku": "return",
    "sheriya": "True",
    "sheri" : "True",   
    "sheriyalla": "False",
    "illa": "None",
    "pinne": "elif",
    "mathi": "pass",
    "nok": "try",
    "avasanam": "finally",
    "ppd": "def",
    "ithinu": "for",
    "appol": "while"
}

def translate(code):
    for manglish, py in MAPPING.items():
        code = re.sub(rf'\b{manglish}\b', py, code)
    return code

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    code = ""
    if request.method == "POST":
        code = request.form["code"]

        python_code = translate(code)

        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        try:
            exec(python_code, {})
        except Exception as e:
            output = str(e)
        else:
            output = redirected_output.getvalue()
        finally:
            sys.stdout = old_stdout

    return render_template("index.html", output=output, code=code)

if __name__ == "__main__":
    app.run(debug=True)
