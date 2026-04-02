# RangerSuite

Mock websites for design exploration.

## Included concepts

- `mockups/documentation-redesign`: earlier documentation hub concept.
- `mockups/account-settings-redesign`: earlier account settings concept.
- `mockups/rangersuite-redesign`: multi-page exploratory concept set.
- `mockups/preview.html`: consolidated launcher for the active mockups.
- `mockups/updated-pages`: refreshed previews for:
  - Documentation (`documentation.html`)
  - Account (`account.html`)
  - Survey Demographics (`survey-demographics.html`)
  - Facility Maintenance (`facility-maintenance.html`)
  - Quick launcher (`preview.html`)
- `mockups/user-management-portal`: redesigned user management portal pages based on the provided settings/users template:
  - User detail (`user-detail.html`)
  - Subscriber detail (`subscriber-detail.html`)
  - Maintenance (`maintenance.html`)
  - Quick launcher (`preview.html`)

## Download-ready Exports

Download HTML files under `mockups/*/downloads/` are generated artifacts and are not tracked.

Run:

```bash
python3 scripts/export_mockup_downloads.py
```

This rebuilds standalone HTML files with CSS inlined for:

- `mockups/updated-pages/downloads/`
- `mockups/user-management-portal/downloads/`

## Merge Guardrails

- Edit the source HTML/CSS files, not the generated `downloads/` copies.
- Run `python3 scripts/check_conflict_markers.py` before committing if you want a manual check.
- Optional local hook setup:

```bash
git config core.hooksPath .githooks
```
