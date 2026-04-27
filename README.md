# Dragonfly Tables + PocketBase

PocketBase stores one workbook per user.

## 1) Start PocketBase

```bash
docker compose up -d
```

If this is your first run, Docker will pull the image and create `./pb_data`.

Open:

- `http://localhost:8090/` for the app
- `http://localhost:8090/_/` for the PocketBase admin

## 2) First-time PocketBase admin setup

1. Open `http://localhost:8090/_/`.
2. Create the first admin account (email + password).
3. Log into the admin UI.

## 3) Create required collections

### `users`

- Type: **Auth collection**

#### Exact admin UI steps (important)

1. In PocketBase admin (`http://localhost:8090/_/`) click **Collections**.
2. Click **+ New collection**.
3. Choose **Auth collection**.
4. Name it exactly: `users`.
5. Open collection settings for `users` and make sure:

- **Username field is enabled**
- **Username is unique**
- **Password auth is enabled**
- **Create rule is set to `username != ""`**

6. Save.

The app logs in with **username + password** and auto-generates internal email values when registering from the app.

- Username minimum is **2 characters**.
- App registration is for normal users. PocketBase superusers are only for admin access.

#### If your existing `users` records show only email (no username)

You likely created `users` without username enabled.

- Easiest fix: delete/recreate `users` as an **Auth collection** with username enabled.
- Or edit existing `users` collection and ensure a `username` field exists and is unique.
- Existing records with empty username must be updated manually (set a unique username per user).

### `workbooks`

- Type: **Base collection**
- Add field `user`
  - Type: **Relation**
  - Collection: `users`
  - Max select: `1`
  - Required: `true`
  - Unique: `true`
- Add field `db`
  - Type: **JSON**
  - Default: `{}`
  - Required: `true`

## 4) Set collection API rules (`workbooks`)

- List rule: `true`
- View rule: `true`
- Create rule: `user = @request.auth.id`
- Update rule: `user = @request.auth.id`
- Delete rule: `user = @request.auth.id`

## 5) Create test users

Use PocketBase admin UI to create a few records in `users`, or click **Register** in the app if you want self-registration.

If you want **only superusers** to create users, leave the `users` create rule locked down and disable/remove the Register button in `simple_frontend.html`.

When creating users in admin UI, fill at least:

- `username`
- `email`
- `password`
- `passwordConfirm`

If two people try the same username, the app will show `Username already taken.`

## 6) Quick checklist if login fails

- You are logging into the app (`/`) with `users` credentials (not `_superusers`).
- `users` collection is **Auth** type and has username enabled.
- `users` collection has a working Create rule, such as `username != ""`, if you want app registration.
- User record has non-empty unique `username`.
- Password is set for that user.

## 7) Custom weeks / porting old weeks

- Use **Create custom week** to create an older week by date label, for example `Week 06.04.26 - 13.04.26`.
- Use **Create current week** to create the current Monday-based week automatically.
- New weeks copy the previous week's `goal` values for all users.

## 8) Backups

- Click **Export backup JSON** in the app to download the current loaded database as a JSON file.
- The backup includes all loaded `workbooks` data, the active week label, and a timestamp.
- For a full server backup, also copy PocketBase's `pb_data/` directory.

## 9) Running it as a website

- This app works best when the frontend and PocketBase are served from the same origin, like the current PocketBase setup.
- If you host the frontend separately, set `window.__DRAGONFLY_API_BASE__` or the `<meta name="api-base">` value so the page knows where PocketBase lives.
- Keep HTTPS enabled for any public deployment.
- If registration should stay private, remove the **Register** button and keep the `users` create rule locked down.

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
docker compose logs -f pocketbase
docker compose restart pocketbase
docker compose down
```

## Notes

- The frontend is served from `simple_frontend.html` via PocketBase public files.
- The app shows the logged-in user's workbook as editable and others as read-only.
