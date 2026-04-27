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
- Keep `username` enabled and unique
- The app logs in with **username + password**
- The app auto-generates an internal email value during registration

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

Use PocketBase admin UI to create a few records in `users`, or click **Register** in the app.
If two people try the same username, the app will show `Username already taken.`

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
