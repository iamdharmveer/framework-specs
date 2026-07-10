# Drop in your real files, then generate the manifest

Copy your 14 real files into the repo root (same folder as bootstrap.py):
  11x Framework_*.md, validate_framework_md.py, explain_audit_gate.py, explain_engine.py

Then:  python3 gen_manifest.py     # builds MANIFEST.json from YOUR real bytes

CONFIRM before release: open routes.json and verify, for each step trigger:
  (a) the trigger name matches exactly what you type to run the step, and
  (b) the file list includes the spec PLUS every spec/script it depends on
      (e.g. MockDeliver depends on Framework_DeliveryFooter.md).
The manifest + gate only guarantee "full, correct files" for what routes.json lists.
