import json

def save_to_json(dados, file_name="processos_tjmg.json"):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {file_name}")
