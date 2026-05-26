# KIẾN TRÚC TỔNG THỂ NÂNG CẤP: MASTER SKILL SUITE (VER_2.0.0 - CLEAN & SOLID)

Tài liệu này định hình kiến trúc nâng cấp toàn diện và thực chất cho bộ **Master Skill Suite** từ cấu trúc Ver_0 cũ lên **Ver_2.0.0 (Adaptive & Iron-clad)**. Bản thiết kế tích hợp sâu sắc triết lý kiểm soát **CASE** (Confidence-Aware Skill Execution), định dạng chuẩn hóa **LLM Knowledge Activation**, và giao thức vận hành Multi-Agent (Subagents) cô lập để giải phóng tối đa sức mạnh của AI đồng thời duy trì chốt chặn chất lượng thực chất, chống lại mọi hành vi "lừa đảo hoàn thành" (shortcut completion).

---

## 🎯 1. BỐI CẢNH VÀ TIÊU CHÍ THÀNH CÔNG CỦA BẢN THIẾT KẾ (DESIGN SUCCESS METRICS)

Để đo lường và xác nhận bản thiết kế Ver_2.0.0 hoạt động thực chất và thành công, hệ thống phải vượt qua 5 chỉ số định lượng sau:

1.  **Chỉ số Không Placeholder Thực chất (Zero Placeholder Integrity - ZPI):** 100% mã nguồn được xây dựng không chứa bất kỳ mock logic rỗng, cấu trúc điều kiện thiếu xử lý hoặc semantic placeholder nào (được quét và xác nhận bởi Tester Subagent trong Sandbox). **Mật độ đạt 0% tuyệt đối.**
2.  **Tỷ lệ Tự sửa lỗi Thành công (Self-Correction Rate - SCR):** Tối thiểu **80%** các lỗi logic/biên dịch thông thường được phát hiện bởi Tester được tự động rollback và sửa thành công bởi Builder thông qua `diagnostic.json` mà không cần sự can thiệp của Steve trong tối đa 3 vòng lặp.
3.  **Tỷ lệ Độc lập của Subagent (Subagent Autonomy - SAA):** 100% Tester Subagents chạy hoàn toàn độc lập, không làm tràn log rác về session chính, và truyền nhận bối cảnh thành công qua JSON Specs.
4.  **Độ tin cậy của Kịch bản biên (Edge-Case Coverage - ECC):** Tester Subagent phải tự suy luận và chạy thành công tối thiểu **2 kịch bản biên (Stress-Tests)** nằm ngoài kịch bản mẫu ban đầu, giúp phát hiện ra các lỗi tiềm ẩn của Builder trước khi xuất xưởng.
5.  **Tốc độ Khám phá Tri thức (Knowledge Retrieval Latency - KRL):** Việc gom nhóm tri thức tránh phân mảnh (SKILL.md làm Dynamic Index) giúp giảm số lượng tool calls đọc file của AI khi sử dụng kỹ năng mới xuống dưới **3 cuộc gọi**, tăng tốc độ phản hồi và tiết kiệm 60-90% token budget.

---

## 🏛️ 2. NGUYÊN LÝ THIẾT KẾ HỆ THỐNG CỐT LÕI (CORE PRINCIPLES)

*   **Ranh giới Trách nhiệm Đơn nhất (Single Responsibility Bounded Context):** Mỗi Stage hoạt động như một hộp đen độc lập (Stateless Function). Nó không cần biết Stage trước đã làm việc thế nào, chỉ cần nhận đúng cấu trúc dữ liệu đầu vào chuẩn và sản xuất ra đầu ra chuẩn.
*   **Sổ cái Bối cảnh có Cấu trúc (Structured State Ledger):** Loại bỏ việc truyền nhận ngữ cảnh bằng các tệp Markdown phẳng dễ gây mơ hồ cho AI. Toàn bộ dữ liệu trung gian trong `.skill-context/` được chuyển đổi sang **Structured JSON** đi kèm Schema `.schema.json` nghiêm ngặt để đảm bảo khả năng xử lý tự động chính xác 100%.
*   **Cô lập Môi trường & Đóng gói Ngữ cảnh (Context & Environment Isolation):** Tách biệt hoàn toàn các nhiệm vụ nặng log và rủi ro (kiểm thử, nghiên cứu sâu) thông qua kiến trúc Subagents và Sandbox Docker. Session chính đóng vai trò là Orchestrator/State Manager.
*   **Vòng lặp Phản hồi Tự sửa lỗi (Closed-Loop Diagnostic Feedback):** Thay vì rollback mơ hồ, hệ thống tự động chuyển giao lỗi biên dịch/logic thành chỉ dẫn sửa đổi có cấu trúc cho các giai đoạn thiết kế/lập kế hoạch.

