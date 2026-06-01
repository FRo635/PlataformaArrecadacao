Aplicação web "Conecta Causa" (simulador de arrecadação) feita com Django e SQLite.

<h2><b> Rodando a aplicação </b></h2>

<b>Pré-requisitos<b>
* Python 3.x, pip
* (opcional) virtualenv

<b>Instalação</b>
Usando o terminal, execute o seguinte:

``python -m venv venv && source venv/bin/activate``

``pip install -r requirements.txt`` (ou ``pip install django``)

<b>Inicialização</b>

``run.sh``

ou:

``python conectacausa/manage.py runserver 127.0.0.1:8000 --noreload``

E acesse 127.0.0.1:8000 usando um navegador.
