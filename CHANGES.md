# Phase-1 SECURITY cleanup — laundry-management-system

Repo: https://github.com/iambillgates/laundry-management-system (branch `master`, PUBLIC).
Work dir: files here mirror repo-relative paths. Nothing has been pushed.

## What changed per file

### `laundry_project/settings.py` (modified)
- **SECRET_KEY moved to env.** Was a hardcoded `django-insecure-...` literal committed to a public repo. Now read from `os.environ["SECRET_KEY"]`; if it is missing, Django refuses to start with an `ImproperlyConfigured` error that tells the user to copy `.env.example` to `.env` and generate a key.
- **DEBUG moved to env, default `False`.** Was hardcoded `True`. Now `DEBUG = os.environ.get("DEBUG", "False")` (accepts `1`/`true`/`yes`).
- **ALLOWED_HOSTS moved to env, default `localhost,127.0.0.1`.** Was hardcoded and included the leftover CodeSandbox host `znyfdw-8000.csb.app` — that host is **removed** from every default. Set via comma-separated `ALLOWED_HOSTS` env var.
- **LANGUAGE_CODE `en-us` → `id`, TIME_ZONE `UTC` → `Asia/Jakarta`.** The UI is Indonesian; Django-generated messages/dates now match.
- Everything else (INSTALLED_APPS, MIDDLEWARE, DATABASES, validators, static) is byte-identical to the original.

### `laundry_app/views.py` (modified)
- **`dashboard()` is now staff-only.** Added `@login_required`; non-staff logged-in users are redirected to `home` with the message "Halaman dashboard hanya untuk staff." Previously anyone on the internet could open `/dashboard/` and read every customer's name, home address and WhatsApp number.
- **`track_order()` now masks personal data.** Added `_mask_address()` (first 10 chars + `...`) and `_mask_whatsapp()` (first 4 + `****` + last 2 chars). The public tracking page still shows name, service, status and pickup slot, but address/WhatsApp are masked. Masking is done in memory only — nothing is written back to the database, and staff still see the full details on the dashboard and in Django admin. No template change was needed: `track_result.html` already renders `{{ order.address }}` / `{{ order.whatsapp }}`, which now receive the masked values.
- `home()` is untouched.

### `.env.example` (new, repo root)
- Placeholder-only values (no real secrets) for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, with comments on how to generate a key and what each var does.

### `.gitignore` (new, repo root)
- Standard Python/Django ignores: `__pycache__/`, `*.pyc`, `db.sqlite3`, `media/`, `venv/`, `.env`, IDE/OS files. Prevents the database and secrets from being committed by accident.

## Verification done locally
- `python3 -m py_compile` on both edited files: OK.
- `ast.parse` on both files: OK.
- Functional smoke test with Django 5.2.3 (same version as the repo) using stub models/forms + the real `views.py`:
  - `_mask_address("Jl. Merdeka No. 123 Pontianak")` → `"Jl. Merdek..."`; `_mask_whatsapp("081234567890")` → `"0812****90"`.
  - `track_order` rendered page contains the masked values and the full address/number, while the name and status still show.
  - `dashboard`: anonymous user → 302 to login; logged-in non-staff → 302 to home; staff user → 200.
- Real `settings.py` loaded via `django.setup()` with env vars set: `DEBUG`, `ALLOWED_HOSTS` (comma-split), `LANGUAGE_CODE=id`, `TIME_ZONE=Asia/Jakarta` all correct. Without `SECRET_KEY` in env, startup raises `ImproperlyConfigured` with the copy-`.env.example` instruction.

## Needs akbar
1. **Rotate the committed SECRET_KEY.** The old `django-insecure-...` key is in git history forever; removing it from the code does not un-expose it. Generate a new key and set it in the deployment environment (`.env` / host env vars). Do NOT reuse the old value anywhere.
2. **Create a staff user for the dashboard.** The dashboard now requires login + `is_staff`. Create one with `python manage.py createsuperuser` (then tick "staff status" in `/admin/`) or promote an existing user in the admin. Regular customers cannot log in to the dashboard anymore — that is the intended fix.
3. **Note: history still contains the old secret.** A plain new commit with these files does not erase the old key from git history. If the repo must be fully clean, history has to be rewritten (e.g. `git filter-repo`) or the repo re-created — that is a separate, destructive step and needs your explicit go-ahead.
4. **Nothing was deleted.** No files were removed from the repo in this phase (the snapshot-push flow cannot delete tracked files). If `db.sqlite3` ever gets committed, `.gitignore` now prevents it going forward.
