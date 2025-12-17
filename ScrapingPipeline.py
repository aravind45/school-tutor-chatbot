import time, json, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0 (educational dataset builder)"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def clean(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text

def parse_problem_page(html):
    soup = BeautifulSoup(html, "html.parser")
    # You must inspect the site’s DOM and adjust selectors:
    question = soup.select_one("h1, .question, .problem")
    answer   = soup.select_one(".answer, .solution, .explanation")
    if not question or not answer:
        return None
    return {
        "instruction": clean(question.get_text(" ")),
        "input": "",
        "output": clean(answer.get_text(" "))
    }

def scrape(urls, out_path="train.jsonl", sleep_s=2):
    with open(out_path, "w", encoding="utf-8") as f:
        for url in urls:
            html = fetch(url)
            row = parse_problem_page(html)
            if row:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            time.sleep(sleep_s)

# scrape(["https://example.com/problem1", "https://example.com/problem2"])
