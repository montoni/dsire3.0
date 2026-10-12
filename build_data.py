"""Convert a DSIRE Insight "50 States of Energy Affordability" actions workbook into data/actions.json.

Usage: python scripts/build_data.py path/to/workbook.xlsx [data/actions.json]
Requires pandas and openpyxl.
"""
import pandas as pd,re,json
from collections import Counter
import sys
src=sys.argv[1] if len(sys.argv)>1 else 'workbook.xlsx'
out=sys.argv[2] if len(sys.argv)>2 else 'data/actions.json'
df=pd.read_excel(src,header=None,skiprows=1)
names={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','DC':'District of Columbia','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming','PR':'Puerto Rico'}
st={'E':'Enacted','P1':'Passed one chamber','P2':'Passed both chambers','D':'Failed','V':'Vetoed'}
rows=[]
for i,r in df.iterrows():
    s=str(r[0]).strip()
    cats=[c.strip() for c in str(r[1]).split(',') if c.strip()]
    cats=['Utility Oversight and Cost Recovery' if c=='Utility Oversight' else c for c in cats]
    cats=sorted(set(cats),key=cats.index)
    subs=[c.strip() for c in str(r[2]).split(',') if c.strip() and str(r[2])!='nan']
    srcs=[str(x).strip() for x in r[4:].tolist() if pd.notna(x) and str(x).strip()]
    codes=[m for x in srcs for m in re.findall(r'\((E|P1|P2|D|V)\)\s*$',x)]
    if codes: typ='Legislation'
    elif any(re.search(r'Executive Order',x) for x in srcs): typ='Executive & other'
    elif any(re.search(r'Docket|Order|Decision|Case|Proceeding|Rule',x,re.I) for x in srcs): typ='Regulatory proceeding'
    else: typ='Executive & other'
    rows.append(dict(id=f'A{i+1:03d}',state=s,state_name=names[s],categories='; '.join(cats),subtopics='; '.join(subs),
        action_type=typ,bill_status=st[codes[0]] if codes else '',description=re.sub(r'\s{2,}',' ',str(r[3]).strip()),sources='; '.join(srcs)))
print(Counter(x['action_type'] for x in rows)); print(Counter(x['bill_status'] for x in rows))

json.dump(rows,open(out,'w'),ensure_ascii=False)
print(f'Wrote {len(rows)} actions to {out}')
