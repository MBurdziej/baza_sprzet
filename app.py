from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja połączenia z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/sprzet_db'  # Zaktualizuj dane logowania
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Wyłączenie monitorowania modyfikacji

db = SQLAlchemy(app)

class Sprzet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(100), nullable=False)
    numer_seryjny = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    producent = db.Column(db.String(100), nullable=False)
    
    lokalizacja_id = db.Column(db.Integer, db.ForeignKey('lokalizacja.id'), nullable=True)
    dzial_id = db.Column(db.Integer, db.ForeignKey('dzial.id'), nullable=True)
    pracownik_id = db.Column(db.Integer, db.ForeignKey('pracownik.id'), nullable=True)

    lokalizacja = db.relationship('Lokalizacja', backref=db.backref('sprzety', lazy=True))
    dzial = db.relationship('Dzial', backref=db.backref('sprzety', lazy=True))
    pracownik = db.relationship('Pracownik', backref=db.backref('sprzety', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'typ': self.typ,
            'numer_seryjny': self.numer_seryjny,
            'model': self.model,
            'producent': self.producent,
            'lokalizacja': self.lokalizacja.nazwa if self.lokalizacja else None,
            'dzial': self.dzial.nazwa if self.dzial else None,
            'pracownik': self.pracownik.imie if self.pracownik else None,
        }

class Lokalizacja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    adres = db.Column(db.String(255), nullable=False)

class Dzial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    lokalizacja_id = db.Column(db.Integer, db.ForeignKey('lokalizacja.id'), nullable=True)

    lokalizacja = db.relationship('Lokalizacja', backref='dzialy')

    def to_dict(self):
        return {
            'id': self.id,
            'nazwa': self.nazwa,
            'lokalizacja': self.lokalizacja.nazwa if self.lokalizacja else None
        }

class Pracownik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    telefon = db.Column(db.String(50), nullable=True)

@app.route('/')
def index():
    sprzety = Sprzet.query.all()
    return render_template('index.html', sprzety=sprzety)

@app.route('/sprzet/add/', methods=['GET'])
def add_sprzet():
    lokalizacje = Lokalizacja.query.all()
    dzialy = Dzial.query.all()
    pracownicy = Pracownik.query.all()
    return render_template('add_sprzet.html', lokalizacje=lokalizacje, dzialy=dzialy, pracownicy=pracownicy)

@app.route('/sprzet/add', methods=['POST'])
def save_add_sprzet():
    data = request.form

    lokalizacja = None
    if data['lokalizacja']:
        lokalizacja = Lokalizacja.query.get(data['lokalizacja'])
    dzial = None
    if data['dzial']:
        dzial = Dzial.query.get(data['dzial'])
    pracownik = None
    if data['pracownik']:
        pracownik = Pracownik.query.get(data['pracownik'])

    new_sprzet = Sprzet(
        typ=data['typ'],
        numer_seryjny=data['numer_seryjny'],
        model=data['model'],
        producent=data['producent'],
        lokalizacja_id=lokalizacja.id if lokalizacja else None,
        dzial_id=dzial.id if dzial else None,
        pracownik_id=pracownik.id if pracownik else None
    )
    db.session.add(new_sprzet)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/api/dzialy/<int:lokalizacja_id>')
def get_dzialy_for_lokalizacja(lokalizacja_id):
    dzialy = Dzial.query.filter_by(lokalizacja_id=lokalizacja_id).all()
    return jsonify([{'id': d.id, 'nazwa': d.nazwa} for d in dzialy])

@app.route('/sprzet/edit/<int:id>', methods=['GET'])
def edit_sprzet(id):
    sprzet_to_edit = Sprzet.query.get(id)
    if sprzet_to_edit:
        lokalizacje = Lokalizacja.query.all()
        dzialy = Dzial.query.all()
        pracownicy = Pracownik.query.all()
        return render_template('edit_sprzet.html', sprzet=sprzet_to_edit, lokalizacje=lokalizacje, dzialy=dzialy, pracownicy=pracownicy)
    else:
        return "Sprzęt nie znaleziony", 404

@app.route('/sprzet/edit/<int:id>', methods=['POST'])
def save_edit_sprzet(id):
    data = request.form
    sprzet_to_edit = Sprzet.query.get(id)

    sprzet_to_edit.typ = data['typ']
    sprzet_to_edit.numer_seryjny = data['numer_seryjny']
    sprzet_to_edit.model = data['model']
    sprzet_to_edit.producent = data['producent']

    if data['lokalizacja']:
        lokalizacja = Lokalizacja.query.get(data['lokalizacja'])
        sprzet_to_edit.lokalizacja_id = lokalizacja.id
    else:
        sprzet_to_edit.lokalizacja_id = None

    if data['dzial']:
        dzial = Dzial.query.get(data['dzial'])
        sprzet_to_edit.dzial_id = dzial.id
    else:
        sprzet_to_edit.dzial_id = None

    if data['pracownik']:
        pracownik = Pracownik.query.get(data['pracownik'])
        sprzet_to_edit.pracownik_id = pracownik.id
    else:
        sprzet_to_edit.pracownik_id = None

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/sprzet', methods=['GET'])
def get_sprzet():
    sprzety = Sprzet.query.all()
    return jsonify([sprzet.to_dict() for sprzet in sprzety])

@app.route('/sprzet/delete/<int:id>', methods=['DELETE', 'GET'])
def delete_sprzet(id):
    sprzet_to_delete = Sprzet.query.get(id)
    if sprzet_to_delete:
        db.session.delete(sprzet_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return "Sprzęt nie znaleziony", 404
    
@app.route('/dzialy')
def dzialy():
    lokalizacja_id = request.args.get('lokalizacja_id')

    if lokalizacja_id:
        dzialy = Dzial.query.filter_by(lokalizacja_id=lokalizacja_id).all()
        lokalizacja = Lokalizacja.query.get(lokalizacja_id)
    else:
        dzialy = Dzial.query.all()
        lokalizacja = None

    lokalizacje = Lokalizacja.query.all()
    return render_template('dzial.html', dzialy=dzialy, lokalizacje=lokalizacje, lokalizacja=lokalizacja)


@app.route('/dzial/add', methods=['POST'])
def add_dzial():
    nazwa = request.form['nazwa']
    lokalizacja_id = request.form.get('lokalizacja_id')

    new_dzial = Dzial(nazwa=nazwa, lokalizacja_id=lokalizacja_id)
    db.session.add(new_dzial)
    db.session.commit()

    if lokalizacja_id:
        return redirect(url_for('dzialy', lokalizacja_id=lokalizacja_id))
    else:
        return redirect(url_for('dzialy'))

@app.route('/dzial/delete/<int:id>', methods=['DELETE', 'GET'])
def delete_dzial(id):
    dzial_to_delete = Dzial.query.get(id)
    
    if dzial_to_delete:
        lokalizacja_id = dzial_to_delete.lokalizacja_id

        db.session.delete(dzial_to_delete)
        db.session.commit()

        if lokalizacja_id:
            return redirect(url_for('dzialy', lokalizacja_id=lokalizacja_id))
        else:
            return redirect(url_for('dzialy'))
    else:
        return "Dział nie znaleziony", 404
    
@app.route('/dzial/edit/<int:id>', methods=['GET'])
def edit_dzial(id):
    dzial = Dzial.query.get_or_404(id)
    lokalizacje = Lokalizacja.query.all()
    return render_template('edit_dzial.html', dzial=dzial, lokalizacje=lokalizacje)

@app.route('/dzial/edit/<int:id>', methods=['POST'])
def save_edit_dzial(id):
    dzial = Dzial.query.get_or_404(id)

    previous_lokalizacja_id = dzial.lokalizacja_id
    dzial.nazwa = request.form['nazwa']
    nowa_lokalizacja_id = int(request.form.get('lokalizacja_id')) or None
    dzial.lokalizacja_id = nowa_lokalizacja_id

    sprzet_akcja = request.form.get('sprzet_akcja')

    db.session.commit()
    print(f"Nowa = {nowa_lokalizacja_id}")
    print(f"Stara = {previous_lokalizacja_id}")
    # Jeżeli zmieniono lokalizację działu
    if nowa_lokalizacja_id != previous_lokalizacja_id:
        sprzety = Sprzet.query.filter_by(dzial_id=dzial.id).all()

        if sprzet_akcja == "usun":
            for sprzet in sprzety:
                sprzet.dzial_id = None  # Usuwamy przypisanie działu
        elif sprzet_akcja == "przenies":
            for sprzet in sprzety:
                sprzet.lokalizacja_id = nowa_lokalizacja_id  # Przenosimy lokalizację

        db.session.commit()

    if nowa_lokalizacja_id:
        return redirect(url_for('dzialy', lokalizacja_id=nowa_lokalizacja_id))
    else:
        return redirect(url_for('dzialy'))


@app.route('/lokalizacja', methods=['GET'])
def get_lokalizacja():
    lokalizacje = Lokalizacja.query.all()
    return render_template('lokalizacje.html', lokalizacje=lokalizacje)


@app.route('/lokalizacja/add', methods=['POST'])
def add_lokalizacja():
    nazwa = request.form['nazwa']
    adres = request.form['adres']

    new_lokalizacja = Lokalizacja(nazwa=nazwa, adres=adres)
    db.session.add(new_lokalizacja)
    db.session.commit()
    return redirect(url_for('get_lokalizacja'))

@app.route('/lokalizacja/edit/<int:id>', methods=['GET'])
def edit_lokalizacja(id):
    lokalizacja = Lokalizacja.query.get_or_404(id)
    return render_template('edit_lokalizacja.html', lokalizacja=lokalizacja)

@app.route('/lokalizacja/edit/<int:id>', methods=['POST'])
def save_edit_lokalizacja(id):
    lokalizacja = Lokalizacja.query.get_or_404(id)
    lokalizacja.nazwa = request.form['nazwa']
    lokalizacja.adres = request.form['adres']

    db.session.commit()
    return redirect(url_for('get_lokalizacja'))

@app.route('/lokalizacja/delete/<int:id>', methods=['GET', 'POST'])
def delete_lokalizacja(id):
    lokalizacja = Lokalizacja.query.get_or_404(id)

    # 1. Odpinamy sprzęty od tej lokalizacji
    for sprzet in lokalizacja.sprzety:
        sprzet.lokalizacja_id = None

    # 2. Usuwamy działy przypisane do tej lokalizacji (i odpinamy ich sprzęty)
    for dzial in lokalizacja.dzialy:
        for sprzet in dzial.sprzety:
            sprzet.dzial_id = None
        db.session.delete(dzial)

    # 3. Usuwamy lokalizację
    db.session.delete(lokalizacja)
    db.session.commit()

    return redirect(url_for('get_lokalizacja'))

@app.route('/pracownik', methods=['GET'])
def get_pracownicy():
    pracownicy = Pracownik.query.all()
    return render_template('pracownicy.html', pracownicy=pracownicy)

@app.route('/pracownik/add', methods=['POST'])
def add_pracownik():
    imie = request.form['imie']
    nazwisko = request.form['nazwisko']
    email = request.form.get('email')
    telefon = request.form.get('telefon')

    new_pracownik = Pracownik(imie=imie, nazwisko=nazwisko, email=email, telefon=telefon)
    db.session.add(new_pracownik)
    db.session.commit()
    return redirect(url_for('get_pracownicy'))

@app.route('/pracownik/edit/<int:id>', methods=['GET', 'POST'])
def edit_pracownik(id):
    pracownik = Pracownik.query.get_or_404(id)

    if request.method == 'POST':
        pracownik.imie = request.form['imie']
        pracownik.nazwisko = request.form['nazwisko']
        pracownik.email = request.form.get('email')
        pracownik.telefon = request.form.get('telefon')
        db.session.commit()
        return redirect(url_for('get_pracownicy'))

    return render_template('edit_pracownik.html', pracownik=pracownik)

@app.route('/pracownik/delete/<int:id>', methods=['GET', 'POST'])
def delete_pracownik(id):
    pracownik = Pracownik.query.get_or_404(id)

    for sprzet in pracownik.sprzety:
        sprzet.pracownik_id = None  # odpinamy sprzęt

    db.session.delete(pracownik)
    db.session.commit()
    return redirect(url_for('get_pracownicy'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
