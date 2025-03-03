from flask import Flask, render_template, redirect, url_for, request, flash, session, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Branch, Staff, HOD, BranchImages, Lecturer, Management, Principal, CellMember, Notification
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

UPLOAD_FOLDER = 'static/staff_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER_1 = 'static/hod_images'
app.config['UPLOAD_FOLDER_1'] =UPLOAD_FOLDER_1

app.config['UPLOAD_FOLDER_2'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER_2'], exist_ok=True)

app.config['UPLOAD_FOLDER_3'] = 'static/lecturer_images'
os.makedirs(app.config['UPLOAD_FOLDER_3'], exist_ok=True)

app.config['UPLOAD_FOLDER_4'] = 'static/images'
os.makedirs(app.config['UPLOAD_FOLDER_4'], exist_ok=True)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER_5'] = 'static/pdfs'
os.makedirs(app.config['UPLOAD_FOLDER_5'], exist_ok=True)

app.config['UPLOAD_FOLDER_6'] = 'static/management'
os.makedirs(app.config['UPLOAD_FOLDER_6'], exist_ok=True)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

VIEW_COUNT_FILE = "views.txt"

def get_views():
    """Read the current view count from the file."""
    try:
        with open(VIEW_COUNT_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # If file not found or empty, start with 0 views.

def update_views():
    """Increase the view count and save it back to the file."""
    views = get_views() + 1
    with open(VIEW_COUNT_FILE, "w") as file:
        file.write(str(views))
    return views

@app.route("/")
def home():
    views = update_views()
    notifications = Notification.query.order_by(Notification.id.desc()).all()
    return render_template("base.html", notifications=notifications, views=views)

@app.route("/about")
def about():
    management_list = Management.query.all()
    principal_info = Principal.query.first()
    cells = ["Placement", "NSS", "Sports", "Anti-Ragging Committee", "Anti-Ragging Squad", "WSW GR Cell"]
    members = {cell: CellMember.query.filter_by(cell=cell).all() for cell in cells}
    return render_template("about.html", management=management_list, principal=principal_info, members=members)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/application-form')
def application_form():
    return render_template('application-form.html')

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

@app.route('/notification/manage', methods=['GET', 'POST'])
def manage_notification():
    if request.method == 'POST':
        message = request.form.get('message')
        pdf_file = request.files.get('pdf')

        pdf_filename = None
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER_5'], pdf_filename))

        new_notification = Notification(message=message, pdf_filename=pdf_filename)
        db.session.add(new_notification)
        db.session.commit()
        return redirect(url_for('manage_notification'))

    notifications = Notification.query.order_by(Notification.id.desc()).all()
    return render_template('manage_notification.html', notifications=notifications)

@app.route('/notification/edit/<int:id>', methods=['GET', 'POST'])
def edit_notification(id):
    notification = Notification.query.get_or_404(id)

    if request.method == 'POST':
        new_message = request.form.get('message')
        new_pdf = request.files.get('pdf')

        if new_message:
            notification.message = new_message

        if new_pdf and new_pdf.filename.endswith('.pdf'):
            pdf_filename = secure_filename(new_pdf.filename)
            new_pdf.save(os.path.join(app.config['UPLOAD_FOLDER_5'], pdf_filename))
            notification.pdf_filename = pdf_filename

        db.session.commit()
        return redirect(url_for('manage_notification'))

    return render_template('edit_notification.html', notification=notification)

@app.route('/notification/delete/<int:id>', methods=['POST'])
def delete_notification(id):
    notification = Notification.query.get_or_404(id)

    if notification.pdf_filename:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER_5'], notification.pdf_filename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('manage_notification'))

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_5'], filename, as_attachment=True)


@app.route('/admin')
def admin():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid usernme or password', 'danger')

    return render_template('login.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # Check if old password is correct
        if not check_password_hash(current_user.password, old_password):
            flash('Incorrect old password', 'danger')
            return redirect(url_for('change_password'))  # Reloads the same page with error

        # Update password securely
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
        return redirect(url_for('dashboard'))  # Redirects to dashboard after success

    return render_template('change_password.html')

@app.route("/dashboard")
@login_required
def dashboard():
    branches = Branch.query.all()
    chart_images = {}

    for branch in branches:
        # Count staff, lecturers, and HODs for each branch
        staff_count = Staff.query.filter_by(branch_code=branch.branch_code).count()
        lecturer_count = Lecturer.query.filter_by(branch_code=branch.branch_code).count()
        hod_count = HOD.query.filter_by(branch_code=branch.branch_code).count()

        labels = ["Staff", "Lecturers", "HODs"]
        sizes = [staff_count, lecturer_count, hod_count]

        colors = ["skyblue", "lightgreen", "lightcoral"]

        # Generate pie chart only if there are values
        plt.switch_backend('Agg')
        plt.figure(figsize=(4, 4))

        if sum(sizes) > 0:
            plt.pie(sizes, labels=labels,
                    autopct=lambda p: f"{int(round(p * sum(sizes) / 100))}" if sum(sizes) > 0 else "0",
                    colors=colors, startangle=90)
        else:
            plt.pie([1], labels=["No Data"], colors=["gray"])

        plt.title(f"{branch.branch_name}")

        # Save image to a byte buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart_images[branch.branch_code] = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close()

    # Count totals
    total_staff = Staff.query.count()
    total_branches = Branch.query.count()
    total_lecturers = Lecturer.query.count()
    total_hods = HOD.query.count()
    theme = session.get("theme", "light")

    return render_template(
        "dashboard.html",
        total_staff=total_staff,
        total_branches=total_branches,
        total_lecturers=total_lecturers,
        total_hods=total_hods,
        chart_images=chart_images,
        branches=branches
    )

@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    branch_code = request.form.get('branch_code')
    image = request.files['image']

    if not branch_code or not image:
        return redirect(url_for('manage_branch_images'))

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER_2'], filename)
    image.save(image_path)

    # Save to database
    new_image = BranchImages(branch_code=branch_code, image_url=f"/{image_path}")
    db.session.add(new_image)
    db.session.commit()

    return redirect(url_for('manage_branch_images'))

@app.route("/branch")
@login_required
def branch():
    query = request.args.get('query', '')
    if query:
        branches = Branch.query.filter(
            (Branch.branch_name.ilike(f"%{query}%")) |
            (Branch.branch_code.ilike(f"%{query}%"))
        ).all()
    else:
        branches = Branch.query.order_by(Branch.branch_name).all()
    return render_template("view_branches.html", branches=branches)

# Route: Add Branch
@app.route("/add_branch", methods=["GET", "POST"])
@login_required
def add_branch():
    if request.method == "POST":
        branch_name = request.form["branch_name"]
        branch_code = request.form["branch_code"]
        new_branch = Branch(branch_name=branch_name, branch_code=branch_code)
        db.session.add(new_branch)
        db.session.commit()
        return redirect(url_for('branch'))
    return render_template("add_branch.html")

# Route: Edit Branch
@app.route("/edit_branch/<int:id>", methods=["GET", "POST"])
@login_required
def edit_branch(id):
    branch = Branch.query.get(id)
    if request.method == "POST":
        branch.branch_name = request.form["branch_name"]
        branch.branch_code = request.form["branch_code"]
        db.session.commit()
        return redirect(url_for('branch'))
    return render_template("edit_branch.html", branch=branch)

# Route: Delete Branch
@app.route("/delete_branch/<int:id>")
@login_required
def delete_branch(id):
    branch = Branch.query.get(id)
    if branch:
        db.session.delete(branch)
        db.session.commit()
    return redirect(url_for('branch'))

@app.route('/branch/<string:branch_code>')

def branch_details(branch_code):
    branch = Branch.query.filter_by(branch_code=branch_code).first_or_404()  # Fetch branch details
    staffs = Staff.query.filter_by(branch_code=branch_code).order_by(Staff.staff_id.asc()).all()
    lecturers = Lecturer.query.filter_by(branch_code=branch_code).order_by(Lecturer.staff_id.asc()).all()
    hod = HOD.query.filter_by(branch_code=branch_code).all()
    return render_template('branch_details.html', branch=branch, staffs=staffs, hod=hod, lecturers=lecturers)

@app.route("/branch_names")
def branch_names():
    branches = Branch.query.all()  # Fetch all added branch names
    return render_template("branch_names.html", branches=branches)


@app.route('/manage_branch_images')
@login_required
def manage_branch_images():
    branches = Branch.query.all()
    images = BranchImages.query.all()
    return render_template('manage_branch_images.html', branches=branches, images=images)

@app.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = BranchImages.query.get(image_id)
    if image:
        # Delete the file from the uploads folder
        image_path = image.image_url.lstrip('/')
        if os.path.exists(image_path):
            os.remove(image_path)

        # Remove from database
        db.session.delete(image)
        db.session.commit()

    return redirect(url_for('manage_branch_images'))

@app.route("/staff")
@login_required
def staff():
    query = request.args.get('query', '')
    if query:
        staff_members = Staff.query.filter(
            (Staff.staff_name.ilike(f"%{query}%")) |
            (Staff.staff_id.ilike(f"%{query}%")) |
            (Staff.designation.ilike(f"%{query}%")) |
            (Staff.department.ilike(f"%{query}%")) |
            (Staff.branch_code.ilike(f"%{query}%")) |
            (Staff.contact.ilike(f"%{query}%")) |
            (Staff.qualification.ilike(f"%{query}%"))
        ).order_by(Staff.staff_id.asc()).all()
    else:
        staff_members = Staff.query.order_by(Staff.staff_id.asc()).all()
    return render_template("view_staff.html", staff_members=staff_members)
# Route: Add Staff
@app.route("/add_staff", methods=["GET", "POST"])
@login_required
def add_staff():
    if request.method == "POST":
        staff_name = request.form["staff_name"]
        staff_id = request.form["staff_id"]
        designation = request.form["designation"]
        department = request.form["department"]
        branch_code = request.form["branch_code"]
        contact = request.form["contact"]
        qualification =request.form["qualification"]
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f"/static/staff_images/{filename}"
        else:
            image_url = None

        new_staff = Staff(
            staff_name=staff_name,
            staff_id=staff_id,
            designation=designation,
            department=department,
            contact=contact,
            branch_code=branch_code,
            qualification=qualification,
            image_url=image_url
        )
        db.session.add(new_staff)
        db.session.commit()
        return redirect(url_for('staff'))
    branches = Branch.query.all()
    return render_template("add_staff.html", branches=branches)

# Route: Edit Staff
@app.route("/edit_staff/<int:id>", methods=["GET", "POST"])
@login_required
def edit_staff(id):
    staff = Staff.query.get(id)
    if request.method == "POST":
        staff.staff_name = request.form["staff_name"]
        staff.staff_id = request.form["staff_id"]
        staff.designation = request.form["designation"]
        staff.department = request.form["department"]
        staff.branch_code = request.form["branch_code"]
        staff.contact = request.form["contact"]
        staff.qualification =request.form["qualification"]
        # Handle new image upload
        if 'image' in request.files:
            image = request.files['image']
            if image.filename:  # Only update if a new file is provided
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                staff.image_url = f"/static/staff_images/{filename}"

        db.session.commit()
        return redirect(url_for('staff'))
    branches = Branch.query.all()
    return render_template("edit_staff.html", staff=staff, branches=branches)

# Route: Delete Staff
@app.route('/delete_staff/<int:id>', methods=['POST'])
@login_required
def delete_staff(id):
    staff = Staff.query.get(id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
    return redirect(url_for('staff'))

@app.route('/hods')
@login_required
def view_hods():
    query = request.args.get('query', '')
    if query:
        hods = HOD.query.filter(
            (HOD.hod_name.ilike(f"%{query}%")) |
            (HOD.branch_code.ilike(f"%{query}%")) |
            (HOD.department.ilike(f"%{query}%")) |
            (HOD.qualification.ilike(f"%{query}%"))
        ).order_by(HOD.department.asc()).all()  # Sorting by hod_id in ascending order
    else:
        hods = HOD.query.order_by(HOD.department.asc()).all()  # Sorting by hod_id in ascending order
    return render_template("view_hod.html", hod_members=hods)

@app.route('/add_hod', methods=['GET', 'POST'])
@login_required
def add_hod():
    if request.method == 'POST':
        hod_name = request.form['hod_name']
        department = request.form['department']
        contact = request.form['contact']
        branch_code = request.form["branch_code"]
        qualification = request.form['qualification']
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER_1'], filename))
            image_url = f"/static/hod_images/{filename}"
        else:
            image_url = None

        new_hod = HOD(
            hod_name=hod_name,
            department=department,
            contact=contact,
            branch_code=branch_code,
            qualification=qualification,
            image_url=image_url,
        )

        db.session.add(new_hod)
        db.session.commit()
        return redirect(url_for('view_hods'))
    branches = Branch.query.all()
    return render_template("add_hod.html", branches=branches)

# Edit HOD
@app.route('/edit_hod/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_hod(id):
    hod = HOD.query.get_or_404(id)

    if request.method == 'POST':
        hod.hod_name = request.form['hod_name']
        hod.department = request.form['department']
        hod.contact = request.form['contact']
        hod.branch_code = request.form["branch_code"]
        hod.qualification = request.form['qualification']

        if 'image' in request.files:
            image = request.files['image']
            if image.filename:  # Only update if a new file is provided
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER_1'], filename))
                hod.image_url = f"/static/hod_images/{filename}"

        db.session.commit()
        return redirect(url_for('view_hods'))
    branches = Branch.query.all()
    return render_template("edit_hod.html", hod=hod, branches=branches)

@app.route('/delete_hod/<int:id>', methods=['POST'])
@login_required
def delete_hod(id):
    hod = HOD.query.get_or_404(id)
    db.session.delete(hod)
    db.session.commit()
    return redirect(url_for('view_hods'))

@app.route("/lecturers")
@login_required
def view_lecturers():
    search_query = request.args.get("search", "")
    if search_query:
        lecturers = Lecturer.query.filter(
            (Lecturer.name.ilike(f"%{search_query}%")) |
            (Lecturer.staff_id.ilike(f"%{search_query}%")) |
            (Lecturer.designation.ilike(f"%{search_query}%")) |
            (Lecturer.department.ilike(f"%{search_query}%")) |
            (Lecturer.qualification.ilike(f"%{search_query}%")) |
            (Lecturer.branch_code.ilike(f"%{search_query}%"))
        ).order_by(Lecturer.staff_id.asc()).all()  # Sorting by staff_id in ascending order
    else:
        lecturers = Lecturer.query.order_by(Lecturer.staff_id.asc()).all()  # Sorting by staff_id in ascending order
    return render_template("view_lecturer.html", lecturers=lecturers, search_query=search_query)

@app.route("/lecturers/add", methods=["GET", "POST"])
@login_required
def add_lecturer():
    if request.method == "POST":
        name = request.form["name"]
        staff_id = request.form["staff_id"]
        designation = request.form["designation"]
        department = request.form["department"]
        contact = request.form["contact"]
        branch_code = request.form["branch_code"]
        qualification = request.form["qualification"]

        # Handle Image Upload
        image_file = request.files["image"]
        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER_3"], filename)
            image_file.save(image_path)

        # Save Lecturer
        new_lecturer = Lecturer(
            name=name, staff_id=staff_id, designation=designation,
            department=department, contact=contact, branch_code=branch_code,
            qualification=qualification, image=filename  # ✅ Corrected field name
        )
        db.session.add(new_lecturer)
        db.session.commit()
        return redirect(url_for("view_lecturers"))
    branches = Branch.query.all()
    return render_template("add_lecturer.html", branches=branches)

# Edit Lecturer
@app.route("/lecturers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_lecturer(id):
    lecturer = Lecturer.query.get_or_404(id)

    if request.method == "POST":
        lecturer.name = request.form["name"]
        lecturer.staff_id = request.form["staff_id"]
        lecturer.designation = request.form["designation"]
        lecturer.department = request.form["department"]
        lecturer.contact = request.form["contact"]
        lecturer.branch_code = request.form["branch_code"]
        lecturer.qualification = request.form["qualification"]

        # Handle Image Update
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER_3'], filename)
            image_file.save(image_path)

            # Update Lecturer's Image Field in the Database
            lecturer.image = filename

        db.session.commit()
        return redirect(url_for("view_lecturers"))
    branches = Branch.query.all()
    return render_template("edit_lecturer.html", lecturer=lecturer, branches=branches)

# Delete Lecturer
@app.route("/lecturers/delete/<int:id>", methods=["POST"])
@login_required
def delete_lecturer(id):
    lecturer = Lecturer.query.get_or_404(id)

    # Remove Image File if it Exists
    if lecturer.image:
        image_path = os.path.join(app.config["UPLOAD_FOLDER_3"], lecturer.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(lecturer)
    db.session.commit()
    return redirect(url_for("view_lecturers"))

@app.route('/admin/management')
@login_required
def admin_management():
    management_list = Management.query.all()
    return render_template('view_management.html', management=management_list)

@app.route('/admin/management/add', methods=['GET', 'POST'])
@login_required
def add_management():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        description = request.form['description']
        image_file = request.files['image']

        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)

        new_entry = Management(name=name, position=position, description=description, image=image_file.filename)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('admin_management'))

    return render_template('add_management.html')

@app.route('/admin/management/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_management(id):
    entry = Management.query.get_or_404(id)
    if request.method == 'POST':
        entry.name = request.form['name']
        entry.position = request.form['position']
        entry.description = request.form['description']

        image_file = request.files['image']
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)
            entry.image = image_file.filename

        db.session.commit()
        return redirect(url_for('admin_management'))

    return render_template('edit_management.html', entry=entry)

@app.route('/admin/management/delete/<int:id>')
@login_required
def delete_management(id):
    entry = Management.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('admin_management'))

# Admin panel to manage principal details
@app.route('/admin/principal')
@login_required
def admin_principal():
    principal = Principal.query.first()  # Assuming only one principal exists
    return render_template('view_principal.html', principal=principal)

# Add a Principal
@app.route('/admin/principal/add', methods=['GET', 'POST'])
@login_required
def add_principal():
    if request.method == 'POST':
        name = request.form['name']
        qualification = request.form['qualification']
        description = request.form['description']
        image_file = request.files['image']

        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)

        new_principal = Principal(name=name, qualification=qualification, description=description, image=image_file.filename)
        db.session.add(new_principal)
        db.session.commit()
        return redirect(url_for('admin_principal'))

    return render_template('add_principal.html')

# Edit Principal
@app.route('/admin/principal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_principal(id):
    principal = Principal.query.get_or_404(id)
    if request.method == 'POST':
        principal.name = request.form['name']
        principal.qualification = request.form['qualification']
        principal.description = request.form['description']

        image_file = request.files['image']
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)
            principal.image = image_file.filename

        db.session.commit()
        return redirect(url_for('admin_principal'))

    return render_template('edit_principal.html', principal=principal)

# Delete Principal
@app.route('/admin/principal/delete/<int:id>')
@login_required
def delete_principal(id):
    principal = Principal.query.get_or_404(id)
    db.session.delete(principal)
    db.session.commit()
    return redirect(url_for('admin_principal'))

# View Members for a Specific Cell
@app.route('/admin/cell/<cell_name>')
@login_required
def view_cell_members(cell_name):
    members = CellMember.query.filter_by(cell=cell_name).all()
    return render_template('view_cell_members.html', members=members, cell_name=cell_name)

# Add a New Member
@app.route('/admin/cell/add/<cell_name>', methods=['GET', 'POST'])
@login_required
def add_cell_member(cell_name):
    if request.method == 'POST':
        name = request.form['name']
        image_file = request.files['image']

        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)

        new_member = CellMember(name=name, image=image_file.filename, cell=cell_name)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('view_cell_members', cell_name=cell_name))

    return render_template('add_cell_member.html', cell_name=cell_name)

# Edit a Member
@app.route('/admin/cell/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cell_member(id):
    member = CellMember.query.get_or_404(id)
    if request.method == 'POST':
        member.name = request.form['name']

        image_file = request.files['image']
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER_6'], image_file.filename)
            image_file.save(image_path)
            member.image = image_file.filename

        db.session.commit()
        return redirect(url_for('view_cell_members', cell_name=member.cell))

    return render_template('edit_cell_member.html', member=member)

# Delete a Member
@app.route('/admin/cell/delete/<int:id>')
@login_required
def delete_cell_member(id):
    member = CellMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('view_cell_members', cell_name=member.cell))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

with app.app_context():
    db.create_all()  # Ensure tables are created

    # Check if admin user exists, if not, create one
    if not User.query.filter_by(username="admin123").first():
        new_user = User(username="admin123")
        new_user.set_password("password")  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        print("Admin user added successfully")

if __name__ == "__main__":
    app.run(debug=True)



