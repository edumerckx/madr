import re


def sanitize(input: str) -> str:
    res = re.sub(r'[^a-zA-ZÀ-ú\s]', '', input)
    res = re.sub(r'\s{2,}', ' ', res)
    return res.strip().lower()
