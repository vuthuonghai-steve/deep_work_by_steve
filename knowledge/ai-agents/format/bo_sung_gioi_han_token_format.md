# Bổ sung giới hạn token cho Markdown, YAML và XML trong file hướng dẫn AI Agent

## Mục tiêu tài liệu
Tài liệu này bổ sung cho tài liệu trước bằng một lớp thông tin mà các đội kỹ thuật thường thiếu khi xây `CLAUDE.md`, `AGENT.md`, `SYSTEM.md` hoặc agent spec: **giới hạn sử dụng theo token**, theo tầng thông tin, và theo loại format. Mục tiêu không phải là đưa ra một con số tuyệt đối đúng cho mọi model, mà là xây một hệ quy chiếu thực hành để quyết định khi nào nên giữ nội dung trong root guide, khi nào nên tách file, và khi nào một format bắt đầu làm giảm hiệu quả do tăng token, tăng nhiễu, hoặc tăng gánh nặng suy luận [web:16][web:37][web:41].

## Nguyên tắc đọc số liệu
Không tồn tại một ngưỡng token “chuẩn công nghiệp” áp dụng cho mọi model và mọi workload. Tài liệu này dùng **ngưỡng vận hành khuyến nghị** thay vì ngưỡng lý thuyết của context window, vì chất lượng instruction-following thường giảm từ rất sớm trước khi chạm giới hạn tối đa; nghiên cứu về prompt formatting cho thấy format có thể làm thay đổi hiệu suất rõ rệt, và tài liệu của Anthropic/OpenAI đều nhấn mạnh vai trò của cấu trúc và delimiter trong prompt dài [web:16][web:37][web:41].

Vì token phụ thuộc tokenizer, ngôn ngữ, dấu câu, indentation và mật độ ký tự đặc biệt, mọi con số dưới đây nên được hiểu như **vùng an toàn** để thiết kế tài liệu, không phải luật cứng để tính toán chính xác. Cách dùng đúng là: đo prompt thật bằng tokenizer của model đang dùng, sau đó đối chiếu với các “mức tải” bên dưới để quyết định giữ, nén, tách hay chuyển format [web:16][web:41].

## Đơn vị đánh giá theo tầng
Để kiểm soát file hướng dẫn hiệu quả, nên chia context thành bốn tầng.

- **Layer 0 – Anchor rules:** các luật tối quan trọng, mục tiêu hệ thống, giới hạn quyền và anti-goals; đây là phần phải luôn hiện diện trong root guide [web:37][web:41].
- **Layer 1 – Working policy:** coding rules, conventions, output contract, acceptance criteria, tool rules; chỉ nên đủ ngắn để agent dùng thường xuyên mà không bị loãng [web:37][web:41].
- **Layer 2 – Domain context:** kiến trúc, domain glossary, data flow, ADRs, subsystem notes; chỉ nạp khi task cần [web:37][web:41].
- **Layer 3 – Evidence/examples:** docs tham chiếu, logs, ticket text, examples, test fixtures; đây là tầng dễ phình to nhất và cần delimiter mạnh [web:37][web:41].

## Ngưỡng token khuyến nghị cho từng layer
Bảng dưới đây là mức khuyến nghị để giữ chất lượng agent ổn định trong đa số workflow coding-agent thực tế.

| Layer | Mục đích | Ngưỡng tốt | Cảnh báo | Nên tách khi |
|---|---|---:|---:|---:|
| Layer 0 | Anchor rules | 150–400 tokens [web:37][web:41] | 500–700 tokens [web:16][web:41] | >700 tokens [web:16] |
| Layer 1 | Working policy | 400–1,200 tokens [web:16][web:41] | 1,200–2,000 tokens [web:16] | >2,000 tokens [web:16][web:41] |
| Layer 2 | Domain context | 600–2,500 tokens [web:16][web:37] | 2,500–5,000 tokens [web:16] | >5,000 tokens [web:16][web:41] |
| Layer 3 | Evidence/examples | 300–2,000 tokens [web:37][web:41] | 2,000–6,000 tokens [web:16] | >6,000 tokens [web:16][web:37] |

Ý nghĩa của bảng này là: root guide nên chủ yếu chứa Layer 0 và phần ngắn nhất của Layer 1. Khi tài liệu root mang quá nhiều Layer 2 và Layer 3, agent bắt đầu dành attention cho thông tin chỉ có ích theo tình huống, làm giảm độ sắc của chỉ dẫn trung tâm [web:16][web:37][web:41].

