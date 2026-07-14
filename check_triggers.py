#!/usr/bin/env python3
"""
TRIGGER CONSISTENCY CHECK — prevents drift between the three places that name
pipeline step triggers:

  1. PIPELINE (the canonical step->number dict in validate_framework_md.py)
  2. routes.json (the advisory routing map; its keys are the user-facing triggers)
  3. mocktestframework_SKILL.md (the trigger list advertised in the skill description)

Canonical user-facing trigger set = routes.json keys.
Rules enforced:
  - every routes.json trigger must be a known PIPELINE step (no unknown trigger);
  - the SKILL description's trigger list must EQUAL the routes.json trigger set.

PIPELINE may carry extra legacy ALIASES (e.g. Blueprint == MockBlueprint step 6,
MockTestAnalyse == PYQExtract step 5). Those resolve for backward compatibility but
are NOT user-facing triggers, so they are allowed in PIPELINE without appearing in
routes.json / the skill.

Exit 0 = consistent. Exit 1 = drift (prints exactly what diverged). Run it in CI so
the skill list and routing can never silently fall out of sync again.

Usage: python3 check_triggers.py
"""
import json, os, re, sys

ALIASES = {"Blueprint", "MockTestAnalyse"}  # in PIPELINE for resolution; not user-facing


def pipeline_steps():
    from validate_framework_md import PIPELINE
    return set(PIPELINE)


def routes_triggers(path="routes.json"):
    r = json.load(open(path, encoding="utf-8"))
    return set(k for k in r if not k.startswith("_"))


def skill_triggers(path="mocktestframework_SKILL.md"):
    line = next(l for l in open(path, encoding="utf-8") if l.startswith("description:"))
    seg = line.split("framework step —")[1].split("— or asks")[0]
    return set(re.sub(r"^\s*or\s+", "", t.strip()) for t in seg.split(",") if t.strip())


def main():
    pipeline = pipeline_steps()
    routes = routes_triggers()
    skill = skill_triggers()

    errs = []
    unknown = routes - pipeline
    if unknown:
        errs.append(f"routes.json triggers not defined in PIPELINE: {sorted(unknown)}")
    if skill != routes:
        errs.append(
            "SKILL trigger list != routes.json  "
            f"(only-in-skill={sorted(skill - routes)}  only-in-routes={sorted(routes - skill)})"
        )

    if errs:
        print("TRIGGER DRIFT:")
        for e in errs:
            print("  - " + e)
        sys.exit(1)

    print(
        f"TRIGGERS CONSISTENT: {len(routes)} user-facing triggers "
        f"(routes.json == SKILL, all valid PIPELINE steps; "
        f"legacy aliases in PIPELINE: {sorted(ALIASES)})"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
