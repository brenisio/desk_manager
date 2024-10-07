
# Desk Manager

## Descrição
O **Desk Manager** é uma plataforma desenvolvida para a gestão eficiente de espaços de coworking, centralizando o controle de reservas de mesas, gerenciamento de planos de uso e fornecimento de relatórios gerenciais. O sistema visa otimizar o uso dos recursos disponíveis, melhorar a experiência dos clientes e auxiliar na tomada de decisões estratégicas pelos gestores.

## Objetivo
Este projeto tem como objetivo proporcionar um ambiente de fácil gestão para coworkings, permitindo aos gestores controlar as reservas de mesas, vincular clientes a planos de uso, e gerar relatórios de ocupação e cancelamento de reservas.

## Requisitos Funcionais
- Cadastrar clientes, mesas e reservas.
- Registrar a chegada e saída dos clientes em suas mesas.
- Controlar o cancelamento de reservas.
- Cadastrar diferentes tipos de planos de uso e vincular clientes a esses planos.
- Gerar relatórios de uso de mesas e de cancelamento de reservas.

## Requisitos Não Funcionais
- Interface gráfica interativa e intuitiva.
- Resposta rápida ao listar a disponibilidade das mesas.
- Sistema desenvolvido em **Python** com o framework **Flask**.
- Código em conformidade com a notação **PEP8**.
- Utilização de boas práticas, com descrição no arquivo `README`.

## Regras de Negócio
- As reservas devem seguir os períodos estabelecidos (matutino, vespertino e noturno).
- Um cliente só pode reservar uma mesa se tiver saldo suficiente em seu plano.
- O cancelamento de uma reserva deve ser feito com no mínimo 24 horas de antecedência.
- O saldo dos planos é renovado mensalmente e não acumula.

## Membros da Equipe:
- Breno Juliano (23103778)
- Cleverson Borges (23100758)
- Felipe Esmanhotto (23100764)

## Fluxo do Site
### 1. Home
Página inicial da plataforma, onde os gestores podem visualizar as principais funcionalidades do sistema.

### 2. Acessando
Os gestores podem acessar o sistema diretamente, sem a necessidade de login na versão atual.

### 3. Criar Cliente
O gestor pode cadastrar novos clientes, informando nome, CPF e telefone.

## Tecnologias Utilizadas
- **Python** com **Flask**
- **HTML/CSS** para a interface gráfica
