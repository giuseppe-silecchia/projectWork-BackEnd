from app import create_app, db

app = create_app()  # Crea un'istanza dell'app Flask

with app.app_context():  # Crea il contesto dell'app, per effetuare operazioni legate al database
    db.create_all()  # Crea le tabelle nel database in base ai modelli(models) definiti.

if __name__ == '__main__':
    app.run(debug=True)  # Avvia il server Flask in modalità di debug,