---

## 📦 3. RANH GIỚI TRÁCH NHIỆM & DATA CONTRACTS GIỮA CÁC STAGES

Mỗi Stage được phân định ranh giới trách nhiệm cực kỳ rõ ràng thông qua **Input/Output Contracts (Giao thức đầu vào/đầu ra)**:

```mermaid
graph TD
    User([STEVE - Human Input])
    
    subgraph ContextLedger ["SỔ CÁI BỐI CẢNH DẠNG JSON (.skill-context/)"]
        E[exploration.json]
        C[criteria.json]
        B[blueprint.json]
        P[dag_plan.json]
        V[verification.json]
        D[diagnostic.json]
    end

    User -->|Gate 0: Duyệt & Nạp tri thức| S0[Stage 0: Explorer]
    S0 -->|Sản xuất| E & C
    
    E & C --> S1[Stage 1: Architect]
    S1 -->|Sản xuất| B
    
    B & C --> S2[Stage 2: Planner]
    S2 -->|Sản xuất| P
    
    P & B & C --> S3[Stage 3: Builder]
    S3 -->|Sản xuất| SrcCode[new-skill/ SKILL.md + Core Files]
    
    SrcCode & C --> S4[Stage 4: Tester - Subagent]
    S4 -->|Sản xuất| V
    S4 -->|Confidence < 85%| D
    
    D -->|Diagnostic Feedback Loop| S1 & S2
    
    V -->|Confidence >= 85%| S5[Stage 5: Indexer]
    S5 -->|Sản xuất| Index[llms.txt & README.md & Experience]
```

### Stage 0: Explorer (The Business & Quality Boundary)
*   **Trách nhiệm:** Định hình bài toán nghiệp vụ, phân tích rủi ro kỹ thuật (Technical Risks, Prompt Injection, dependencies) và xây dựng bộ tiêu chí nghiệm thu định lượng. Đây là **Gate duy nhất** có sự phê duyệt và định hướng ngữ cảnh trực tiếp từ Steve.
*   **Input Contract:** User Prompt + Personal Knowledge Base (`knowledge/`).
*   **Output Contract:** 
    *   `exploration.json` (Xác thực bởi `exploration.schema.json`): Bản đồ nghiệp vụ, phân tích rủi ro chi tiết.
    *   `criteria.json` (Xác thực bởi `criteria.schema.json`): Bộ tối thiểu 5 tiêu chí nghiệm thu định lượng và 2 test-cases mẫu (input/output).

### Stage 1: Architect (The Structural Blueprint Boundary)
*   **Trách nhiệm:** Tự động chuyển hóa các yêu cầu và tiêu chí nghiệp vụ thành bản vẽ kiến trúc hệ thống tĩnh (Static Structure - 7 Zones) và động (Dynamic Behavior). Thiết lập Mitigation Map (Ánh xạ rủi ro bảo mật ở Stage 0 sẽ được khắc phục ở Zone nào ở Stage 3).
*   **Input Contract:** `exploration.json` + `criteria.json`.
*   **Output Contract:** 
    *   `blueprint.json` (Xác thực bởi `blueprint.json`): Sơ đồ thư mục chi tiết (100% ánh xạ tệp vật lý vào 7 Zones), sequence flowcharts, các Interaction Points của người dùng, và kế hoạch khắc phục rủi ro.

### Stage 2: Planner (The DAG Scheduler Boundary)
*   **Trách nhiệm:** Chuyển hóa blueprint kiến trúc tĩnh thành một sơ đồ hướng công việc phi chu kỳ (DAG - Directed Acyclic Graph) nhằm tối ưu hóa luồng phụ thuộc và thứ tự thực thi của Builder.
*   **Input Contract:** `blueprint.json` + `criteria.json`.
*   **Output Contract:**
    *   `dag_plan.json` (Xác thực bởi `dag_plan.schema.json`): Danh sách các task công việc độc lập, ma trận phụ thuộc (blockers), ước lượng tài nguyên và trace tags chính xác về `blueprint.json`.

