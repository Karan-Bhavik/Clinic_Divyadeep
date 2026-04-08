import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

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

    connection.commit()
    connection.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