## Giới hạn khuyến nghị theo format

### Markdown
Markdown phù hợp nhất cho prose, giải thích, rationale và bản đồ điều hướng. Tuy nhiên, khi Markdown narrative vượt quá **1,200–1,800 tokens trong một khối liên tục** mà không có delimiter mạnh hoặc sự phân đoạn rõ ràng, mô hình thường phải suy luận lại loại thông tin của từng đoạn, dẫn tới tăng tải nhận thức và tăng nguy cơ xem luật như ghi chú mềm [web:16][web:41].

Ngưỡng thực hành nên dùng cho Markdown trong file hướng dẫn:

| Cấp độ | Token cho một section Markdown | Đánh giá |
|---|---:|---|
| Nhẹ | 100–400 [web:41] | Tốt cho overview, rationale ngắn, glossary |
| Vừa | 400–900 [web:16][web:41] | Chấp nhận được nếu có heading rõ và ít trộn rule |
| Nặng | 900–1,800 [web:16] | Bắt đầu nên tách hoặc chuyển phần policy sang YAML |
| Quá tải | >1,800 [web:16] | Dễ gây loãng ý, nên chia nhỏ hoặc thay bằng file tham chiếu |

Markdown **không hỏng kỹ thuật** khi dài, nhưng **hỏng ngữ nghĩa vận hành**: quá nhiều prose làm agent khó biết đoạn nào là luật, đoạn nào là giải thích, đoạn nào là ngoại lệ. Vì vậy, giới hạn của Markdown không nằm ở parser mà nằm ở chi phí suy luận mà nó buộc model phải gánh [web:16][web:41].

### YAML
YAML phù hợp cho policy và schema vì tạo key-value rõ ràng. Nhưng YAML dài sẽ gặp ba loại vấn đề: tăng indentation depth, tăng lặp khóa, và tăng chi phí kiểm tra quan hệ giữa các nhánh; khi đó lợi thế “rõ nghĩa” bắt đầu giảm và tài liệu trở nên khó quét với cả người lẫn agent [web:41].

Ngưỡng thực hành nên dùng cho YAML trong hướng dẫn agent:

| Cấp độ | Token cho một YAML block | Đánh giá |
|---|---:|---|
| Nhẹ | 80–300 [web:41] | Rất tốt cho constraints, capability map nhỏ |
| Vừa | 300–700 [web:41] | Tốt cho policy block, checklist, acceptance criteria |
| Nặng | 700–1,200 [web:16][web:41] | Bắt đầu nên tách thành nhiều block theo domain |
| Quá tải | >1,200 [web:16] | YAML mất ưu thế, dễ rối và khó duy trì |

Một block YAML vượt **1,200 tokens** không có nghĩa model không đọc được; vấn đề là block đó thường đã chứa quá nhiều loại ý nghĩa khác nhau. Cách xử lý đúng là tách theo miền như `constraints`, `tooling`, `review_rules`, `output_contract`, thay vì tiếp tục dồn sâu bằng indentation [web:41].

Với root guide, tổng YAML nên ở khoảng **300–900 tokens** là hiệu quả nhất. Nếu tổng YAML của file gốc vượt **1,500–2,000 tokens**, nên chuyển sang nhiều file rule hoặc scoped rule files, vì agent không cần nạp toàn bộ chính sách của mọi miền trong mọi lượt làm việc [web:16][web:41].

### XML-like tags
XML tags rất mạnh ở vai trò delimiter và semantic boundary. Anthropic khuyến nghị XML khi prompt có nhiều phần như context, instructions và examples vì Claude parse các phần này rõ hơn khi có tag bao quanh [web:37].

Tuy nhiên, XML có chi phí token cao hơn do mở/đóng tag lặp lại. Dữ liệu thực nghiệm cộng đồng cho thấy Markdown thường gọn hơn XML, và ví dụ token count đơn giản cho thấy Markdown 53 tokens, XML 77 tokens, JSON 103 tokens trong cùng một tập biểu diễn; XML vì vậy nên được dùng cho **biên giới ngữ nghĩa**, không nên phủ toàn bộ tài liệu bằng tag nếu không cần thiết [web:54].

Ngưỡng thực hành cho XML trong file hướng dẫn:

