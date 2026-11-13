"""Check research scope, links, counts and accidental copying of source secrets.
Never prints a credential value or matching line.
"""
import ast
import csv
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE='c6acf4ecbb5ef6cee238ef206a6923b4e9a6288e'

def main():
    counts={}
    for name,field,minimum in [('source_registry.csv','source_id',25),('competitor_registry.csv','competitor_id',30),
                              ('distribution_channels.csv','channel_id',30),('product_opportunities.csv','product_id',30)]:
        rows=list(csv.DictReader((ROOT/'data'/name).open()))
        assert len(rows)>=minimum and len({r[field] for r in rows})==len(rows),name
        counts[name]=len(rows)
    for path in (ROOT/'docs/research').glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                target=link.split('#')[0]
                assert (path.parent/target).exists(),f'Broken local link in {path.name}: {target}'
    originals=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT).decode().splitlines()
    for path in originals:
        old=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
        assert (ROOT/path).read_bytes()==old,f'Original tracked file changed: {path}'
    # Known fallback literals are inspected only in memory; do not emit them.
    secrets=[]
    for node in ast.walk(ast.parse((ROOT/'freelancehuntNinja.py').read_text())):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('API_TOKEN','FREELANCEHUNT_TOKEN','GROQ_API_KEY') for t in node.targets):
            if isinstance(node.value,ast.Call):
                secrets += [a.value.encode() for a in node.value.args[1:] if isinstance(a,ast.Constant) and isinstance(a.value,str) and len(a.value)>15]
    for folder in ('docs/research','data','research'):
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():
                body=path.read_bytes()
                assert not any(secret in body for secret in secrets),f'Secret copied into artifact: {path.relative_to(ROOT)}'
    for path in (ROOT/'data').glob('*.json'):json.loads(path.read_text())
    for row in csv.DictReader((ROOT/'data/revenue_scenarios.csv').open()):
        assert 0<=float(row['p_month_revenue_ge_2000'])<=1
        assert float(row['hours_median'])<=float(row['capacity_hours_median'])
    result={'catalog_counts':counts,'original_files_unchanged':len(originals),
            'known_source_credential_values_absent_from_research':True,'local_markdown_links_resolve':True}
    (ROOT/'data/artifact_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
