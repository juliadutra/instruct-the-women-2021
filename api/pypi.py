import requests

# Referências sobre o uso do requests:
#
# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content

def version_exists(package_name, version):
    try:
        url = f'https://pypi.org/pypi/{package_name}/{version}/json'
        return requests.get(url).status_code == requests.codes.ok
    except:
        return False

def latest_version(package_name):
    try:
        url = f'https://pypi.org/pypi/{package_name}/json'
        r = requests.get(url)
        if(r.status_code == requests.codes.ok):
            return list(r.json()["releases"].keys())[-1]
        else:
            return None
    except:
        return None
