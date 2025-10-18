scraper-tjmg

Este projeto é um web scraper desenvolvido em Python para automatizar a extração de dados de processos judiciais do site de consulta pública do TJMG (Tribunal de Justiça de Minas Gerais).

-----------------------------------
Funcionalidades
-----------------------------------

- Busca por Nomes: Realiza buscas automáticas a partir de uma lista de nomes pré-definida.
- Extração Completa: Coleta dados detalhados de cada processo, incluindo:
    - Capa do Processo
    - Assuntos
    - Partes e Representantes (parametrizado para "AUTOR/RÉU" e "REQUERENTE/REQUERIDO")
    - Informações Adicionais
    - Movimentações (Eventos)
- Armazenamento Flexível: Salva os dados extraídos em dois formatos:
    - Arquivo JSON: Para fácil visualização e integração com outras aplicações.
    - Banco de Dados SQLite: Para consultas estruturadas e análises de dados.
- Robusto e Confiável: Utiliza esperas inteligentes para lidar com o carregamento dinâmico de conteúdo (JavaScript) do site, garantindo a extração de todos os dados.

-----------------------------------
Requisitos
-----------------------------------

- Python 3.12 ou superior.
- Navegador compatível com Chromium (o Playwright fará o download automaticamente na primeira instalação).

-----------------------------------
Instalação (do zero)
-----------------------------------

Siga os passos abaixo para configurar e executar o projeto.

1. Clonar o repositório:
   git clone <link-do-repositorio>
   cd scraper-tjmg

2. Criar e ativar um ambiente virtual (altamente recomendado):
   python -m venv .venv

   - No Windows:
     .venv\Scripts\activate

   - No Linux / macOS:
     source .venv/bin/activate

3. Instalar as dependências do projeto:
   pip install --upgrade pip
   pip install -r requirements.txt

4. Instalar os navegadores que o Playwright utiliza:
   python -m playwright install

-----------------------------------
Configuração
-----------------------------------

Antes de executar, você pode personalizar os parâmetros de busca no arquivo `config.py` (ou no topo do `main.py`).

# Endereço do site alvo
URL = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

# Lista de nomes a serem pesquisados
NAMES = [
    "ADILSON DA SILVA",
    "JOÂO DA SILVA MORAES",
    "RICARDO DE JESUS"
]

# Caminhos para os arquivos de saída
DB_NAME = "data/processos_tjmg.db"
JSON_FILE = "data/processos_tjmg.json"

- NAMES: Lista de nomes completos para a busca.
- DB_NAME: Nome e caminho do arquivo de banco de dados SQLite que será gerado.
- JSON_FILE: Nome e caminho do arquivo JSON que será gerado.

-----------------------------------
Execução
-----------------------------------

Para iniciar o scraper, execute o script principal a partir do seu terminal:

   python main.py

- Por padrão, o scraper roda em modo headless (sem abrir uma janela de navegador visível).
- O progresso de cada nome consultado será exibido no terminal.
- Ao final da execução, os dados coletados estarão disponíveis nos arquivos definidos na configuração, por exemplo:
    - data/processos_tjmg.json
    - data/processos_tjmg.db

-----------------------------------
Estrutura dos Dados
-----------------------------------

>> Banco de Dados SQLite
Os dados são armazenados de forma relacional em várias tabelas para facilitar as consultas:
- processos: Contém os dados da capa do processo e informações gerais.
- assuntos: Armazena os assuntos vinculados a cada processo.
- partes: Lista as partes (requerente, réu, etc.) de cada processo.
- movimentacoes: Guarda o histórico de eventos de cada processo.

>> Arquivo JSON
O arquivo JSON contém uma lista de objetos, um para cada nome pesquisado.
Exemplo de um registro:
{
  "nome_busca": "ADILSON DA SILVA",
  "processos": [
    {
      "capa_do_processo": { ... },
      "assuntos": [ ... ],
      "partes_e_representantes": { "requerente": [], "requerido": [] },
      "informacoes_adicionais": { ... },
      "movimentacoes": [ ... ]
    }
  ]
}

-----------------------------------
Dicas
-----------------------------------

- Se um nome retornar "Registro não encontrado", verifique se a grafia está correta e se realmente existem processos para aquele nome no site.
- Para visualizar a automação em tempo real (útil para depuração), altere o parâmetro `headless=False` na linha `browser = await p.chromium.launch(headless=False)` dentro do arquivo `main.py`.
- O scraper utiliza pausas estratégicas (asyncio.sleep) para evitar sobrecarregar o servidor do TJMG e reduzir a chance de bloqueios.

-----------------------------------
Licença
-----------------------------------

Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais informações.