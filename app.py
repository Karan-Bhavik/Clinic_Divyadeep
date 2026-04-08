import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, date, timedelta
import os
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'divyadeep_secret_key_123'
app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')  # /tmp is writable on Railway
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    db_path = os.path.join(basedir, 'database.db')
    if not os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            with open(os.path.join(basedir, 'schema.sql'), 'r') as f:
                conn.executescript(f.read())
            cur = conn.cursor()
            # Prepopulate Settings
            settings_data = [
                ('clinic_name', 'Divyadeep Skin Laser and Hair Transplant Centre'),
                ('address', 'Divyadeep Skin Laser and Hair Transplant Centre,<br/>Jhansi, Uttar Pradesh, India'),
                ('phone', '+91 XXXXX XXXXX'),
                ('reception_phone', '+91 XXXXX XXXXX'),
                ('working_hours', 'Monday - Saturday: 10:00 AM - 8:00 PM<br/>Sunday: Closed'),
                ('doctor_name', 'Dr. Kuldeep Verma'),
                ('doctor_qualifications', 'MD, DNB (Dermatology, Venereology & Leprosy), Hair Transplant Specialist'),
                ('doctor_bio', 'Dr. Kuldeep Verma is a highly qualified and renowned dermatologist based in Jhansi, Uttar Pradesh. With a deep passion for clinical dermatology and aesthetic medicine, he has helped thousands of patients achieve healthy, glowing skin and restored confidence through advanced hair transplant procedures.'),
                ('doctor_education', 'MD Dermatology|DNB (National Board of Examinations)|Fellowship in Aesthetic Medicine'),
                ('doctor_achievements', 'National-level research publications|Advanced Training in Hair Transplants|Member of leading Dermatological Societies')
            ]
            cur.executemany("INSERT INTO settings (key_name, value_text) VALUES (?, ?)", settings_data)
            # Prepopulate Categories
            categories_data = [
                ('Hair & Scalp Care', 'fa-solid fa-scissors'),
                ('Skin & Dermatology', 'fa-solid fa-face-smile'),
                ('Advanced Laser Treatments', 'fa-solid fa-wand-magic-sparkles')
            ]
            cur.executemany("INSERT INTO categories (name, icon) VALUES (?, ?)", categories_data)
            # Prepopulate Treatments
            treatments_data = [
                (1, 'Hair Transplant Surgery', 'FUE techniques providing permanent, natural-looking results with minimal downtime.'),
                (1, 'PRP Therapy', 'Platelet-Rich Plasma therapy to stimulate natural hair growth and increase thickness.'),
                (1, 'Hair Fall Treatment', 'Medical management and diagnosis to stop excessive hair loss and promote regrowth.'),
                (2, 'Acne & Scar Treatment', 'Targeted therapies including peels, medication, and lasers for acne-free clear skin.'),
                (2, 'Vitiligo Treatment', 'Advanced medical and surgical treatments to repigment the white patches.'),
                (2, 'Pigmentation & Melasma', 'Effective treatments to reduce dark spots and ensure an even skin tone.'),
                (3, 'Laser Hair Removal', 'Painless diode laser technology for permanent reduction of unwanted body hair.'),
                (3, 'Tattoo Removal', 'Safe Q-switched laser treatments to fade and remove unwanted tattoos.'),
                (3, 'CO2 Fractional Laser', 'Resurfacing treatment for severe scars, stretch marks, and skin rejuvenation.')
            ]
            cur.executemany("INSERT INTO treatments (category_id, name, description) VALUES (?, ?, ?)", treatments_data)
            conn.commit()
            conn.close()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Database initialization error: {e}")

init_db()

