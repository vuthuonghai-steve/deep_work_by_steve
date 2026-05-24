# Hướng dẫn chọn format cho file hướng dẫn AI Agent

## Mục tiêu tài liệu
Tài liệu này giải thích cách dùng Markdown, YAML và XML-like tags trong các file như `CLAUDE.md`, `AGENT.md`, `SYSTEM.md` hoặc các prompt dùng cho AI coding agents. Mục tiêu không phải là chọn một định dạng “tốt nhất tuyệt đối”, mà là chọn đúng định dạng cho đúng loại thông tin để mô hình hiểu rõ ý chí của người dùng, giảm nhiễu context, và tăng mức tuân thủ hướng dẫn [cite:37][cite:41].

Điểm cốt lõi là LLM không “đọc” định dạng theo kiểu trình biên dịch, mà phản ứng theo các mẫu đã gặp trong dữ liệu huấn luyện và theo ranh giới cấu trúc mà prompt thể hiện. Vì vậy, format tốt là format giúp mô hình nhận ra: đâu là quy tắc bắt buộc, đâu là dữ liệu tham chiếu, đâu là ví dụ, và đâu là phần giải thích bối cảnh [cite:37][cite:41].

## Vấn đề cần giải quyết
Trong các dự án lớn, file hướng dẫn chung dễ phình ra thành hàng trăm dòng, trộn lẫn nhiều loại nội dung: mục tiêu, ràng buộc, ngữ cảnh kiến trúc, tiêu chuẩn code, checklist, ví dụ, anti-pattern, và quy trình phối hợp. Khi mọi thứ đều được viết bằng cùng một kiểu Markdown phẳng, mô hình có thể hiểu sai mức độ ưu tiên, trộn context với instruction, hoặc coi những luật quan trọng như thông tin tham khảo thông thường [cite:37][cite:41].

Vấn đề ở đây không chỉ là “quá dài”, mà là “thiếu phân lớp ngữ nghĩa”. Một agent mạnh không chỉ cần nhiều thông tin; nó cần biết thông tin nào là mệnh lệnh, thông tin nào là dữ liệu, thông tin nào là ví dụ, và thông tin nào chỉ dùng khi gặp đúng hoàn cảnh [cite:37][cite:41].

## Nguyên lý chọn format
Format nên được xem như công cụ kích hoạt đúng vùng tri thức đã được mô hình học trong quá trình training. Một cấu trúc giống tài liệu kể chuyện sẽ đánh thức hành vi đọc hiểu tự do; một cấu trúc giống file cấu hình sẽ đánh thức hành vi tuân thủ tham số; một cấu trúc có delimiter rõ sẽ giúp mô hình phân biệt lệnh với dữ liệu tham chiếu [cite:37][cite:41].

Vì vậy, cách tiếp cận hiệu quả không phải là “viết cứng nhắc hơn”, mà là “mã hóa ý định tốt hơn”. Khi ý định được thể hiện bằng đúng hình thức, mô hình sẽ bớt phải suy đoán, giảm lỗi diễn giải, và dùng attention hiệu quả hơn trên đúng phần cần thiết [cite:37][cite:41].

## Bản chất khác nhau giữa các format

### Markdown
Markdown mạnh ở khả năng trình bày cho con người. Nó phù hợp với giải thích kiến trúc, rationale, onboarding, walkthrough, quyết định thiết kế, ví dụ, bảng so sánh, và các phần cần đọc tuần tự như một tài liệu kỹ thuật [cite:41].

Tuy nhiên, Markdown thuần có nhược điểm là nhiều phần nhìn giống nhau về mặt cấu trúc đối với LLM: heading, bullet list, note, warning, exception, policy có thể cùng tồn tại nhưng không có schema đủ chặt để mô hình luôn phân biệt đúng mức ưu tiên. Nếu dùng Markdown cho cả luật cứng lẫn diễn giải dài dòng, mô hình dễ xem luật như “guidance mềm” thay vì “ràng buộc phải tuân thủ” [cite:37][cite:41].

### YAML
YAML mạnh ở vai trò cấu hình. Nó phù hợp khi cần biểu diễn các trường có tên rõ ràng như `must`, `must_not`, `tech_stack`, `allowed_paths`, `forbidden_patterns`, `review_checklist`, `output_contract`, hoặc `routing_rules`. Cấu trúc key-value và phân cấp bằng indentation giúp mô hình nhận ra đây là dữ liệu có schema, không phải đoạn văn tường thuật [cite:41].

