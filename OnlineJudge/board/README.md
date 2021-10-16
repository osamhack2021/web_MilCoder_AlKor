# board

## `/api/board/`

### `GET /api/board/?id=[1234]`

Get an article via id, or search and show list.
It uses pagination.

- `id` (optional): article id
- `problem_id` (optional): problem id
- `keyword` (optional): search for title

### `POST /api/board/`

Write a new article.

- `title`: Title
- `content`: Content

### `DELETE /api/board/list/`

Remove an article via id.
Requested user should be super_admin, admin or writer itself.

- `id`: Target article's id

## `/api/board/comment/`

### `GET /api/board/comment/?id=[1234]`

Get a list of comments via article id

- `id`: article id
