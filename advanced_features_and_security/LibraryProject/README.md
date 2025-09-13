# Groups & Permissions Setup

## Custom Permissions
Defined in `Book` model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
- Viewers → [can_view]
- Editors → [can_view, can_create, can_edit]
- Admins → [can_view, can_create, can_edit, can_delete]

## Usage
Views are protected with `@permission_required`.

Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    ...