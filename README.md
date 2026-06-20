# Gestão Vinicius — Planejamento Semanal Pessoal

Central pessoal de planejamento semanal para acompanhar objetivos, tarefas, finanças e progresso por frente de vida.

## Funcionalidades

- **Painel da Semana**: visão geral, foco principal e dívida de atenção por frente
- **Tarefas Semanais**: cadastro e acompanhamento de tarefas por frente de vida
- **Frentes de Vida**: gestão das áreas de vida com alerta de dívida de atenção
- **Finanças**: registro semanal de gastos e saldo com histórico
- **Progresso**: métricas de conclusão e tempo por semana
- **Revisão de Domingo**: reflexão semanal com nota e aprendizados
- **Agenda Manual**: blocos de tempo por dia da semana

## Como rodar

### Requisitos

- Python 3.11+

### Instalação

```bash
# 1. Crie o ambiente virtual
python -m venv .venv

# 2. Ative o ambiente
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run app.py
```

### Windows (atalho)

Clique duas vezes em `run_app.bat`.

## Estrutura

```
gestao_vinicius/
├── app.py                    # Entrada principal
├── requirements.txt
├── run_app.bat               # Atalho Windows
├── data/
│   └── gestao_vinicius.db   # Banco SQLite local
├── src/
│   ├── database.py           # Inicialização do banco
│   ├── seed.py               # Frentes iniciais
│   ├── calculations.py       # Lógica de cálculos
│   ├── services/             # Camada de serviços
│   │   ├── frente_service.py
│   │   ├── semana_service.py
│   │   ├── tarefa_service.py
│   │   ├── financas_service.py
│   │   ├── revisao_service.py
│   │   └── agenda_service.py
│   └── pages/                # Telas Streamlit
│       ├── painel_semana.py
│       ├── tarefas_semanais.py
│       ├── frentes_de_vida.py
│       ├── financas.py
│       ├── progresso.py
│       ├── revisao_domingo.py
│       └── agenda_manual.py
└── tests/
    └── test_calculations.py
```

## Frentes de vida carregadas automaticamente

- Carreira / EUA
- Doutorado
- Inglês / TOEFL
- Finanças
- Programação / Tecnologia
- Rotina / Equilíbrio
- Trabalho / Aulas
- Acompanhamentos

## Regras de cálculo

### Dívida de atenção
- **ok**: última atividade dentro do limite de dias
- **atenção**: passou do limite
- **crítico**: passou do dobro do limite (ou nunca teve atividade)
- **pausada**: não gera alerta

### Finanças
- Gasto semanal informado manualmente
- Saldo atual informado manualmente
- Variação calculada em relação ao registro anterior
- Média de gasto semanal no mês corrente

### Tempo livre
- Informado manualmente na criação/edição da semana
- Sem integração com Google Calendar nesta versão

## Rodando os testes

```bash
pytest tests/ -v
```

## Nota sobre o banco de dados

O arquivo `data/gestao_vinicius.db` está incluído no repositório intencionalmente,
pois esta é uma aplicação pessoal local.

**Se publicar no GitHub público no futuro:** adicione `data/*.db` ao `.gitignore`
e remova o banco do repositório para não expor dados pessoais.
