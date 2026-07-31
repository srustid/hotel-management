from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# ---- Config ----
app.config['SECRET_KEY'] = 'f3a9c1e7d8b4a2f6c0e5d9b7a1c3e8f2'  # replace with a securely generated key in production
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'example.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---- Model ----
class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    rooms = db.Column(db.Integer, nullable=False, default=0)
    contact = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Hotel {self.name}>'


# ---- Ensure table exists even if example.db already exists ----
with app.app_context():
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    db.create_all()   # only creates missing tables, won't touch existing ones


# ---- Routes: CRUD ----

@app.route('/')
def index():
    hotels = Hotel.query.order_by(Hotel.id.desc()).all()
    return render_template('index.html', hotels=hotels)


@app.route('/add', methods=['POST'])
def add_hotel():
    name = request.form.get('name', '').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', '').strip()
    rooms = request.form.get('rooms', '0').strip()
    contact = request.form.get('contact', '').strip()

    if not name or not address or not city or not contact:
        flash('All fields are required.', 'error')
        return redirect(url_for('index'))

    try:
        rooms = int(rooms)
    except ValueError:
        rooms = 0

    new_hotel = Hotel(name=name, address=address, city=city, rooms=rooms, contact=contact)
    db.session.add(new_hotel)
    db.session.commit()
    flash('Hotel registered successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<int:hotel_id>', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)

    if request.method == 'POST':
        hotel.name = request.form.get('name', '').strip()
        hotel.address = request.form.get('address', '').strip()
        hotel.city = request.form.get('city', '').strip()
        try:
            hotel.rooms = int(request.form.get('rooms', '0'))
        except ValueError:
            hotel.rooms = 0
        hotel.contact = request.form.get('contact', '').strip()

        db.session.commit()
        flash('Hotel updated successfully.', 'success')
        return redirect(url_for('index'))

    hotels = Hotel.query.order_by(Hotel.id.desc()).all()
    return render_template('index.html', hotels=hotels, edit_hotel=hotel)


@app.route('/delete/<int:hotel_id>', methods=['POST'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)