from desk_manager import create_app
from desk_manager.dados_iniciais import criar_planos_padrao
from desk_manager.models import Cliente
from desk_manager.extensions import db
from datetime import datetime
import os

# Caminho do arquivo de log para registrar a última execução
log_file_path = 'ultima_execucao.txt'


def verificar_e_atualizar_clientes():
    agora = datetime.utcnow()
    data_atual = agora.strftime('%Y-%m')

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            ultima_execucao = file.read().strip()
    else:
        ultima_execucao = None

    if ultima_execucao != data_atual:
        print("Atualizando saldos dos clientes...")

        clientes = Cliente.query.all()
        for cliente in clientes:
            cliente.saldo = 1
        db.session.commit()

        with open(log_file_path, 'w') as file:
            file.write(data_atual)

        print("Saldos atualizados e data de execução registrada.")
    else:
        print("A rotina já foi executada este mês. Nenhuma ação necessária.")


app = create_app()

with app.app_context():
    db.create_all()
    criar_planos_padrao(db)
    verificar_e_atualizar_clientes()

if __name__ == '__main__':
    app.run(debug=True)
