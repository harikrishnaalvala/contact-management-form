from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret-key'

# Create database and table
def init_db():
    conn = sqlite3.connect('contacts.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT,
            email TEXT UNIQUE,
            phone TEXT
        )
    ''')
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# View all contacts
@app.route('/contacts')
def contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    all_contacts = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', contacts=all_contacts)

# Add contact
# contacts
@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        addr = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        if not first or not last or '@' not in email or not phone.isdigit():
            flash("Invalid input!")
            return redirect(url_for('add_contact'))

        try:
            conn = sqlite3.connect('contacts.db')
            conn.execute("INSERT INTO contacts (first_name, last_name, address, email, phone) VALUES (?, ?, ?, ?, ?)",
                         (first, last, addr, email, phone))
            conn.commit()
            conn.close()
            flash("Contact added successfully!")
        except:
            flash("Email already exists or error in saving.")
        return redirect(url_for('contacts'))
    return render_template('add_contact.html')

# Edit contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        addr = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute("UPDATE contacts SET first_name=?, last_name=?, address=?, email=?, phone=? WHERE id=?",
                       (first, last, addr, email, phone, id))
        conn.commit()
        conn.close()
        flash("Contact updated!")
        return redirect(url_for('contacts'))

    cursor.execute("SELECT * FROM contacts WHERE id=?", (id,))
    contact = cursor.fetchone()
    conn.close()
    return render_template('edit_contact.html', contact=contact)

# Delete contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    conn = sqlite3.connect('contacts.db')
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Contact deleted.")
    return redirect(url_for('contacts'))

if __name__ == '__main__':
    app.run(debug=True)
