"""Two-pass PDF build: pass 1 finds where each topic ends on its last page,
pass 2 fills the leftover space with art, quotes, tips, school info and note lines."""
import json, re, subprocess, sys
from playwright.sync_api import sync_playwright

FONTS = sys.argv[1]
OUT = "/home/claude/book/sakura-n5.pdf"
H = f"{FONTS}/fontsource-hind-siliguri-5.3.0/files"
M = f"{FONTS}/fontsource-shippori-mincho-5.3.0/files"
ff = ""
for w in (400, 600, 700):
    for sub in ("bengali", "latin"):
        ff += f"@font-face{{font-family:'Hind Siliguri';font-weight:{w};src:url('file://{H}/hind-siliguri-{sub}-{w}-normal.woff2')}}\n"
for w in (600, 800):
    for sub in ("japanese", "latin"):
        ff += f"@font-face{{font-family:'Shippori Mincho';font-weight:{w};src:url('file://{M}/shippori-mincho-{sub}-{w}-normal.woff2')}}\n"
base = open("/home/claude/book/print.html").read().replace("<style>", "<style>\n" + ff, 1)

PAGE_H = 841.89            # A4 in points
CONTENT_BOTTOM = PAGE_H - 21 * 72 / 25.4   # 12mm page margin + 9mm inner padding

def render(html_path, pdf_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + html_path)
        pg.wait_for_timeout(2500)
        pg.pdf(path=pdf_path, format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>",
               footer_template='<div style="font-size:7px;width:100%;text-align:center;padding-top:5mm;color:#c4577a;font-family:sans-serif"><span class="pageNumber"></span></div>',
               margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"})
        b.close()
        if errs:
            print("page errors:", errs)

# pass 1
p1 = "/home/claude/book/pass1.html"
open(p1, "w").write(base)
render(p1, "/home/claude/book/pass1.pdf")
bbox = subprocess.run(["pdftotext", "-bbox", "/home/claude/book/pass1.pdf", "-"], capture_output=True, text=True).stdout
fill = {}
for m in re.finditer(r'yMax="([\d.]+)">ZQ(\d+)QZ</word>', bbox):
    y, tid = float(m.group(1)), m.group(2)
    rest_mm = (CONTENT_BOTTOM - y) * 25.4 / 72 - 5 - 4
    fill[tid] = round(rest_mm, 1)
print("topics", len(fill), "with space >=34mm:", sum(1 for v in fill.values() if v >= 34))

# pass 2
p2 = "/home/claude/book/pass2.html"
open(p2, "w").write(base.replace("const PRINT=true;", "const PRINT=true;\nwindow.FILL=" + json.dumps(fill) + ";", 1))
render(p2, OUT)
pages1 = subprocess.run(["pdfinfo", "/home/claude/book/pass1.pdf"], capture_output=True, text=True).stdout
pages2 = subprocess.run(["pdfinfo", OUT], capture_output=True, text=True).stdout
print("pages pass1", re.search(r"Pages:\s+(\d+)", pages1).group(1), "pass2", re.search(r"Pages:\s+(\d+)", pages2).group(1))
