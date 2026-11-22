import sys, fitz
p = sys.argv[1]
doc = fitz.open(p)
out = []
for i, page in enumerate(doc):
    out.append(f"\n===== PAGE {i+1} =====\n" + page.get_text())
open(sys.argv[2], "w", encoding="utf-8").write("".join(out))
print(f"pages={len(doc)} chars={sum(len(x) for x in out)}")
