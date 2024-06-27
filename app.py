from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for flash messages

CONTACTS_FILE = 'contacts.json'


# Function to load contacts from the JSON file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    return {}


# Function to save contacts to the JSON file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)


@app.route('/')
def index():
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts)


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        contacts = load_contacts()

        if name in contacts:
            flash(f"Contact {name} already exists.")
        else:
            contacts[name] = {'Phone': phone, 'Email': email}
            save_contacts(contacts)
            flash(f"Contact {name} added.")

        return redirect(url_for('index'))
    return render_template('add_contact.html')


@app.route('/remove/<name>')
def remove_contact(name):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        flash(f"Contact {name} removed.")
    else:
        flash(f"Contact {name} does not exist.")
    return redirect(url_for('index'))


@app.route('/update/<name>', methods=['GET', 'POST'])
def update_contact(name):
    contacts = load_contacts()
    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']

        if name in contacts:
            contacts[name]['Phone'] = phone
            contacts[name]['Email'] = email
            save_contacts(contacts)
            flash(f"Contact {name} updated.")
        else:
            flash(f"Contact {name} does not exist.")

        return redirect(url_for('index'))

    contact = contacts.get(name)
    if not contact:
        flash(f"Contact {name} not found.")
        return redirect(url_for('index'))

    return render_template('update_contact.html', name=name, contact=contact)


@app.route('/search', methods=['GET', 'POST'])
def search_contact():
    if request.method == 'POST':
        name = request.form['name']
        contacts = load_contacts()
        contact = contacts.get(name)
        if contact:
            return render_template('search_contact.html', contact=contact, name=name)
        else:
            flash(f"Contact {name} not found.")
            return redirect(url_for('index'))

    return render_template('search_contact.html')


if __name__ == '__main__':
    app.run(debug=True)
