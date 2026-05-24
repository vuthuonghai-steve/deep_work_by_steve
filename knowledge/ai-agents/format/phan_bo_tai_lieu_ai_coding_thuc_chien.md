# Phân bổ tài liệu AI và coding trong thực tế: từ một file đến hệ thống nhiều lớp

## Mục tiêu
Tài liệu này nối tiếp hai tài liệu trước và tập trung vào câu hỏi thực hành nhất: khi làm tài liệu cho AI agent và coding workflow, nên **phân bổ nội dung vào đâu, theo format nào, và theo mức phát triển nào của dự án**. Trọng tâm không còn là chỉ hiểu Markdown, YAML hay XML tốt ở điểm nào, mà là biến hiểu biết đó thành một **kiến trúc tài liệu ổn định**, dễ mở rộng, và có thể dùng lâu dài trong dự án thực tế [web:37][web:41][web:71].

Ý tưởng cốt lõi là: không nên xem tài liệu cho agent như một file ghi chú dài, mà nên xem nó như **hệ thống điều khiển hành vi**. Khi nhìn như vậy, việc phân bổ format sẽ bám theo vai trò của thông tin: cái gì là luật, cái gì là ngữ cảnh, cái gì là ví dụ, cái gì là tri thức chuyên miền, và cái gì chỉ được nạp khi cần [web:37][web:41][web:63].

## Nguyên lý phân bổ
Một hệ tài liệu tốt cho AI và coding cần thỏa mãn ba mục tiêu cùng lúc.

- **Rõ ý chí:** agent hiểu đâu là bắt buộc, đâu là ưu tiên, đâu là gợi ý [web:37][web:41].
- **Rõ tải context:** chỉ nạp đúng lượng tri thức cần cho task hiện tại, tránh để root guide trở thành kho lưu trữ tổng [web:16][web:71].
- **Rõ vị trí tài liệu:** con người và agent đều biết nên tìm loại thông tin nào ở đâu, thay vì quét cả repo cho mọi câu hỏi [web:41][web:63].

Từ đó, cách phân bổ hợp lý nhất là **theo lớp thông tin và theo thời điểm nạp**, không chỉ theo chủ đề file. Tài liệu nào cần hiện diện mọi lúc ở root thì phải ngắn, cứng, ít suy đoán; tài liệu nào chỉ cần khi sửa backend, khi test, khi deploy hoặc khi đọc domain thì phải tách riêng và chỉ gọi vào khi cần [web:37][web:63][web:71].

## Mô hình phân bổ theo 4 lớp
Đối với công việc AI + coding, có thể dùng mô hình 4 lớp sau làm khung mặc định.

| Lớp | Mục đích | Nơi đặt | Format chính | Có nên luôn nạp? |
|---|---|---|---|---|
| Lớp 0 | Luật nền, mục tiêu, giới hạn tuyệt đối | `CLAUDE.md` / `AGENT.md` ở root | Markdown ngắn + YAML ngắn + XML ngăn khối [web:37][web:41] | Có |
| Lớp 1 | Quy ước làm việc thường xuyên | `docs/agent/policies/` hoặc `.claude/rules/` | YAML + Markdown ngắn [web:41][web:71] | Thường xuyên, nhưng có chọn lọc |
| Lớp 2 | Tri thức kỹ thuật theo miền | `docs/architecture/`, `docs/domains/`, `docs/runbooks/` | Markdown chủ đạo, có thể kèm YAML snippets [web:41] | Không, chỉ nạp khi cần |
| Lớp 3 | Ví dụ, spec, logs, tickets, fixtures | `docs/examples/`, `specs/`, `tickets/`, `tmp/context/` | XML bọc ngoài + Markdown/YAML bên trong [web:37][web:41] | Không |

Điểm mạnh của mô hình này là nó chuyển câu hỏi “viết ở file nào” thành “thuộc lớp nào”. Khi phân lớp đúng, việc chọn format gần như tự nhiên: luật nền thì phải ngắn và dễ ép hành vi; tài liệu domain thì phải dễ đọc; ví dụ và input thì phải có delimiter mạnh để tránh lẫn với instructions [web:37][web:41][web:63].

## Trường hợp 1: Làm việc trong duy nhất một file
Khi dự án còn nhỏ hoặc bạn cố tình giữ mọi thứ trong một file để giảm chi phí tổ chức, cách hợp lý nhất là dùng **một file Markdown lai**. Điều quan trọng là file đó vẫn phải có phân khu ngữ nghĩa rõ, không phải một bài văn dài có nhiều heading [web:37][web:41].