### Stage 3: Builder (The Implementation Engine)
*   **Trách nhiệm:** Viết code thực chất, tuân thủ nguyên lý Đóng gói Hợp nhất (Unified Layering). Builder bị cấm tuyệt đối việc sửa đè ngược lên `blueprint.json`.
*   **Input Contract:** `dag_plan.json` + `blueprint.json` + `criteria.json`.
*   **Output Contract:**
    *   Thư mục kỹ năng hoàn chỉnh: `SKILL.md` (Mục Lục Động từ 500-1000 tokens) liên kết đến tối đa **3 file tri thức cốt lõi** (`policy/guidelines.yaml`, `knowledge/concepts.md`, `scripts/tools.py`). Triệt tiêu hoàn toàn mã nguồn giả (placeholders, mock rỗng).

### Stage 4: Tester (The Verification Sandbox & Oracle)
*   **Trách nhiệm:** Spawn một Subagent chạy độc lập trong Docker Sandbox (gVisor) để kiểm thử mã nguồn. Tester tự động sinh thêm **tối thiểu 2 kịch bản biên (Edge Cases / Stress Tests)** độc lập để tra tấn mã nguồn. Tính toán toán học chỉ số tự tin thực chất.
*   **Input Contract:** `criteria.json` + Mã nguồn kỹ năng vừa build.
*   **Output Contract:**
    *   `verification.json` (Xác thực bởi `verification.schema.json`): Kết quả test chi tiết, tỉ lệ test pass, điểm Semantic Placeholder Density, chỉ số tự tin CASE.
    *   `diagnostic.json` (Xác thực bởi `diagnostic.schema.json`): Báo cáo chẩn đoán lỗi chi tiết khi chỉ số tự tin < 85%.

### Stage 5: Indexer (The Packaging & Distiller Boundary)
*   **Trách nhiệm:** Đóng gói kỹ năng, cập nhật `llms.txt`, tự động sinh tài liệu sử dụng nhanh (`README.md`) có kèm ví dụ Good/Bad thực tế. Tự động trích xuất tri thức, sự cố thu hoạch được từ sandbox ghi ngược lại `knowledge/experience/` theo định dạng standards.md.
*   **Input Contract:** `verification.json` + Mã nguồn kỹ năng.
*   **Output Contract:** README.md + cập nhật `llms.txt` + `knowledge/experience/{skill-name}.md`.

---

## 📅 4. CHÍNH SÁCH TIẾT LỘ TIẾN TRÌNH CO LẬP (PROGRESSIVE DISCLOSURE POLICY)

Để tối ưu hóa Token Budget cho từng Agent và đảm bảo tính tập trung cao độ, bối cảnh chỉ được nạp theo nhu cầu (Progressive Disclosure) nghiêm ngặt dựa trên bảng cấu hình sau:

```yaml
progressive_disclosure_policy:
  stage_0_explorer:
    load_always: 
      - "standards.md"
      - "_shared/knowledge/framework.md"
    target_write: 
      - ".skill-context/{name}/exploration.json"
      - ".skill-context/{name}/criteria.json"
    token_budget: 800
    
  stage_1_architect:
    load_always: 
      - ".skill-context/{name}/criteria.json"
    load_on_demand: 
      - ".skill-context/{name}/exploration.json"
    target_write: 
      - ".skill-context/{name}/blueprint.json"
    token_budget: 1200
    
  stage_2_planner:
    load_always: 
      - ".skill-context/{name}/criteria.json"
    load_on_demand: 
      - ".skill-context/{name}/blueprint.json" # Chỉ nạp static_structure & dynamic_behavior
    target_write: 
      - ".skill-context/{name}/dag_plan.json"
    token_budget: 1000
    
  stage_3_builder:
    load_always: 
      - ".skill-context/{name}/dag_plan.json"
      - ".skill-context/{name}/criteria.json"
    load_on_demand: 
      - ".skill-context/{name}/blueprint.json"
    target_write: 
      - "SKILL.md"
      - "policy/guidelines.yaml"
      - "knowledge/concepts.md"
    token_budget: 2000
    
  stage_4_tester:
    load_always: 
      - ".skill-context/{name}/criteria.json"
    load_on_demand: 
      - "Mã nguồn kỹ năng vừa build"
    target_write: 
      - ".skill-context/{name}/verification.json"
      - ".skill-context/{name}/diagnostic.json"
    token_budget: 1500
    
  stage_5_indexer:
    load_always: 
      - ".skill-context/{name}/verification.json"
    target_write: 
      - "README.md"
      - "llms.txt"
      - "knowledge/experience/{name}.md"
    token_budget: 800
```

