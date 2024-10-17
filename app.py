from desk_manager import create_app
from desk_manager.dados_iniciais import criar_planos_padrao
from desk_manager.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    criar_planos_padrao(db)

if __name__ == '__main__':
    app.run(debug=True)
