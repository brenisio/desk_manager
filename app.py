from desk_manager import create_app
from desk_manager.extensions import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
