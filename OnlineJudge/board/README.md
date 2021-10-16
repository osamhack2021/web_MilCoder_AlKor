# board

## `/api/board/`

### `GET /api/board/?id=[1234]`

Get an article via id.

### `POST /api/board/`

Write a new article.

- `title`: Title
- `content`: Content

### `DELETE /api/board/list/`

Remove an article via id.
Requested user should be super_admin, admin or writer itself.

- `id`: Target article's id

## `/api/board/list/`

### `GET /api/board/list/?problem_id=[PROBLEM_BALLOON]&...`

Get a list of articles.

- `problem_id` (optional)
- ...

