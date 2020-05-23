from common import cache_request
import requests
import PyPDF2
from io import BytesIO
from tqdm import tqdm
from tika import parser

if __name__ == "__main__":
    r = requests.get("https://www.ok.gov/elections/documents/CEB_Physical%20Addresses_%283-19-2020%29.pdf")
    with open("swag.pdf", 'wb') as swag:
        swag.write(r.content)
    f = BytesIO(r.content)

    with open("swag.pdf", 'rb') as swag:
        raw = parser.from_file(swag)
        for line in raw['content'].split("\n"):
            split_line = line.split(" ")
            print(split_line)