---

## 🏆 5. KHUNG TIÊU CHÍ CHẤP NHẬN ĐẦU RA THỰC CHẤT (ACCEPTANCE MATRIX VER_2.0.0)

Mỗi giai đoạn phát triển bắt buộc phải vượt qua bộ chốt chặn chất lượng phân cấp dưới đây. Tuyệt đối KHÔNG BÀN GIAO nếu sản phẩm thuộc dải kiểm định [ ❌ BAD ].

```yaml
acceptance_matrix:
  stage_0_explorer:
    bad:
      - "Không phân tích tối thiểu 3 rủi ro kỹ thuật hoặc điểm mù bảo mật của kỹ năng"
      - "Tệp criteria.json trống hoặc chỉ mô tả định tính chung chung, thiếu test cases định lượng rõ ràng"
    good:
      - "Có tối thiểu 5 tiêu chí nghiệm thu rõ ràng và 2 kịch bản test-case định lượng cụ thể"
      - "Vượt qua exploration.schema.json và criteria.schema.json"
    premium:
      - "Phân tích rủi ro Prompt Injection đặc thù của task nghiệp vụ và đề xuất cơ chế phòng vệ chi tiết"
      - "Sinh sẵn bộ dữ liệu mẫu (mock inputs/outputs) chất lượng cao để chạy tự động ở Stage 4"

  stage_1_architect:
    bad:
      - "Sử dụng tên file giả định (placeholders như file1.py, script_new.sh) trong bản thiết kế"
      - "Thiếu sơ đồ Mermaid mô tả cấu trúc thư mục hoặc luồng tuần tự sequence logic"
      - "Không thiết lập các Interaction Points (Điểm dừng tương tác) bắt buộc với người dùng"
    good:
      - "Chỉ định chính xác 100% tên file vật lý và ánh xạ khớp hoàn hảo vào 7 Zones trong blueprint.json"
      - "Có đầy đủ sơ đồ folder structure và sequence flowchart"
    premium:
      - "Thiết kế chi tiết giao thức Rollback tự động phục hồi trạng thái khi gặp lỗi dựa trên diagnostic.json"
      - "Có bảng mapping chi tiết: Từng rủi ro bảo mật ở Stage 0 được khắc phục ở Zone nào ở Stage 3"

  stage_2_planner:
    bad:
      - "Checklist công việc mơ hồ, không thể triển khai lập trình (ví dụ: 'Code chức năng chính')"
      - "Thiếu hoặc ghi sai định dạng trace tags quy định"
      - "Sắp xếp tasks phi logic (ví dụ: viết logic trước khi tạo file tri thức hoặc cấu hình data)"
    good:
      - "100% các task kết thúc bằng trace tags hợp lệ: [TỪ DESIGN §N] hoặc [TỪ AUDIT TÀI NGUYÊN]"
      - "Thiết lập cấu trúc đồ thị phi chu kỳ (DAG) với blocker dependencies rõ ràng"
    premium:
      - "Xây dựng ma trận blocker và biểu đồ phụ thuộc công việc (DAG), ước lượng Est. Hours chuẩn"
      - "Tích hợp script tự động kiểm tra cú pháp và tính đồng nhất của dag_plan.json"

  stage_3_builder:
    bad:
      - "Mã nguồn chứa code giả, ghi chú trì hoãn hoặc placeholders (// TODO, pass, mock())"
      - "Tệp điều hướng cốt lõi SKILL.md phình to quá 1200 tokens, vi phạm chuẩn layering"
      - "Tự ý thay đổi ngược tệp thiết kế blueprint.json gây xung đột bối cảnh hệ thống"
    good:
      - "100% code hoạt động thực tế, không chứa bất kỳ placeholder nào"
      - "SKILL.md đạt chuẩn YAML frontmatter, token budget L0 < 1000 tokens, chia nhỏ logic dài dòng sang policy/ và knowledge/"
    premium:
      - "SKILL.md cực kỳ tinh gọn (< 500 tokens), hoạt động như một L0 Anchor Rule thuần khiết"
      - "Bàn giao mã nguồn kèm theo các tệp unit test chất lượng cao chạy ổn định"

  stage_4_tester:
    bad:
      - "AI tự đọc mã nguồn rồi tự xác nhận Pass mà không chạy script kiểm thử thực tế"
      - "Bỏ qua các cảnh báo kiểm tra lỗi Placeholder density (> 0)"
    good:
      - "Chạy thành công 100% kịch bản kiểm thử quy định trong criteria.json bên trong Sandbox Docker biệt lập"
      - "Mật độ placeholder density bằng 0% điểm tuyệt đối"
    premium:
      - "Tích hợp tự động kiểm thử hiệu năng, độ trễ và khả năng phòng thủ prompt injection"
      - "Tự động sinh tối thiểu 2 kịch bản biên (Edge-Cases) độc lập để tra tấn mã nguồn và tính toán Confidence Score >= 85%"

  stage_5_indexer:
    bad:
      - "Không viết tài liệu sử dụng nhanh hoặc viết hời hợt, thiếu ví dụ thực tế"
      - "Quên đăng ký kỹ năng mới vào chỉ mục hệ thống llms.txt"
    good:
      - "README.md đầy đủ cấu trúc, có ví dụ Good/Bad thực tế và hướng dẫn tích hợp chi tiết"
      - "Kỹ năng được đăng ký thành công vào llms.txt và registry/README.md"
    premium:
      - "Tài liệu vận hành có sơ đồ Mermaid giải thích cách tích hợp nhanh và các cổng API liên quan"
      - "Tự động trích xuất tri thức, sự cố thu hoạch được từ sandbox ghi ngược lại knowledge/experience/ đúng chuẩn standards.md"
```