| Cấp độ | Token cho khối XML | Đánh giá |
|---|---:|---|
| Nhẹ | 50–250 [web:37][web:54] | Rất tốt để bọc instructions/context/examples |
| Vừa | 250–800 [web:37][web:54] | Tốt nếu dùng như delimiter quanh khối quan trọng |
| Nặng | 800–1,500 [web:16][web:54] | Chỉ nên dùng khi cần chia source docs hoặc contract rõ ràng |
| Quá tải | >1,500 [web:16][web:54] | Token overhead cao; nên rút gọn hoặc chỉ tag outer blocks |

Nguyên tắc quan trọng là: XML hiệu quả nhất khi số lượng tag nhỏ nhưng tên tag mang nghĩa lớn. Nếu tag quá nhiều, lồng sâu hoặc bọc từng chi tiết nhỏ, chi phí token tăng nhanh trong khi giá trị cấu trúc tăng chậm [web:37][web:54].

## Mức tải tổng cho một file root guide
Dưới đây là ngưỡng vận hành thực tế cho `CLAUDE.md` hoặc `AGENT.md` ở root.

| Tổng token file root | Mức tải | Khuyến nghị |
|---|---:|---|
| 300–900 [web:41] | Rất tốt | Giữ ở root, phù hợp cho anchor rules + policy ngắn |
| 900–1,800 [web:16][web:41] | Tốt | Chấp nhận được nếu nội dung đã hybrid và có import/tách file |
| 1,800–3,000 [web:16] | Cảnh báo | Chỉ nên giữ nếu rất chặt chẽ, ít prose, nhiều phân lớp rõ |
| 3,000–5,000 [web:16] | Nặng | Nên coi là dấu hiệu root guide đang gánh thay docs hệ thống |
| >5,000 [web:16][web:37] | Quá tải | Nên tái cấu trúc; root chỉ giữ bản đồ điều hướng và rules cốt lõi |

Con số này không mâu thuẫn với việc model có context window rất lớn. Vấn đề không phải “nhét có vừa không”, mà là “agent còn giữ được ưu tiên hành động đúng không” khi mọi loại tri thức cùng chen vào một prompt vận hành [web:16][web:37][web:41].

## Budget token theo tỷ lệ
Một cách ổn định hơn là không nhìn mỗi format riêng lẻ mà đặt budget theo tỷ lệ trong file root.

| Thành phần | Tỷ lệ token khuyến nghị trong root guide |
|---|---:|
| Anchor rules | 15–25% [web:37][web:41] |
| Working policy | 35–50% [web:16][web:41] |
| Architecture/context | 20–30% [web:41] |
| Examples/reference snippets | 5–15% [web:37] |

Nếu phần ví dụ hoặc reference chiếm quá nhiều, root guide đang biến thành kho tri thức thay vì bộ điều hướng. Nếu phần rules chiếm quá ít so với prose, agent dễ đọc hiểu được dự án nhưng không hành động nhất quán [web:37][web:41].

## Chi phí token tương đối giữa các format
Không có một hệ số cố định cho mọi nội dung, nhưng có thể dùng quy tắc gần đúng dưới đây khi thiết kế.

- **Markdown** thường là format gọn và tự nhiên nhất cho prose có cấu trúc nhẹ [web:54].
- **YAML** thường gọn hơn XML trong biểu diễn cấu hình, nhưng độ gọn dao động mạnh theo số lượng khóa lặp, độ sâu lồng và whitespace [web:46][web:51].
- **XML** thường tốn token hơn Markdown và nhiều trường hợp tốn hơn YAML vì phải lặp tag mở/đóng, nhưng đổi lại cho ranh giới ngữ nghĩa mạnh hơn [web:37][web:54].

Trong thiết kế thực tế, có thể lấy gần đúng sau làm điểm xuất phát để ước lượng cùng một lượng thông tin: Markdown = 1.0x, YAML = 1.1x đến 1.35x, XML = 1.25x đến 1.6x. Đây là **hệ số ước tính vận hành**, không phải định luật, nhưng hữu ích để dự đoán khi nào một tài liệu hybrid bắt đầu quá tải [web:46][web:51][web:54].

## Khi nào cần chuyển tầng hoặc đổi format
Nên đổi cấu trúc khi gặp một trong các dấu hiệu sau.

