from bs4 import BeautifulSoup

def extract_additional_info(soup):
    additional_info = {}
    container = soup.select_one('fieldset#fldInformacoesAdicionais')
    if container:
        for row in container.select('table > tbody > tr'):
            cells = row.select('td')
            for i in range(0, len(cells), 2):
                if i + 1 < len(cells):
                    key_tag = cells[i].select_one('label')
                    value_tag = cells[i + 1].select_one('label')
                    if key_tag and value_tag:
                        key = key_tag.text.strip().replace(':', '').lower()
                        value = value_tag.text.strip()
                        if key:
                            additional_info[key] = value
    return additional_info

def extract_movements(soup):
    movements = []
    header = soup.find('th', class_='infraTh', string='Evento')
    if header:
        table = header.find_parent('table')
        if table:
            for row in table.select('tbody > tr'):
                cols = row.select('td')
                if len(cols) == 5:
                    movements.append({
                        'evento': cols[0].get_text(strip=True),
                        'data_hora': cols[1].get_text(strip=True),
                        'descricao': cols[2].get_text(separator=' ', strip=True),
                        'usuario': cols[3].get_text(strip=True),
                        'documentos': cols[4].get_text(strip=True)
                    })
    return movements

def parse_content(soup):
    processes = []
    all_containers = soup.select('fieldset#fldAssuntos')
    if len(all_containers) < 2:
        return processes

    summary_container = all_containers[0]
    subjects_container = all_containers[1]

    cover = {
        'numero_do_processo': summary_container.select_one('#txtNumProcesso').text.strip() if summary_container.select_one('#txtNumProcesso') else '',
        'data_de_autuacao': summary_container.select_one('#txtAutuacao').text.strip() if summary_container.select_one('#txtAutuacao') else '',
        'situacao': summary_container.select_one('#txtSituacao').text.strip() if summary_container.select_one('#txtSituacao') else '',
        'orgao_julgador': summary_container.select_one('#txtOrgaoJulgador').text.strip() if summary_container.select_one('#txtOrgaoJulgador') else '',
        'juiz': summary_container.select_one('#txtMagistrado').text.strip() if summary_container.select_one('#txtMagistrado') else '',
        'classe_da_acao': summary_container.select_one('#txtClasse').text.strip() if summary_container.select_one('#txtClasse') else ''
    }

    subjects = []
    for row in subjects_container.select('table > tbody > tr.infraTrClara'):
        cols = row.select('td')
        if len(cols) == 3:
            subjects.append({
                'codigo': cols[0].text.strip(),
                'descricao': cols[1].text.strip(),
                'principal': cols[2].text.strip()
            })

    parties_container = soup.select_one('fieldset#fldPartes')
    parties = {"requerente": [], "requerido": []}
    if parties_container:
        for row in parties_container.select('table > tbody > tr.infraTrClara'):
            cols = row.select('td')
            if len(cols) == 2:
                requester = cols[0].get_text(separator='\n', strip=True)
                if requester:
                    parties["requerente"].append(requester)
                requested = cols[1].get_text(separator='\n', strip=True)
                if requested:
                    parties["requerido"].append(requested)

    additional_info = extract_additional_info(soup)
    movements = extract_movements(soup)

    process = {
        'capa_do_processo': cover,
        'assuntos': subjects,
        'partes_e_representantes': parties,
        'informacoes_adicionais': additional_info,
        'movimentacoes': movements
    }

    processes.append(process)
    return processes