---

## 🛠️ 6. TÍNH MÔ-ĐUN HÓA (MODULARITY) & LINH HOẠT ĐỘNG (DYNAMIC FLEXIBILITY)

Bản thiết kế Ver_2.0.0 phá vỡ sự cứng nhắc của mô hình thác nước truyền thống bằng các đặc tính động và khả năng cô lập mô-đun cao độ:

### 6.1. Mô-đun hóa Độc lập (Loose Coupling)
*   Mỗi Stage được đóng gói thành một mô-đun chức năng tự trị. Các mô-đun giao tiếp thông qua API/Structured JSON ổn định.
*   **Khả năng Chạy Độc lập:** Có thể chạy riêng biệt Stage 4 (Tester Subagent) để kiểm định một kỹ năng viết tay bất kỳ bằng cách cung cấp tệp `criteria.json` bên ngoài. Tương tự, có thể chạy Stage 5 (Indexer) độc lập để đăng ký và trích xuất tri thức từ một báo cáo kiểm thử có sẵn mà không cần đi qua các giai đoạn Architect hay Builder.

### 6.2. Định tuyến Pipeline Linh hoạt (Dynamic Re-routing)
*   **Bypass thông minh:** Hệ thống phân tích sự thay đổi (Context Diff). Nếu Steve chỉ yêu cầu tinh chỉnh một tài liệu tri thức nhỏ hoặc sửa một lỗi cú pháp trong một kỹ năng đang chạy, hệ thống sẽ tự động bỏ qua Stage 0 (Explorer) và Stage 1 (Architect), đi thẳng từ Stage 2 hoặc Stage 3 để tiết kiệm token và thời gian.
*   **Phản hồi động thông minh (Dynamic Re-routing on Failure):** Khi phát hiện lỗi ở Stage 4 (Tester), hệ thống tự động phân loại lỗi để re-route về stage phù hợp:
    *   *Lỗi Logic/Thuật toán:* Re-route trực tiếp về Stage 3 (Builder) để viết lại hàm lỗi.
    *   *Lỗi Cấu trúc/Thiếu file/Sai Zone:* Re-route ngược về Stage 1 (Architect) để thiết kế lại bản vẽ 7 Zones.

