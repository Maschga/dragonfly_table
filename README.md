# Dragonfly Tables

The app now stores everything in a single local JSON file at `data/user.json`.

## 1) Start the app

```bash
docker compose up -d
```

Open `http://localhost:8090/` in the browser.

You can also run it directly with Python:

```bash
python server.py
```

## 2) Accounts and storage

- User accounts and workbook data are stored together in `data/user.json`.
- Passwords are stored as PBKDF2-SHA256 hashes.
- Existing seeded usernames are migrated with a default password equal to the username on first run.
- New registrations use the password you type in the app.

## 3) Working with weeks

- Use **Create current week** to create the current Monday-based week automatically.
- Weeks are shared across the stored workbooks, so a newly created week is saved for all users.
- New weeks copy the previous week's `goal` and `weight` values when available.

## 4) Backups

- Click **Export backup JSON** in the app to download the current loaded database as a JSON file.
- For a full backup, copy `data/user.json`.

## 5) Running it as a website

- The frontend and API should be served from the same origin, which is what `docker compose up -d` does.
- If you host the HTML separately, set `window.__DRAGONFLY_API_BASE__` to the API origin.

## Data shape in `db`

```json
{
  "week1": {
    "ex1": {
      "monday": 1
    }
  }
}
```

## Useful commands

```bash
docker compose logs -f dragonfly
docker compose restart dragonfly
docker compose down
```
