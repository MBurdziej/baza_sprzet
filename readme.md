# Dokumentacja aplikacji zarządzania sprzętem

![obraz](https://github.com/user-attachments/assets/f19933af-48c3-4fc0-ba94-1f225738811c)

## 1. Opis projektu
Aplikacja webowa stworzona w celu zarządzania sprzętem komputerowym w firmie. Umożliwia rejestrowanie sprzętu (laptopy, monitory, drukarki itp.), przypisywanie go do pracowników, lokalizacji oraz działów. Zapewnia pełną edycję, filtrowanie i przejrzystą prezentację danych.

## 2. Technologie
- Python 3
- Flask
- SQLAlchemy (ORM)
- PostgreSQL
- HTML5 + Jinja2
- CSS (własny styl)
- DataTables (JS) – sortowanie, filtrowanie tabel

## 3. Struktura bazy danych

### Tabela: `lokalizacja`
| Kolumna | Typ            | Opis                         |
|---------|----------------|------------------------------|
| id      | SERIAL PRIMARY KEY | ID lokalizacji             |
| nazwa   | VARCHAR(100)   | Nazwa lokalizacji            |
| adres   | VARCHAR(255)   | Adres lokalizacji            |

### Tabela: `dzial`
| Kolumna        | Typ          | Opis                          |
|----------------|--------------|-------------------------------|
| id             | SERIAL PRIMARY KEY | ID działu               |
| nazwa          | VARCHAR(100) | Nazwa działu                 |
| lokalizacja_id | INTEGER      | FK -> lokalizacja(id)         |

### Tabela: `pracownik`
| Kolumna  | Typ           | Opis                         |
|----------|---------------|------------------------------|
| id       | SERIAL PRIMARY KEY | ID pracownika            |
| imię     | VARCHAR(100)  | Imię pracownika               |
| nazwisko | VARCHAR(100)  | Nazwisko pracownika           |
| email    | VARCHAR(100)  | Email (opcjonalnie)           |
| telefon  | VARCHAR(50)   | Telefon (opcjonalnie)         |

### Tabela: `sprzet`
| Kolumna        | Typ           | Opis                          |
|----------------|---------------|-------------------------------|
| id             | SERIAL PRIMARY KEY | ID sprzętu              |
| typ            | VARCHAR(100)  | Typ (np. Laptop, Monitor)     |
| numer_seryjny  | VARCHAR(100)  | Numer seryjny                 |
| model          | VARCHAR(100)  | Model                         |
| producent      | VARCHAR(100)  | Producent                     |
| lokalizacja_id | INTEGER       | FK -> lokalizacja(id)         |
| dzial_id       | INTEGER       | FK -> dzial(id)               |
| pracownik_id   | INTEGER       | FK -> pracownik(id)           |

## 4. Funkcjonalności
- Przeglądanie listy sprzętów z możliwością sortowania i filtrowania
- Dodawanie, edycja i usuwanie sprzętu
- Przypisywanie sprzętu do lokalizacji, działu i pracownika
- Dynamiczne formularze (działy zależne od wybranej lokalizacji)
- Dodawanie, edycja i usuwanie pracowników, działów i lokalizacji
- Okienka potwierdzeń przy usuwaniu informujące o ilości powiązań
- Przy edycji lokalizacji działu, wybór co zrobić ze sprzętem do niego przypisanym

## 5. Struktura plików projektu

```
project_folder/
├── app.py                  # Główny plik aplikacji Flask
├── static/
│   └── style.css           # Wspólny styl dla wszystkich stron
├── templates/
│   ├── index.html
│   ├── add_sprzet.html
│   ├── edit_sprzet.html
│   ├── pracownicy.html
│   ├── edit_pracownik.html
│   ├── lokalizacje.html
│   ├── edit_lokalizacja.html
│   ├── dzial.html
│   └── edit_dzial.html
└── sample_data.sql         # Plik z przykładowymi danymi do bazy
```

## 6. Uruchomienie aplikacji

### Wymagania:
- Python 3
- PostgreSQL

### Kroki:
```bash
# 1. Zainstaluj wymagane biblioteki
pip install flask flask_sqlalchemy flask_migrate

# 2. Stwórz bazę danych
createdb -U postgres sprzet_db

# 3. Uruchom aplikację
python app.py

# 4. (opcjonalnie) Załaduj dane testowe
psql -U postgres -d sprzet_db -f sample_data.sql

# 4. Otwórz w przeglądarce
http://127.0.0.1:5000
```


