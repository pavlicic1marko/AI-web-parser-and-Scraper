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
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

