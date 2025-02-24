from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/sports")
def sports():
    return render_template("sports.html")

@app.route('/nss')  # ✅ This route must be added!
def nss():
    return render_template('nss.html')

@app.route('/campus')  # ✅ New Campus Page Route
def campus():
    return render_template('campus.html')

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/application-form.html')
def application_form():
    return render_template('application-form.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

if __name__ == "__main__":
    app.run(debug=True)



