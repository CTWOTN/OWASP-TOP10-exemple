from flask import Flask, request, render_template
import yaml

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    error = ""

    if request.method == "POST":
        user_input = request.form.get("yaml_input", "")
        exemple = '!!python/object/apply:os.system ["calc.exe"]'
        try:
            # ❌ VULNERABLE: using yaml.load with default Loader
            # This allows arbitrary object deserialization
            data = yaml.load(user_input, Loader=yaml.Loader)
            # data = yaml.safe_load(user_input)  # ✅ FIX: use safe_load to prevent code execution
            output = str(data)

        except Exception as e:
            error = str(e)

    return render_template("index.html", output=output, error=error)


if __name__ == "__main__":
    app.run(debug=True)