YAML giải quyết tốt bài toán “gọi đúng tên vấn đề”. Khi một ràng buộc được đặt dưới khóa `must_not`, mô hình không cần suy luận nhiều như khi gặp một bullet trong phần “Notes”. Nhờ vậy, YAML đặc biệt hữu ích để đánh thức tri thức kiểu cấu hình, policy, mapping và checklist có tính máy móc [cite:41].

Nhược điểm của YAML là dễ gãy vì indentation, khó đọc hơn với nội dung dài, và không phù hợp cho phần giải thích giàu ngữ cảnh. Nếu nhồi quá nhiều prose vào YAML, tài liệu trở nên nặng nề, khó bảo trì, và mất lợi thế rõ ràng ban đầu [cite:41].

### XML-like tags
Anthropic khuyến nghị dùng XML tags để tách các phần khác nhau của prompt khi có nhiều thành phần như context, instructions và examples. Theo tài liệu của Anthropic, XML tags giúp tăng clarity, accuracy, flexibility và parseability vì mô hình dễ xác định ranh giới từng khối thông tin hơn [cite:37].

XML-like tags giải quyết đặc biệt tốt bài toán “đây là dữ liệu, không phải lệnh”. Khi bọc tài liệu tham chiếu trong `<context>`, ví dụ trong `<example>`, và luật trong `<instructions>`, mô hình ít nhầm dữ liệu chèn vào là một phần của chỉ dẫn điều khiển. Đây là cách rất mạnh để giảm trộn lẫn giữa input và instruction trong agent workflows [cite:37][cite:41].

Nhược điểm của XML là dài token hơn, kém tự nhiên hơn với người viết thông thường, và nếu lạm dụng quá nhiều tag lồng nhau thì tài liệu trở nên rối. XML hiệu quả nhất khi dùng làm delimiter và semantic boundary, không phải để thay thế toàn bộ văn bản bằng một cây markup phức tạp [cite:37][cite:41].

## Giải pháp nào xử lý vấn đề gì
| Vấn đề | Format phù hợp | Vì sao hiệu quả |
|---|---|---|
| Luật bắt buộc bị hiểu như gợi ý | YAML hoặc YAML block trong Markdown | Key như `must`, `must_not`, `required` làm rõ tính bắt buộc [cite:41] |
| Context và instruction bị trộn | XML tags | Tag giúp phân định ranh giới dữ liệu, ví dụ và chỉ dẫn [cite:37][cite:41] |
| Kiến thức dự án khó đọc với con người | Markdown | Phù hợp cho prose, giải thích, bảng, ví dụ, hướng dẫn tuần tự [cite:41] |
| Prompt dài, khó bảo trì | Hybrid | Tách đúng loại thông tin vào đúng format giảm nhiễu và tăng khả năng sửa cục bộ [cite:37][cite:41] |
| Cần trích xuất, parse hậu kỳ | XML hoặc YAML | Cấu trúc rõ giúp kiểm tra tự động và post-processing dễ hơn [cite:37][cite:41] |

## Khi nào nên dùng từng loại

### Nên dùng Markdown khi
- Cần giải thích lý do kiến trúc, trade-off, rationale, glossary, onboarding, coding style narrative [cite:41].
- Tài liệu hướng tới cả con người và agent, và phần chính là tri thức cần đọc hiểu chứ không phải policy machine-readable [cite:41].
- Cần trình bày bảng, code block, ví dụ theo dòng chảy tự nhiên [cite:41].

### Nên dùng YAML khi
- Nội dung là policy, config, checklist, routing, constraints, capability matrix, permission map, hoặc contract đầu ra [cite:41].
- Cần giảm mơ hồ bằng tên khóa rõ ràng như `priority`, `scope`, `allowed_tools`, `stop_conditions`, `acceptance_criteria` [cite:41].
- Muốn agent dễ map từ ý định sang hành vi thông qua một schema lặp lại ổn định giữa nhiều dự án [cite:41].

### Nên dùng XML tags khi
- Cần phân tách instruction, examples, context, input docs, test cases, scratch data trong cùng một file hoặc cùng một message [cite:37][cite:41].
- Muốn chặn tình trạng mô hình nhầm dữ liệu tham chiếu là lệnh điều khiển, đặc biệt trong quy trình có RAG, nhiều đoạn tài liệu, hoặc nội dung người dùng cung cấp vào prompt [cite:37][cite:41].
- Cần mô hình hoặc hệ thống hậu kỳ dễ parse các phần đầu ra như `<analysis>`, `<plan>`, `<final_answer>` [cite:37].