def get_db_connection():
    conn = sqlite3.connect(os.path.join(basedir, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

def get_settings():
    conn = get_db_connection()
    settings = conn.execute('SELECT * FROM settings').fetchall()
    conn.close()
    return {s['key_name']: s['value_text'] for s in settings}

@app.context_processor
def inject_settings():
    try:
        return dict(settings=get_settings())
    except:
        return dict(settings={})

# --- PUBLIC ROUTES ---
@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    treatments = conn.execute('SELECT * FROM treatments').fetchall()
    reviews = conn.execute('SELECT * FROM reviews WHERE is_approved = 1 ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()
    return render_template('index.html', categories=categories, treatments=treatments, reviews=reviews)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/treatments')
def treatments():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    treats = conn.execute('SELECT * FROM treatments').fetchall()
    conn.close()
    return render_template('treatments.html', categories=categories, treatments=treats)

@app.route('/gallery')
def gallery():
    conn = get_db_connection()
    images = conn.execute('SELECT * FROM gallery ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('gallery.html', images=images)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/book', methods=['POST'])
def book_appointment():
    name = request.form['name']
    phone = request.form['phone']
    service = request.form['service']
    message = request.form.get('message', '')

    today = date.today().isoformat()

    conn = get_db_connection()

    appointments_today = conn.execute('SELECT COUNT(*) as count FROM appointments WHERE date = ?', (today,)).fetchone()
    count = appointments_today['count']

    token_number = f"TKN-{today.replace('-','')}-{count + 1}"

    start_time = datetime.strptime("10:00 AM", "%I:%M %p")
    expected_time = (start_time + timedelta(minutes=15 * count)).strftime("%I:%M %p")

    conn.execute('INSERT INTO appointments (patient_name, phone, service, message, date, token_number, expected_time) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (name, phone, service, message, today, token_number, expected_time))
    conn.commit()
    conn.close()

    return render_template('token_success.html', token_number=token_number, expected_time=expected_time)

@app.route('/submit-review', methods=['POST'])
def submit_review():
    patient_name = request.form['patient_name']
    rating = request.form['rating']
    review_text = request.form['review_text']
    service_name = request.form.get('service_name', '')

    conn = get_db_connection()
    conn.execute('INSERT INTO reviews (patient_name, rating, review_text, service_name, is_approved) VALUES (?, ?, ?, ?, 0)',
                 (patient_name, rating, review_text, service_name))
    conn.commit()
    conn.close()

    flash("Review submitted successfully! It will appear on the website once approved by the clinic.")
    return redirect(url_for('index'))


# --- ADMIN ROUTES ---

def login_required():
    if 'admin_logged_in' not in session:
        return False
    return True

@app.route('/admin')
def admin_dashboard():
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    today = date.today().isoformat()
    appointments = conn.execute('SELECT * FROM appointments WHERE date = ? ORDER BY id', (today,)).fetchall()
    pending_reviews = conn.execute('SELECT COUNT(*) as count FROM reviews WHERE is_approved = 0').fetchone()['count']
    conn.close()
    return render_template('admin/dashboard.html', appointments=appointments, pending_reviews=pending_reviews)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()

    if request.method == 'POST':
        for key in request.form:
            conn.execute('UPDATE settings SET value_text = ? WHERE key_name = ?', (request.form[key], key))
        conn.commit()
        flash("Settings updated successfully.")

    settings = conn.execute('SELECT * FROM settings').fetchall()
    conn.close()
    return render_template('admin/settings.html', settings={s['key_name']: s['value_text'] for s in settings})

@app.route('/admin/reviews')
def admin_reviews():
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin/reviews.html', reviews=reviews)

@app.route('/admin/reviews/approve/<int:review_id>')
def approve_review(review_id):
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('UPDATE reviews SET is_approved = 1 WHERE id = ?', (review_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_reviews'))

@app.route('/admin/treatments', methods=['GET', 'POST'])
def admin_treatments():
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_category':
            conn.execute('INSERT INTO categories (name, icon) VALUES (?, ?)', (request.form['name'], request.form['icon']))
        elif action == 'add_treatment':
            conn.execute('INSERT INTO treatments (category_id, name, description) VALUES (?, ?, ?)',
                         (request.form['category_id'], request.form['name'], request.form['description']))
        conn.commit()
        return redirect(url_for('admin_treatments'))

    categories = conn.execute('SELECT * FROM categories').fetchall()
    treatments = conn.execute('SELECT t.*, c.name as category_name FROM treatments t JOIN categories c ON t.category_id = c.id').fetchall()
    conn.close()
    return render_template('admin/treatments.html', categories=categories, treatments=treatments)

@app.route('/admin/gallery', methods=['GET', 'POST'])
def admin_gallery():
    if not login_required(): return redirect(url_for('admin_login'))
    conn = get_db_connection()

    if request.method == 'POST':
        if 'image' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash("No image selected")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            caption = request.form.get('caption', '')
            conn.execute('INSERT INTO gallery (image_path, caption) VALUES (?, ?)', (f"uploads/{filename}", caption))
            conn.commit()

    images = conn.execute('SELECT * FROM gallery ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin/gallery.html', images=images)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