### Cấu trúc một file khuyến nghị
Một file root duy nhất nên chia theo thứ tự sau.

1. **Mission + hard rules**: 150–300 tokens, đặt đầu file; nên dùng Markdown ngắn và có thể bọc trong XML `<instructions>` để tăng ranh giới [web:37][web:41].
2. **Core constraints**: 200–700 tokens; nên dùng YAML block với các khóa như `must`, `must_not`, `scope`, `acceptance_criteria` [web:41].
3. **Architecture overview**: 200–600 tokens; dùng Markdown prose, chỉ nói bản đồ cấp cao [web:41].
4. **Working workflow**: 150–400 tokens; có thể là Markdown list hoặc YAML ngắn, tùy tính chất lặp lại [web:41].
5. **Examples / edge cases**: 100–300 tokens; chỉ giữ tối thiểu, tốt nhất bọc `<examples>` hoặc `<reference>` [web:37].

### Tỷ lệ phân bổ trong một file
| Thành phần | Tỷ lệ hợp lý |
|---|---:|
| Rules + constraints | 45–60% [web:37][web:41] |
| Architecture/context overview | 20–30% [web:41] |
| Workflow/process | 10–20% [web:41] |
| Examples/reference | 5–10% [web:37] |

Một file duy nhất chỉ hoạt động tốt khi nó là **bảng điều hướng và luật trọng tâm**, không phải kho kiến thức dự án. Nếu phần context, ví dụ hoặc diễn giải vượt lên quá nhiều, file root mất chức năng điều khiển và trở thành tài liệu đọc hiểu chung, lúc đó agent sẽ giảm mức tuân thủ rõ rệt [web:16][web:37][web:41].

## Trường hợp 2: Dự án bắt đầu phát triển
Khi file root bắt đầu vượt vùng hiệu quả, bước đi đúng không phải viết lại tất cả, mà là **tách theo vai trò thông tin**. Đây là giai đoạn chuyển từ “một file lai” sang “root guide + tài liệu vệ tinh” [web:16][web:71].

### Phân bổ file hợp lý ở giai đoạn này
```text
repo/
├─ CLAUDE.md
├─ docs/
│  ├─ architecture/
│  │  ├─ overview.md
│  │  ├─ data-flow.md
│  │  └─ module-map.md
│  ├─ agent/
│  │  ├─ coding-policy.yaml
│  │  ├─ review-policy.yaml
│  │  └─ test-policy.yaml
│  ├─ domains/
│  │  ├─ billing.md
│  │  ├─ auth.md
│  │  └─ notifications.md
│  └─ examples/
│     ├─ api-patterns.md
│     └─ failure-cases.md
```

Ở mô hình này, `CLAUDE.md` chỉ giữ phần Lớp 0 và đường dẫn tham chiếu. Policy mang tính máy móc hoặc có thể lặp lại nên tách sang YAML; tài liệu domain giữ ở Markdown; các ví dụ hoặc failure case để riêng nhằm tránh trộn quá nhiều minh họa vào root guide [web:37][web:41][web:71].

### Quy tắc tách file
- Tách khi một block YAML vượt vùng khoảng 700–1,200 tokens hoặc bắt đầu ôm nhiều domain khác nhau [web:16][web:41].
- Tách khi một section Markdown vượt khoảng 900 tokens và chứa cả rationale, exception, workflow lẫn examples [web:16][web:41].
- Tách examples ngay khi số ví dụ đủ để làm root guide nặng lên; ví dụ là tài sản tốt nhưng rất dễ chiếm chỗ của rules [web:37].
- Giữ root guide như bản đồ, không biến nó thành tài liệu thay thế toàn bộ `docs/` [web:41][web:71].

## Trường hợp 3: Dự án lớn hoặc monorepo
Ở dự án lớn, cách phân bổ hợp lý nhất không còn là “một root file + docs” đơn thuần, mà là **root constitution + scoped rules + domain docs + on-demand task context**. Đây là cấp độ agentic thực thụ, nơi context được nạp theo phạm vi file, module hoặc task thay vì nạp toàn cục [web:37][web:63][web:71].

