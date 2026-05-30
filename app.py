from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    disease = db.Column(db.String(100))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        patient = Patient(
            name=request.form["name"],
            age=request.form["age"],
            disease=request.form["disease"]
        )

        db.session.add(patient)
        db.session.commit()

        return redirect("/patients")

    return render_template("add_patient.html")


@app.route("/patients")
def patients():

    all_patients = Patient.query.all()

    return render_template(
        "view_patients.html",
        patients=all_patients
    )


@app.route("/delete/<int:id>")
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect("/patients")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient.name = request.form["name"]
        patient.age = request.form["age"]
        patient.disease = request.form["disease"]

        db.session.commit()

        return redirect("/patients")

    return render_template(
        "edit_patient.html",
        patient=patient
    )


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)