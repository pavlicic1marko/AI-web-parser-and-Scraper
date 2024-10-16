from bs4 import BeautifulSoup


def extract_body(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for scripts_or_style in soup(["scripts", "style"]):
        scripts_or_style.extract()  # remove scripts and style from html

    cleaned_content = soup.get_text(separator="\n")  # get text and separate it by new line
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())  # remove "\n" that do do not start a new line

    return cleaned_content

def split_dom_content_by_length(dom_content, max_lenght=6000):
    return [dom_content[i : i + max_lenght] for i in range(0, len(dom_content), max_lenght)]

