from glob import glob
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

files = glob('results/result.*.html')

def parse_addr_line(key, line):
    if not isinstance(line, NavigableString):
        return {}
    else:
        return {key: line.strip()}

def parse_contact_line(line):
    if not isinstance(line, NavigableString):
        return {}
    parsed = line.split(':')
    if len(parsed) == 2:
        k, v = parsed
        return {k.strip(): v.strip()}
    return {}

def parse_contact(h4):
    title = h4.text
    line1 = h4.next_element.next_element
    line2 = line1.next_element.next_element
    if title.endswith('Address:'):
        return {
            'kind': title,
            **parse_addr_line('addr1', line1),
            **parse_addr_line('addr2', line2),
        }
    elif title == 'Contact Information:':
        return {
            'kind': title,
            **parse_contact_line(line1),
            **parse_contact_line(line2),
        }
    else:
        raise ValueError('Encountered unrecognized contact')

def parse_html(file):
    with open(file) as fh:
        soup = BeautifulSoup(fh.read(), "lxml")

    county = soup.find('hr').next_element
    name = county.next_element.next_element

    contact_els = soup.find_all('h4')
    contacts = [parse_contact(contact) for contact in contact_els]

    email_el = soup.find('a')
    email = email_el.text.strip() if email_el else None

    return {
        'county': county.strip(),
        'name': name.strip(),
        'contacts': contacts,
        'email': email,
    }

if __name__ == '__main__':
    js = [parse_html(file) for file in files]

    with open('results/result.json', 'w') as fh:
        json.dump(js, fh)