---

## 🤖 7. KIẾN TRÚC MULTI-AGENT & GIAO THỨC ĐÓNG GÓI NGỮ CẢNH SUBAGENT

Để giải quyết vấn đề loãng ngữ cảnh và tối ưu hóa sức mạnh của từng Agent, Ver_2.0.0 thiết lập **Giao thức Đóng gói Ngữ cảnh Subagent (Subagent Context Isolation Protocol)**:

```text
[Main Session (State Manager & Orchestrator)]
      │
      ├─► Lọc bỏ nhiễu và logs rác (Noise Erasure)
      ├─► Đóng gói Context Package (L0 Anchor + JSON Specs)
      │
      ▼
[Subagent Session (Task-Specific Specialist)]
      │
      ├─► Tự động hóa Sandbox (Docker/gVisor)
      ├─► Tạo kịch bản kiểm thử độc lập / Nghiên cứu sâu
      │
      ▼
[Structured Result (JSON)] ──► Báo cáo gọn nhẹ về Main Session
```

### 7.1. Tester Subagent (Sandbox Executor)
*   **Lý do spawn:** Việc chạy Sandbox và sinh edge cases tạo ra log khổng lồ làm đầy ngữ cảnh session chính, đồng thời tăng nguy cơ bị Prompt Injection khi chạy thử code lạ.
*   **Context Package:** Chỉ nạp `criteria.json` + Thư mục mã nguồn vừa build + file chỉ dẫn `tester_rules.yaml`. Không nạp lịch sử chat thiết kế.
*   **Hoạt động:** Chạy Sandbox Docker cô lập, tự sinh tối thiểu **2 Edge Cases độc lập**, quét Semantic Placeholders, tính Confidence Score và chỉ trả về file báo cáo chắt lọc JSON.

### 7.2. Research Subagent (Stage 0)
*   **Lý do spawn:** Khi Explorer phân tích công nghệ/API phức tạp mà tài liệu tri thức dự án chưa đầy đủ.
*   **Context Package:** Chỉ dẫn câu hỏi trọng tâm + đường dẫn mã nguồn/API cần quét.
*   **Hoạt động:** Quét sâu mã nguồn đích, chắt lọc tri thức thành tệp JSON cô đọng gửi về session chính.

---

## 🔄 8. GIAO THỨC CHẨN ĐOÁN VÀ VÒNG LẶP PHỤC HỒI CASE (CASE RECOVERY @ 85%)

Khi Tester Subagent phát hiện mã nguồn không đạt chuẩn chất lượng thực chất (chỉ số tự tin calculated < 85%), hệ thống sẽ tự động kích hoạt vòng lặp chẩn đoán rollback khép kín:

### 8.1. Công thức tính toán chỉ số tự tin thực chất (Fact-Based Confidence Score)
$$\text{Confidence Score} = 0.4 \times (\text{Sandbox Test Pass Rate}) + 0.3 \times (1 - \text{Semantic Placeholder Density}) + 0.3 \times (\text{Static Analysis \& Lint Status})$$
*   *Sandbox Test Pass Rate:* Tỷ lệ test case vượt qua (bao gồm cả Edge Cases).
*   *Semantic Placeholder Density:* Mật độ hàm rỗng, hàm mock cứng hoặc cấu trúc logic thiếu xử lý lỗi. **Bắt buộc = 0 để đạt PASS.**
*   *Static Analysis & Lint Status:* Trạng thái biên dịch và kiểm tra lỗi tĩnh.

### 8.2. Vòng lặp phản hồi chẩn đoán tự sửa lỗi (Closed-Loop Diagnostic)
1.  Tester Subagent sinh tệp `diagnostic.json` chứa: ID test case bị hỏng, phân loại lỗi, tệp vật lý + số dòng bị lỗi, log stdout lỗi sandbox và gợi ý định hướng kỹ thuật sửa lỗi.
2.  Tín hiệu chẩn đoán tự động được chuyển ngược về Stage 1 (Architect) hoặc Stage 2 (Planner).
3.  Architect/Planner tự động đọc `diagnostic.json`, định vị và cập nhật lại thiết kế/kế hoạch, rồi chuyển giao cho Builder viết lại code.
4.  Vòng lặp tự sửa lỗi chạy tối đa **3 lần** tự động mà không làm phiền người dùng.

