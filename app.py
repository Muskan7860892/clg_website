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

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

@app.route('/campus')
def campus():
    return render_template('campus.html')  # Renders your campus page

@app.route('/nss')
def nss():
    return render_template('nss.html')  # Renders the NSS Events page



if __name__ == "__main__":
    app.run(debug=True)



