# HTML Sanitization Knowledge

> **Usage**: Load when html-cleaner processes HTML input. Contains semantic tag conversion rules and security stripping patterns.

## 1. Security: Tags to Remove

| Tag | Reason |
|-----|--------|
| `<script>` | JavaScript execution |
| `<style>` | CSS injection vector |
| `<iframe>` | Embedded content execution |
| `<object>` | Plugin content |
| `<embed>` | Plugin content |
| `<form>` | Phishing risk (keep actionless) |
| `<input>` | Form injection |
| `<button>` | Can submit forms |

## 2. Security: Attributes to Remove

### Event Handlers (ALWAYS REMOVE)
```
onclick, onload, onerror, onmouseover, onfocus, onblur,
onchange, onsubmit, onkeydown, onkeyup, onkeypress,
onscroll, onwheel, oncopy, oncut, onpaste
```

### Dangerous Attributes
```
javascript:, data:, vbscript:  (in href, src, action)
style                           (CSS injection)
class                           (tracking)
id                              (anchoring manipulation)
```

## 3. Semantic Tag Conversion

| HTML Tag | Markdown Output |
|----------|-----------------|
| `<h1>` - `<h6>` | `#` - `######` |
| `<p>` | Double newline |
| `<br>` | Double newline |
| `<strong>`, `<b>` | `**text**` |
| `<em>`, `<i>` | `*text*` |
| `<code>` | `` `code` `` |
| `<pre>` | ``` ```code``` ``` |
| `<a href="...">` | `[text](url)` |
| `<img src="...">` | `![alt](src)` |
| `<ul><li>` | `- item` |
| `<ol><li>` | `1. item` |
| `<table>` | Markdown table |
| `<blockquote>` | `> quote` |

## 4. Table Conversion

```html
<table>
  <thead>
    <tr><th>Header 1</th><th>Header 2</th></tr>
  </thead>
  <tbody>
    <tr><td>Cell 1</td><td>Cell 2</td></tr>
  </tbody>
</table>
```

Becomes:
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1  | Cell 2  |
```

## 5. List Nesting

```html
<ul>
  <li>Item 1
    <ul>
      <li>Nested item</li>
    </ul>
  </li>
</ul>
```

Becomes:
```markdown
- Item 1
  - Nested item
```

## 6. Code Block Handling

```html
<pre><code class="language-python">
def hello():
    print("world")
</code></pre>
```

Becomes:
```markdown
```python
def hello():
    print("world")
```
```

## 7. Link Handling

| Scenario | Behavior |
|----------|----------|
| Internal link (`/page`) | Keep as relative |
| External link (`https://`) | Keep full URL |
| `javascript:` protocol | Remove link |
| `data:` URI | Remove link |
| Empty href | Skip link |

## 8. Whitespace Handling

- Collapse multiple spaces to one
- Remove leading/trailing whitespace per line
- Preserve paragraph breaks (double newline)
- Trim code block content

## 9. Error Handling

| Situation | Response |
|-----------|----------|
| Malformed HTML | Use BeautifulSoup parser fallback |
| Unknown tag | Log warning, skip tag |
| Nested tables | Use [TABLE_AMBIGUOUS] marker |
| Empty output | Return error + HITL |
