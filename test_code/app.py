from flask import Flask
import gettext

app = Flask(__name__)

# Load translations
lang = gettext.translation("messages", localedir="locales", languages=["en"])
lang.install()
_ = lang.gettext

@app.route("/")
def home():
    return _( "greeting" )

if __name__ == "__main__":
    app.run(debug=True)
