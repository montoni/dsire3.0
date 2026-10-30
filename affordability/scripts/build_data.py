"""Convert a DSIRE Insight "50 States of Energy Affordability" actions workbook into data/data/actions.json.
 
Usage: python scripts/build_data.py path/to/workbook.xlsx [data/data/actions.json]
Requires openpyxl.
"""
import csv, json, os, re, sys
from openpyxl import load_workbook
 
src = sys.argv[1] if len(sys.argv) > 1 else 'workbook.xlsx'
out = sys.argv[2] if len(sys.argv) > 2 else 'data/actions.json'
 
NAMES = {'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','DC':'District of Columbia','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming','PR':'Puerto Rico'}
STATUS = {'E':'Enacted','P1':'Passed one chamber','P2':'Passed both chambers','D':'Failed','V':'Vetoed'}
 
def text(v):
    return '' if v is None else str(v).strip()
 
ws = load_workbook(src).active  # not read_only: hyperlinks are only available in normal mode
rows = []
for row in ws.iter_rows(min_row=2):
    state = text(row[0].value)
    if not state:
        continue  # skip blank rows
    cats = [c.strip() for c in text(row[1].value).split(',') if c.strip()]
    cats = ['Utility Oversight and Cost Recovery' if c == 'Utility Oversight' else c for c in cats]
    cats = list(dict.fromkeys(cats))
    subs = [c.strip() for c in text(row[2].value).split(',') if c.strip()]
    links = [{'text': text(c.value), 'url': c.hyperlink.target if c.hyperlink and c.hyperlink.target else ''}
             for c in row[6:] if text(c.value)]
    srcs = [l['text'] for l in links]
    leg_status = text(row[4].value).capitalize()   # column E
    proc_status = text(row[5].value).capitalize()  # column F
    codes = [m for x in srcs for m in re.findall(r'\((E|P1|P2|D|V)\)\s*$', x)]
    if codes or leg_status:
        typ = 'Legislation'
    elif any(re.search(r'Executive Order', x) for x in srcs):
        typ = 'Executive & other'
    elif any(re.search(r'Docket|Order|Decision|Case|Proceeding|Rule', x, re.I) for x in srcs):
        typ = 'Regulatory proceeding'
    else:
        typ = 'Executive & other'
    rows.append(dict(
        id=f'A{len(rows) + 1:03d}', state=state, state_name=NAMES.get(state, state),
        categories='; '.join(cats), subtopics='; '.join(subs), action_type=typ,
        bill_status=leg_status or (STATUS[codes[0]] if codes else ''),
        proceeding_status=proc_status,
        description=re.sub(r'\s{2,}', ' ', text(row[3].value)),
        sources='; '.join(srcs), source_links=links))
 
with open(out, 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False)
print(f'Wrote {len(rows)} actions ({sum(len(r["source_links"]) for r in rows)} sources, '
      f'{sum(1 for r in rows for l in r["source_links"] if l["url"])} with links) to {out}')
