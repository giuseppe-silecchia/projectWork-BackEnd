from flask_bcrypt import Bcrypt

from app import create_app, db
from app.initializer import create_default_user, initialize_rooms, create_admin_user

app = create_app()  # Crea un'istanza dell'app Flask
bcrypt = Bcrypt(app)  # Configura Flask-Bcrypt con l'app Flask per abilitare la crittografia delle password.

with app.app_context():  # Crea il contesto dell'app, per effetuare operazioni legate al database
    db.create_all()  # Crea le tabelle nel database in base ai modelli(models) definiti.
    initialize_rooms()
    create_default_user(bcrypt)
    create_admin_user(bcrypt)

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Avvia il server Flask in modalità di debug,