## Vì sao hybrid thường là lựa chọn tốt nhất
Tài liệu của OpenAI khuyến nghị kết hợp Markdown và XML để làm rõ ranh giới logic trong prompt; Markdown hữu ích cho section và hierarchy, còn XML giúp phân định nơi một phần nội dung bắt đầu và kết thúc [cite:41]. Tài liệu của Anthropic cũng nhấn mạnh XML tags đặc biệt hữu ích khi prompt có nhiều thành phần như context, instructions và examples [cite:37].

Từ đó, cách làm hiệu quả nhất cho `CLAUDE.md` hoặc `AGENT.md` thường là hybrid: dùng Markdown cho phần giải thích, YAML cho phần policy/config, và XML tags cho vùng phân cách ngữ nghĩa giữa khối lệnh, khối dữ liệu và khối ví dụ [cite:37][cite:41]. Cách này vừa dễ đọc với con người, vừa tận dụng đúng “mẫu quen thuộc” mà mô hình đã học từ dữ liệu huấn luyện [cite:37][cite:41].

## Mẫu thiết kế khuyến nghị

### Mẫu 1: File gốc ngắn, nhiều ý định rõ
Phù hợp cho file root-level như `CLAUDE.md` dài khoảng 150–250 dòng. Mục tiêu là để agent hiểu được bản đồ điều hướng của dự án, không phải nhét toàn bộ tri thức vào một chỗ.

```md
# Project Guide

## Purpose
Mô tả ngắn dự án, domain, và định nghĩa thành công.

<instructions>
Luôn ưu tiên an toàn thay đổi, giữ backward compatibility, và chỉ sửa đúng phạm vi task.
</instructions>

## Architecture
Mô tả kiến trúc mức cao và link/import tới tài liệu chi tiết.

```yaml
constraints:
  must:
    - preserve public APIs unless task explicitly allows breaking changes
    - write tests for changed business logic
  must_not:
    - edit generated files directly
    - introduce new dependencies without justification
```
```

Mẫu này hiệu quả vì mỗi loại thông tin ở đúng hình thức: prose cho hiểu biết chung, XML cho chỉ dẫn trọng tâm, YAML cho luật cứng và checklist [cite:37][cite:41].

### Mẫu 2: Tài liệu chuyên biệt theo domain
Phù hợp cho monorepo hoặc dự án lớn. File root chỉ giữ nguyên tắc chung; mỗi domain có file riêng như `backend.rules.md`, `frontend.rules.md`, `infra.rules.md`.

Trong từng file domain, có thể dùng Markdown cho giải thích nghiệp vụ và YAML cho rule map. Điều này giúp agent chỉ nạp kiến thức đúng ngữ cảnh thay vì mang cả dự án vào một context duy nhất, giảm nhiễu và thời gian xử lý [cite:41].

### Mẫu 3: Prompt có tài liệu tham chiếu đi kèm
Phù hợp khi agent nhận thêm spec, ticket, logs, hoặc user story trong từng phiên làm việc.

```xml
<task>
Refactor payment retry flow.
</task>

<context>
... trích đoạn kiến trúc và constraint liên quan ...
</context>

<examples>
... ví dụ request/response mong muốn ...
</examples>

```yaml
acceptance_criteria:
  - retries are idempotent
  - max retry count remains configurable
  - existing API contract is preserved
```
```

Mẫu này hiệu quả vì tách ranh giới dữ liệu và chỉ dẫn, đồng thời biến tiêu chí nghiệm thu thành cấu trúc dễ kiểm tra [cite:37][cite:41].

## Làm thế nào là đúng
- Dùng format để biểu diễn đúng bản chất thông tin: policy thì có schema, giải thích thì ở dạng prose, delimiter thì dùng tag [cite:37][cite:41].
- Dùng tên khóa và tên tag mang nghĩa nghiệp vụ rõ ràng như `constraints`, `acceptance_criteria`, `forbidden_patterns`, `<context>`, `<instructions>`, `<examples>` [cite:37][cite:41].
- Giữ một đơn vị thông tin quan trọng trên một dòng hoặc một mục độc lập để agent dễ trỏ lại và dễ sửa cục bộ [cite:37][cite:41].
- Đặt luật ưu tiên cao ở khu vực nổi bật, ngắn gọn, không trộn với phần diễn giải dài [cite:41].
- Duy trì tính nhất quán giữa các file; cùng một ý nghĩa nên dùng cùng một khóa, cùng một tag, cùng một mẫu trình bày [cite:37].

