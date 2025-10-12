Functions to convert between different casings (like snake_case and PascalCase)

Basic usage:

```python
from utilitaire import Case

print(Case.snake("XHTMLRequest")) # xhtml_request
```

## `Case.snake(key: str) -> str`:
```
kebab-case -> kebab_case
snake_case -> snake_case
PascalCase -> pascal_case
XHTMLRequest -> xhtml_request
UserID -> user_id
```

## `Case.kebab(key: str) -> str`:
```
kebab-case -> kebab-case
snake_case -> snake-case
PascalCase -> pascal-case
XHTMLRequest -> xhtml-request
UserID -> user-id
```

## `Case.camel(key: str, cap_first: bool = False) -> str`:

```
kebab-case -> kebabCase
snake_case -> snakeCase
PascalCase -> pascalCase
XHTMLRequest -> xhtmlRequest
UserID -> userId
```

*for cap_first=True, check out pascal_case docstring

## `Case.pascal(key: str) -> str`:

```
kebab-case -> KebabCase
snake_case -> SnakeCase
PascalCase -> PascalCase
XHTMLRequest -> XhtmlRequest
UserID -> UserId
```