- Một section Markdown vượt khoảng **900–1,200 tokens** nhưng vẫn chứa cả giải thích, rule, exception và checklist trong cùng một dòng chảy [web:16][web:41].
- Một block YAML vượt **700–1,200 tokens** hoặc độ sâu lồng vượt 3–4 cấp, khiến người đọc khó xác định đâu là nhánh ưu tiên [web:16][web:41].
- Các tag XML xuất hiện dày đặc quanh gần như mọi đoạn văn, làm phần delimiter bắt đầu chiếm tỉ lệ đáng kể trong tổng token [web:37][web:54].
- Root guide vượt **1,800–3,000 tokens** mà vẫn tăng đều sau mỗi sprint; đây gần như luôn là dấu hiệu của thiếu phân tầng tài liệu [web:16].

## Mẫu budget khuyến nghị cho dự án lớn
Dưới đây là cách phân bổ token phù hợp cho một root guide hiệu quả trong dự án lớn.

| Khối | Format chính | Budget khuyến nghị |
|---|---|---:|
| Mission + hard rules | Markdown ngắn + XML bọc ngoài | 150–300 tokens [web:37][web:41] |
| Constraints/policies | YAML | 250–700 tokens [web:41] |
| Architecture overview | Markdown | 250–600 tokens [web:41] |
| Tool rules / workflow | YAML hoặc Markdown ngắn | 150–400 tokens [web:41] |
| Examples | XML hoặc Markdown code block | 100–300 tokens [web:37][web:54] |
| Tổng root guide | Hybrid | 900–2,000 tokens [web:16][web:37][web:41] |

Nếu vượt mức này, hướng đi tốt nhất không phải cố viết “hay hơn” trong cùng file, mà là chuyển thêm tri thức xuống layer thấp hơn: scoped rules, domain docs, retrieved context, hoặc examples chỉ nạp theo task [web:16][web:37][web:41].

## Cách dùng số liệu này cho AI agent
Một agent hiệu quả nên được dạy không chỉ “dùng YAML cho rules” mà còn phải hiểu **khi nào dừng nhồi thêm YAML**, **khi nào chuyển prose sang docs tham chiếu**, và **khi nào XML chỉ nên đóng vai delimiter**. Những ngưỡng token ở trên cung cấp cho agent một hệ quy chiếu để tự đánh giá prompt/file hiện tại đang ở mức nhẹ, vừa, nặng hay quá tải [web:16][web:37][web:41].

Điều này hữu ích vì nó biến tri thức format thành hành vi có thể ra quyết định. Thay vì chỉ biết “YAML tốt cho constraints”, agent có thể kết luận cụ thể hơn: “Block constraints đã vượt 900 tokens, nên tách theo domain”, hoặc “examples đang chiếm 20% root guide, nên rút về file riêng”, từ đó giảm chi phí context và giữ chất lượng tuân thủ cao hơn [web:16][web:37][web:41].

## Quy tắc thực hành ngắn gọn
- Root guide nên giữ trong khoảng **900–2,000 tokens**, chỉ chứa phần cốt lõi và bản đồ điều hướng [web:16][web:41].
- Một section Markdown nên bắt đầu được xem xét tái cấu trúc khi vượt **900 tokens**, và gần như chắc chắn nên tách khi vượt **1,800 tokens** [web:16].
- Một block YAML nên tách miền khi vượt **700–1,200 tokens** hoặc lồng quá sâu [web:16][web:41].
- XML nên dùng để bọc khối, không nên bọc vi mô; nếu phần tag bắt đầu chiếm cảm giác “nhiều hơn nội dung”, cấu trúc đã đi sai hướng [web:37][web:54].
- Khi nghi ngờ, ưu tiên giảm token ở Layer 2 và Layer 3 trước, không giảm Layer 0 [web:37][web:41].

## Kết luận áp dụng
Giới hạn hữu ích nhất không phải là giới hạn tổng context window của model, mà là **giới hạn vận hành của từng lớp thông tin**. Markdown dài quá sẽ tăng chi phí suy luận, YAML dài quá sẽ mất lợi thế schema, XML dày quá sẽ ăn token nhanh; vì vậy, cách đúng là đặt budget token theo layer, rồi chọn format theo bản chất thông tin của từng layer [web:16][web:37][web:41][web:54].

Nói ngắn gọn: Markdown dùng để giải thích, YAML dùng để ràng buộc, XML dùng để phân ranh giới; nhưng chỉ hiệu quả khi mỗi loại đều được giữ trong vùng token mà nó còn phát huy đúng ưu thế của mình [web:37][web:41][web:54].
