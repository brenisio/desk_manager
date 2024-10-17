from flask import flash

from desk_manager.models import PlanoDeUso


def criar_planos_padrao(db):
    planos_padrao = [
        {'nome_do_plano': 'Bronze', 'quantidade_de_usos': '10'},
        {'nome_do_plano': 'Prata', 'quantidade_de_usos': '25'},
        {'nome_do_plano': 'Ouro', 'quantidade_de_usos': '45'}
    ]

    if not PlanoDeUso.query.first():
        for plano in planos_padrao:
            novo_plano = PlanoDeUso(nome_do_plano=plano['nome_do_plano'], quantidade_de_usos=plano['quantidade_de_usos'])
            db.session.add(novo_plano)
        db.session.commit()