---

## 📅 9. CHÍNH SÁCH ĐỘ LỆCH THỜI GIAN (STALENESS POLICY)

Để đảm bảo an toàn thông tin và tính cập nhật của Sổ cái bối cảnh `.skill-context/` giữa các stage stateless, hệ thống thực hiện kiểm tra độ lệch thời gian tại mỗi chu kỳ khởi động (Boot Sequence):

```yaml
staleness_policy:
  check_interval: "Thực hiện tại mỗi Boot Sequence"
  rules:
    fresh:
      condition: "Khoảng cách thời gian sửa đổi cuối cùng của các JSON Specs < 7 ngày"
      action: "Tiếp tục chạy bình thường từ checkpoint gần nhất"
    warning:
      condition: "Khoảng cách thời gian sửa đổi cuối cùng của các JSON Specs từ 7 - 30 ngày"
      action: "Cảnh báo người dùng về nguy cơ mất ngữ cảnh, yêu cầu AI review lại dag_plan.json trước khi chạy"
    force_fresh:
      condition: "Khoảng cách thời gian sửa đổi cuối cùng của các JSON Specs > 30 ngày"
      action: "Bắt buộc hủy bỏ checkpoint cũ và khởi động lại Pipeline từ Stage 0 để đảm bảo tính an toàn"
```

---

## 📚 10. QUẢN LÝ VÀ SỬ DỤNG SKILL SAU KHI BUILD (POST-BUILD LIFECYCLE)

Sau khi một kỹ năng được xây dựng thành công, việc quản lý và đưa vào sử dụng phải tuân thủ quy trình an toàn tuyệt đối:

### 10.1. Đồng bộ Runtime Nguyên tử (Staging Atomic Swap Protocol)
Để tránh gây crash cho agent đang hoạt động trong session chính khi chép đè trực tiếp vào `.hermes/skills/`:
1.  Indexer tạo một bản cài đặt thử nghiệm tại `.hermes/skills/.staging/{skill-name}/`.
2.  Kích hoạt một dry-run test độc lập tại môi trường staging.
3.  Nếu vượt qua, thực hiện hoán đổi nguyên tử (atomic swap/mv) thư mục staging thành production runtime an toàn tuyệt đối.

### 10.2. Nạp Tri thức Động theo Nhu cầu (On-Demand Activation)
Để tiết kiệm 60-90% token budget và giữ session sạch sẽ, kỹ năng mới được đóng gói theo nguyên lý Layering:
*   `SKILL.md` đóng vai trò là **L0 Anchor (Mục lục Động)**, chỉ chứa metadata kích hoạt (`when_to_use`) và các liên kết markdown tuyệt đối dẫn tới các file tri thức thành phần.
*   AI agent khi sử dụng kỹ năng sẽ tự động kích hoạt luật và chỉ đọc đúng file tri thức cần thiết (`policy/guidelines.yaml` hoặc `knowledge/concepts.md`) tương ứng với tác vụ hiện tại, thay vì đọc toàn bộ thư mục.

---

## 📚 11. GIAO THỨC CHUYỂN HÓA TRI THỨC TỰ HỌC (SELF-LEARNING DISTILLER)

```yaml
knowledge_distiller_protocol:
  trigger: "Stage 5 Indexer khởi chạy thành công sau khi Stage 4 đạt PASS"
  input_sources:
    - ".skill-context/{skill-name}/verification.json"
    - "Sandbox execution logs"
    - "Developer manual adjustments during dry-run"
  distillation_rules:
    - "Trích xuất bài học kinh nghiệm từ các Edge Cases đã vượt qua ở Stage 4"
    - "Mã hóa các bài học này theo cấu trúc chuẩn standards.md của Steve"
    - "Định dạng:"
        markdown: "Giải thích kiến trúc và hiện tượng logic"
        yaml: "Các ràng buộc cứng (constraints, must, must_not) được rút ra"
        xml_tags: "Các ví dụ Good/Bad minh họa thực tế"
  persistence:
    path: "knowledge/experience/{skill-name}.md"
    registration: "Tự động đăng ký tệp tri thức mới vào knowledge/README.md để các lượt chạy sau của Suite tự động nạp làm dữ liệu tham chiếu"
```
