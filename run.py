from app import create_app, db
from app.routes import main

app = create_app()
app.register_blueprint(main)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
