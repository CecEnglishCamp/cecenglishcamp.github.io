"""Re-run audit and emit cec_audit_report_v2.html (Desktop)."""
import sys, importlib.util
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

spec = importlib.util.spec_from_file_location('_audit', r'C:\Users\cecsu\cecenglishcamp.github.io\_audit.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

# Override report path
m.REPORT = Path(r"C:\Users\cecsu\Desktop\cec_audit_report_v2.html")
m.main()
