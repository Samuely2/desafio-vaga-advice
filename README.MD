======================================
  scraper-tjmg (Desafio Advice)
======================================

Este projeto é um web scraper desenvolvido em Python como parte de um desafio técnico. A aplicação automatiza a extração de dados de processos judiciais a partir do site de consulta pública do TJMG (Tribunal de Justiça de Minas Gerais).

--- FUNCIONALIDADES ---

* Busca por Nomes: Realiza buscas automáticas a partir de uma lista de nomes pré-definida.
* Extração Completa: Coleta um conjunto detalhado de dados para cada processo, incluindo:
    - Capa do Processo
    - Assuntos
    - Partes e Representantes (parametrizado para "AUTOR/RÉU" e "REQUERENTE/REQUERIDO")
    - Informações Adicionais
    - Histórico de Movimentações (Eventos)
* Armazenamento Duplo: Salva os dados extraídos de forma persistente em dois formatos:
    - Arquivo JSON: Para fácil visualização e integração com outras aplicações.
    - Banco de Dados SQLite: Para consultas estruturadas e análises de dados.
* Robusto e Confiável: Utiliza esperas inteligentes para lidar com o carregamento de conteúdo dinâmico (JavaScript), garantindo a extração completa dos dados da página.


--- REQUISITOS ---

* Python 3.12 ou superior.
* Git instalado.
* Navegador compatível com Chromium (o Playwright fará o download automaticamente).


--- INSTALAÇÃO E EXECUÇÃO (PASSO A PASSO) ---

Siga estas etapas para configurar e rodar o projeto.

1. Clonar o Repositório:
   Abra seu terminal e clone o projeto usando o link do GitHub.
   
   git clone https://github.com/Samuely2/desafio-vaga-advice.git
   cd desafio-vaga-advice

2. Criar e Ativar um Ambiente Virtual:
   Isso isola as dependências do projeto.
   
   python -m venv .venv

   - No Windows:
     .venv\Scripts\activate

   - No Linux / macOS:
     source .venv/bin/activate

3. Instalar as Dependências:
   Com o ambiente ativado, instale as bibliotecas necessárias.
   
   pip install --upgrade pip
   pip install -r requirements.txt

4. Instalar os Navegadores do Playwright:
   Este comando fará o download do navegador que o scraper utiliza.
   
   python -m playwright install

5. Executar o Scraper:
   Para iniciar a extração, execute o script principal.
   
   python main.py

   - O progresso será exibido no terminal. Ao final, os dados estarão salvos nos arquivos `processos_tjmg.json` e `processos_detalhado.db`.


--- CONFIGURAÇÃO ---

Para alterar lista de nomes a serem pesquisados, edite a variável `nomes` no topo do arquivo `main.py`:

    # Lista de nomes a consultar:
    nomes = [
        "ADILSON DA SILVA",
        "JOÂO DA SILVA MORAES",
        "RICARDO DE JESUS",
        # Adicione ou remova nomes aqui
    ]


--- ESTRUTURA DOS DADOS ---

>> Banco de Dados SQLite (`processos_detalhado.db`)
Os dados são armazenados de forma relacional em várias tabelas para facilitar as consultas SQL:
- processos: Dados da capa do processo.
- assuntos: Assuntos vinculados a cada processo.
- partes: Partes (requerente, réu, etc.) de cada processo.
- movimentacoes: Histórico de eventos de cada processo.

>> Arquivo JSON (`processos_tjmg.json`)
O arquivo contém uma lista de objetos, um para cada nome pesquisado.
Exemplo de um registro:

    {
      "nome_busca": "ADILSON DA SILVA",
      "processos": [
        {
          "capa_do_processo": { "... " },
          "assuntos": [ { "..." } ],
          "partes_e_representantes": {
            "requerente": [ "..." ],
            "requerido": [ "..." ]
          },
          "informacoes_adicionais": { "... " },
          "movimentacoes": [ { "..." } ]
        }
      ]
    }