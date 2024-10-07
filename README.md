
# Desk Manager

## Descrição
O **Desk Manager** é uma plataforma projetada para ajudar você, gestor de coworking, a organizar e otimizar a gestão do seu espaço. Centralizamos o controle de reservas de mesas, o gerenciamento de planos de uso e fornecemos relatórios detalhados que apoiam sua tomada de decisões. Tudo isso para garantir que seu espaço seja utilizado da melhor maneira possível, melhorando tanto sua operação quanto a experiência dos seus clientes.

## Objetivo
Este projeto foi desenvolvido para facilitar o seu dia a dia na gestão de coworkings. Com ele, você poderá cadastrar clientes e mesas, controlar reservas, vincular clientes a diferentes planos de uso, e acessar relatórios que ajudam a acompanhar a ocupação das mesas e cancelamentos de reservas.

## Fluxo do Sistema
### 1. Home
Aqui, você encontrará as principais funcionalidades do sistema, oferecendo uma visão geral das operações.

### 2. Acesso ao Sistema
O acesso ao Desk Manager é simples. Nesta versão, você poderá acessar o sistema diretamente, sem a necessidade de login, tornando o processo mais rápido e prático.

### 3. Gestão de Clientes (CRUD Cliente)
Cadastre novos clientes facilmente, informando o nome, CPF e telefone. Você também pode buscar, editar, listar ou até excluir clientes do sistema, mantendo o cadastro sempre atualizado.

### 4. Gestão de Mesas (CRUD Mesa)
Registre as mesas do coworking, com identificação simples por número. Além disso, você pode editar, buscar, listar ou excluir as mesas, facilitando o controle de disponibilidade.

### 5. Gestão de Planos (CRUD Plano)
Crie diferentes planos de uso para seus clientes, definindo o nome do plano e a quantidade de usos disponíveis. Assim como nas outras áreas, é possível editar, buscar, listar ou excluir planos conforme a necessidade.

## Requisitos Funcionais
- Cadastrar clientes, mesas e reservas.
- Registrar a chegada e saída dos clientes nas mesas.
- Controlar cancelamentos de reservas.
- Vincular clientes a diferentes tipos de planos.
- Gerar relatórios de uso de mesas e cancelamentos.

## Requisitos Não Funcionais
- Interface gráfica amigável e de fácil navegação.
- Resposta rápida ao listar a disponibilidade de mesas.
- Desenvolvido em **Python** com o framework **Flask**.
- Código seguindo boas práticas e a notação **PEP8**.

## Regras de Negócio
- As reservas seguem os períodos matutino (7h-11h59), vespertino (12h-16h59) e noturno (17h-21h59).
- Um cliente só pode reservar uma mesa se tiver saldo disponível em seu plano.
- O cancelamento deve ser feito com no mínimo 24 horas de antecedência.
- O saldo de planos é renovado mensalmente, sem acúmulo de meses anteriores.

## Tecnologias Utilizadas
- **Python** com **Flask**
- **HTML/CSS** para a interface gráfica