### Cấu trúc khuyến nghị
```text
repo/
├─ CLAUDE.md                        # constitution / non-negotiables
├─ .claude/
│  ├─ rules/
│  │  ├─ backend.md
│  │  ├─ frontend.md
│  │  ├─ infra.md
│  │  └─ testing.md
│  └─ skills/
│     ├─ api-design.md
│     ├─ migration-safety.md
│     └─ release-checks.md
├─ docs/
│  ├─ architecture/
│  ├─ domains/
│  ├─ runbooks/
│  └─ adr/
├─ specs/
└─ examples/
```

Mô hình này phù hợp vì mỗi loại tri thức đi vào đúng kênh: `CLAUDE.md` giữ luật bất biến; `.claude/rules/` giữ quy tắc theo miền; `docs/` giữ tri thức đọc hiểu; `specs/` và `examples/` giữ bối cảnh tác vụ. Như vậy agent không cần nhớ toàn bộ dự án ở mọi lượt, mà chỉ cần có “hiến pháp” chung cộng với tài liệu cục bộ cho task đang xử lý [web:37][web:63][web:71].

## Phân bổ format theo loại tài liệu
Để làm việc thực dụng, có thể dùng bảng sau như luật mặc định.

| Loại tài liệu | Câu hỏi nó trả lời | Format chính | Vì sao |
|---|---|---|---|
| Root guide (`CLAUDE.md`, `AGENT.md`) | Tôi là ai, phải tuân thủ gì, sửa thế nào cho an toàn? | Markdown lai với YAML block và XML delimiters [web:37][web:41] | Cần vừa dễ đọc vừa phân ranh rules rõ |
| Policy files | Những quy ước lặp lại nào phải thi hành? | YAML [web:41] | Schema rõ, phù hợp rule/checklist |
| Architecture docs | Hệ thống được tổ chức ra sao? | Markdown [web:41] | Dễ giải thích, dễ vẽ bản đồ khái niệm |
| Domain docs | Nghiệp vụ này hoạt động thế nào? | Markdown + bảng + snippets [web:41] | Domain cần prose và ví dụ |
| Task context / specs | Task này yêu cầu gì? | XML bọc ngoài + Markdown/YAML bên trong [web:37] | Tách lệnh, dữ liệu, tiêu chí nghiệm thu |
| Examples / tests | Một pattern đúng trông ra sao? | Markdown code blocks, đôi khi XML wrapper [web:37][web:41] | Dễ đọc, dễ đối chiếu |

## Mẫu root guide tối ưu cho AI và coding
Một root guide tốt cho công việc coding thường nên giữ bốn vùng cố định.

### 1. Identity và success definition
Phần này trả lời: dự án này là gì, mục tiêu thành công là gì, agent được tối ưu theo tiêu chí nào. Đây là phần giúp agent không chỉ sửa code đúng cú pháp mà còn đúng chủ đích sản phẩm [web:63][web:71].

### 2. Non-negotiables
Đây là các luật không được thương lượng: an toàn migration, backward compatibility, test expectations, secret handling, giới hạn dependency, quy tắc sửa file generated. Phần này nên rất ngắn, rất cứng, và có thể đặt trong YAML hoặc XML-wrapped instructions [web:37][web:41].

### 3. Working map
Phần này cho agent biết nên đi đâu để lấy thêm tri thức: backend rules ở đâu, frontend rules ở đâu, domain billing đọc file nào, spec task ở đâu. Đây là “bản đồ context” quan trọng hơn nhiều so với việc cố nhét hết thông tin vào root [web:37][web:63][web:71].

### 4. Interaction protocol
Phần này quy định agent nên lập kế hoạch thế nào, khi nào hỏi lại, khi nào được phép sửa nhiều file, khi nào phải đề xuất trước khi chạm code. Đây là phần cực kỳ hữu ích cho coding agents vì nó chuyển hành vi từ reactive assistant sang controlled agent [web:41][web:71].

## Cách phân ranh khu vực tài liệu
Khi số lượng tài liệu tăng lên, nên phân ranh theo **mục đích sử dụng** chứ không chỉ theo team sở hữu.

