import requests
import certifi

def consultar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"

    response = requests.get(url, headers={'User-Agent': 'AgroGestor'})
    if response.status_code == 200:
        print(response.json())  # 👈 veja tudo no terminal
        return response.json()
    return None
