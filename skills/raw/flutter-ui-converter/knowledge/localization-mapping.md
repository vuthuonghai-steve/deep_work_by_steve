# Localization & i18n Mapping (Đa ngôn ngữ)

> **Mục tiêu**: Xử lý text strings theo hệ thống i18n của target project (nếu có).

## 0. Detecting i18n System (CRITICAL - Check First)

**BEFORE enforcing any i18n rules, Agent MUST detect if target project has i18n system:**

```bash
# Check for common i18n patterns
grep -r "S\.of(context)\|context\.l10n\|AppLocalizations\|generated/l10n" lib/ --include="*.dart" -l
find . -name "*.arb"
```

**Decision Tree:**
- **If NO i18n system found** → Skip G5 enforcement, preserve hardcoded text as-is from target
- **If i18n system found** → Apply G5 rules below

## 1. Nhận diện Text Hardcode

Bản thiết kế Source (`tranphueco-redo-AI`) thường chứa các text cứng để làm mẫu (ví dụ: `Text("Đăng nhập")`, `Text("Chào mừng bạn trở lại")`).
Đây là **HÀNH VI BỊ CẤM** khi đưa code sang Target project (`tranphueco`).

## 2. Quy tắc Ánh xạ (Mapping Rules)

Mọi đoạn text hiển thị cho người dùng BẮT BUỘC phải thông qua hệ thống i18n của Target project (thường là `intl` hoặc `easy_localization`).

**Cách xử lý của AI Agent:**
1. Khi lấy code UI từ Source, quét (scan) toàn bộ thuộc tính có truyền `String` (ví dụ: `Text`, `hintText`, `labelText`, `tooltip`).
2. Dịch các text cứng này sang key tương ứng đang được dùng trong Target project.
    - *Ví dụ:* `Text("Đăng nhập")` -> `Text(S.of(context).login)` hoặc `Text(context.l10n.login)` (tùy vào cú pháp dự án đang sử dụng).
3. Nếu text mới trên Source chưa có key tương ứng trong hệ thống i18n của Target (từ mới hoàn toàn), Agent **PHẢI** placeholder bằng một biến và tạo danh sách các từ mới (dưới dạng TODO) để dev bổ sung vào file `.arb` hoặc `.json`, HOẶC sử dụng biến `String` truyền từ ngoài vào. Hạn chế tối đa việc nhúng text cứng, và nếu bắt buộc phải dùng tạm, hãy gắn thẻ `// TODO: i18n`.

## 3. Xử lý Biến Nội suy (Interpolation)

Nếu Source có text như `Text("Xin chào, Nguyễn Văn A")`, Agent cần nhận dạng đây là text nội suy.
- Ở Target, nó sẽ là: `Text(S.of(context).helloUser(state.userName))`
- Không được phép nối chuỗi cứng kiểu `Text("Xin chào, " + state.userName)`.

---

## Reference Data

- **Data file**: `data/localization-dictionary.yaml` — chứa bảng ánh xạ text → i18n key
- **Forbidden patterns**: `data/forbidden-patterns.yaml` → mục `hardcoded_values` (pattern `Text\("[^"]{3,}"\)`)
- **Related knowledge**: `conversion-rules.md` — quy tắc UI-only constraints
