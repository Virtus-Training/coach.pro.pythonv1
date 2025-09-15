import py_compile
import sys

files = [
    "ui/pages/program_page.py",
    "ui/pages/messaging_page.py",
    "ui/pages/billing_page.py",
    "ui/pages/pdf_page.py",
    "ui/pages/progress_page.py",
    "ui/pages/calendar_page.py",
    "ui/pages/clients_page.py",
    "ui/pages/client_detail_page.py",
    "ui/pages/nutrition_page.py",
    "ui/pages/database_page.py",
    "ui/components/design_system/hero.py",
    "ui/components/design_system/buttons.py",
]

ok = True
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print("OK", f)
    except Exception as e:
        ok = False
        print("ERR", f, e)

if not ok:
    sys.exit(1)
