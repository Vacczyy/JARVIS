import webbrowser
import requests
import re

# List of allowed top level domains. Feel free to modify to your comfort.
ALLOWED_TLDS = r"\.(edu|gov|com|net|org|mil)$"

def check_domain(site):
    # Check if the site matches the allowed TLDS
    return re.search(ALLOWED_TLDS, site) is not None

def web_search(search_query):
    # Format the query, feel free to change it to desired search engine.
    search_query = search_query.replace(" ", "+")
    search_query = f'https://www.google.com/search?q={search_query}'

    # Check connection to site
    request = requests.get(search_query)
    if request.status_code == 200:
        print(f"Searching for: {search_query}")
        webbrowser.open(search_query, new=2)
    else:
        f"Unable to connect: ({request.status_code})"

def web_site(site):
    if not check_domain(site):
        print(f"This site's domain is not safe for me to open: {site}")
        return

    if not site.startswith("www."):
        # Add https protocol
        site = f"https://{site}"

    # Check connection to site
    request = requests.get(site, timeout=10)
    if request.status_code == 200:
        print(f"Opening: {site}")
        webbrowser.open(site, new=2)
    else:
        print(f"Unable to connect to {site}: ({request.status_code})")

def web(request_stack):
    def search():
        web_search(request_stack[2])
    def site():
        web_site(request_stack[2])

    function = locals().get(request_stack[1])
    function()
    return False