- **Khu vực điều khiển:** `CLAUDE.md`, `.claude/rules/`, `agent/` policies; ưu tiên YAML và delimiter rõ [web:37][web:41].
- **Khu vực tri thức:** `docs/architecture/`, `docs/domains/`, `adr/`; ưu tiên Markdown [web:41].
- **Khu vực tác vụ:** `specs/`, `tickets/`, `runbooks/`; dùng XML hoặc sectioned Markdown để tách task/context/criteria [web:37].
- **Khu vực minh họa:** `examples/`, `patterns/`, `fixtures/`; để riêng nhằm hỗ trợ retrieval khi cần, tránh kéo cả kho ví dụ vào root [web:37][web:41].

Phân ranh kiểu này giúp agent trả lời ba câu hỏi rất nhanh: “tôi phải tuân thủ gì”, “tôi cần hiểu thêm gì”, và “task hiện tại yêu cầu gì”. Nếu ba câu này không được trả lời từ cấu trúc thư mục và format tài liệu, dự án sẽ sớm quay lại tình trạng root file phình to [web:63][web:71].

## Budget thực hành khuyến nghị
Dưới đây là budget thực dụng cho hệ tài liệu AI + coding.

| Thành phần | Budget hợp lý |
|---|---:|
| `CLAUDE.md` / root guide | 900–2,000 tokens [web:16][web:41] |
| Mỗi policy YAML | 200–800 tokens [web:16][web:41] |
| Mỗi doc architecture/domain | 400–1,500 tokens cho overview; dài hơn thì chia file [web:16][web:41] |
| Mỗi task spec | 300–1,200 tokens tùy độ phức tạp [web:16][web:37] |
| Examples giữ trong root | 100–300 tokens tối đa [web:37] |

Các budget này không nhằm giới hạn sáng tạo, mà để buộc hệ tài liệu giữ được tính module. Một agent tốt không cần root guide biết mọi thứ; nó cần root guide biết **dẫn đúng chỗ** và **giữ đúng luật** [web:37][web:63][web:71].

## Quy trình triển khai thực tế
Có thể triển khai theo ba bước để tránh đập đi xây lại.

1. **Ổn định root guide**: giữ lại mission, hard rules, working map, interaction protocol; loại bỏ prose dài và examples nặng [web:16][web:41].
2. **Tách policy khỏi prose**: đưa constraints, checklists, acceptance criteria sang YAML theo domain hoặc theo workflow [web:41].
3. **Tách context theo nhu cầu nạp**: kiến trúc, domain, spec, logs, examples đi vào file riêng; chỉ tham chiếu hoặc import khi task cần [web:37][web:71].

Làm theo thứ tự này giúp dự án không rơi vào bẫy “cải tổ format nhưng không cải tổ luồng nạp context”. Format chỉ phát huy hiệu quả khi đi cùng kiến trúc nạp thông tin đúng lúc [web:37][web:63].

## Phân bổ tối ưu mặc định
Nếu cần một câu trả lời gọn để áp dụng ngay, đây là bố cục mặc định nên dùng cho dự án AI + coding.

- **Root file:** Markdown làm khung, XML để chặn biên giữa instructions/context/examples, YAML cho rules và constraints [web:37][web:41].
- **Rules theo domain:** YAML hoặc Markdown ngắn có cấu trúc, đặt trong thư mục riêng và nạp theo phạm vi [web:41][web:71].
- **Architecture và nghiệp vụ:** Markdown, chia theo module hoặc domain thay vì dồn vào một file lớn [web:41].
- **Task specs và runbooks:** XML-wrapped sections hoặc Markdown sectioned chặt, có acceptance criteria rõ [web:37].
- **Examples:** để file riêng, chỉ giữ ví dụ tối thiểu trong root guide [web:37][web:41].

## Kết luận áp dụng
Phân bổ hợp lý nhất cho tài liệu AI và coding không phải là “chọn một format đúng”, mà là xây một **kiến trúc tài liệu nhiều lớp**: root guide điều khiển, policy files ép quy tắc, domain docs giải thích, task context nạp theo nhu cầu, examples chỉ gọi khi cần. Trong hệ đó, Markdown giữ vai trò giao tiếp và giải thích, YAML giữ vai trò schema hành vi, còn XML giữ vai trò phân ranh ngữ nghĩa [web:37][web:41][web:63][web:71].

Khi dự án còn nhỏ, có thể gói tất cả trong một file Markdown lai. Khi dự án lớn lên, phải chuyển sang cấu trúc nhiều file theo lớp thông tin; nếu không, tài liệu sẽ tăng nhanh hơn khả năng agent hiểu và tuân thủ nó [web:16][web:37][web:71].
EOF && echo done