## Làm thế nào là sai
- Viết toàn bộ file bằng Markdown narrative rồi kỳ vọng agent tự suy ra đâu là luật cứng, đâu là ghi chú mềm [cite:41].
- Nhét mọi thứ vào YAML, bao gồm cả giải thích dài, khiến tài liệu mất khả năng đọc hiểu và khó bảo trì [cite:41].
- Dùng XML tags nhưng tên tag mơ hồ như `<data1>`, `<part2>`, `<misc>`, khiến tag mất giá trị ngữ nghĩa [cite:37].
- Không nhất quán format giữa các file: hôm nay `must_not`, ngày mai `avoid`, hôm khác lại `never_do`; điều đó làm giảm khả năng agent học pattern nội bộ của dự án [cite:37][cite:41].
- Dùng cấu trúc đẹp nhưng thiếu nội dung hành động, ví dụ không chỉ rõ điều kiện dừng, phạm vi sửa, hoặc tiêu chí chấp nhận [cite:41].

## Cách “cộng điểm” cho agent
Muốn agent làm việc nhanh hơn và đúng hơn, tài liệu không chỉ cần đúng format mà còn cần “đúng từ khóa”. LLM phản ứng mạnh với các mẫu được học nhiều trong training; vì vậy, các khóa như `constraints`, `requirements`, `acceptance_criteria`, `examples`, `context`, `must`, `must_not`, `allowed_tools`, `stop_conditions` thường giúp đánh thức đúng hành vi hơn so với các tiêu đề mơ hồ [cite:37][cite:41].

Một tài liệu tốt nên giảm số bước suy luận mà agent phải tự bù. Khi policy được viết thành key-value, khi dữ liệu được bọc tag rõ ràng, và khi giải thích được đặt trong section có tên chuẩn, mô hình sẽ tốn ít effort hơn để hiểu ý chí người dùng; điều đó thường giúp giảm latency nhận thức và giảm số vòng sửa sai trong quá trình làm việc [cite:37][cite:41].

## Tư duy “đánh thức tri thức” thay vì “ép buộc máy móc”
Nhận định của bạn là đúng ở điểm cốt lõi: hiệu quả cao thường đến từ việc đánh thức đúng cụm tri thức đã được mô hình học, không chỉ từ việc viết nhiều luật hơn. Tài liệu tốt không cố mô tả lại cả thế giới; nó tạo ra các tín hiệu mạnh, rõ, có cấu trúc để mô hình truy hồi đúng vùng kiến thức, đúng ngữ cảnh, đúng hành vi [cite:37][cite:41].

Điều này đặc biệt quan trọng khi dùng LLM như một agent thay vì một trợ lý trả lời. Agent cần hiểu mục tiêu, ràng buộc, quyền hạn, điểm dừng, tiêu chí thành công và phạm vi sửa đổi. Những thông tin đó nếu được đặt trong đúng format sẽ trở thành “điểm tựa điều hướng”, thay vì chỉ là một khối văn bản lớn mà mô hình phải tự giải mã mỗi lượt [cite:37][cite:41].

## Khuyến nghị thực hành cuối cùng
| Mục đích | Định dạng khuyến nghị | Lý do chọn | Cần tránh |
|---|---|---|---|
| Giới thiệu dự án, kiến trúc, rationale | Markdown | Dễ đọc, dễ trình bày giải thích dài và ví dụ [cite:41] | Biến prose thành luật cứng ngầm |
| Ràng buộc, policy, checklist, capability | YAML | Key-value rõ, giảm mơ hồ, hợp với config thinking [cite:41] | Nhồi quá nhiều văn xuôi |
| Tách instruction, context, examples, docs | XML tags | Phân định ranh giới, giảm nhầm lẫn giữa dữ liệu và lệnh [cite:37][cite:41] | Tag vô nghĩa hoặc lồng quá sâu |
| Root guide cho agent lớn | Hybrid | Cân bằng readability, compliance và parseability [cite:37][cite:41] | Chọn một format cho mọi loại nội dung |

## Kết luận áp dụng
Thiết kế hiệu quả nhất cho `CLAUDE.md` và `AGENT.md` không phải Markdown thuần, cũng không phải YAML thuần hay XML thuần. Cách phù hợp nhất là kết hợp ba lớp: Markdown để giải thích cho người và agent, YAML để mã hóa ràng buộc và schema hành vi, XML để đóng khung ranh giới giữa instruction, context và examples [cite:37][cite:41].

Nếu mục tiêu là giúp agent hiểu trọn vẹn ý nghĩa, mục đích, ý chí của tài liệu, thì câu hỏi đúng không phải “format nào mạnh nhất”, mà là “loại thông tin này nên được biểu diễn dưới hình thức nào để mô hình hiểu đúng nhất với ít suy đoán nhất” [cite:37][cite:41].
