from pathlib import Path
import hashlib,re,json
root=Path(__file__).resolve().parent
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    h,name=line.split('  ',1);p=root/name
    assert p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==h,name
tex=(root/'paper.tex').read_text()
labels=re.findall(r'\\label\{([^}]+)\}',tex)
assert len(labels)==len(set(labels))
assert set(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',tex))<=set(labels)
assert set(re.findall(r'\\cite\{([^}]+)\}',tex))<=set(re.findall(r'\\bibitem\{([^}]+)\}',tex))
print(json.dumps({'status':'PASS','scope':'manifest and TeX references; finite algebra is in reproduce.py'}))
