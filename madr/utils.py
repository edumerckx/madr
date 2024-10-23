import re


def sanitize(input: str) -> str:
    res = re.sub("[^a-zA-ZÀ-ú\s]", "", input)
    res = re.sub('\s{2,}', ' ', res)
    res = re.sub('^\s|\s*$', '', res)
    return res.lower()
