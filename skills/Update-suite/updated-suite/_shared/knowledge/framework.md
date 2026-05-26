# MASTER FRAMEWORK — Shared Knowledge Base (Ver_2.0.0 - Clean & Solid)

> **Purpose**: Single source of truth for the entire Master Skill Suite Ver_2.0.0
> **Location**: `_shared/knowledge/framework.md` (portable, resolved relative to skills-root)
> **Usage**: Read this FIRST when working with any stage of the Master Skill Suite (Explorer to Indexer)

---

## 🏛️ 1. NGUYÊN LÝ THIẾT KẾ HỆ THỐNG (SYSTEM PRINCIPLES)

Bộ suite Ver_2.0.0 (Adaptive & Iron-clad) được xây dựng trên 4 nguyên lý Clean & Solid cốt lõi:

1.  **Ranh giới Trách nhiệm Đơn nhất (Single Responsibility Bounded Context):** Mỗi Stage hoạt động như một hộp đen độc lập (Stateless Function). Nó nhận dữ liệu đầu vào chuẩn từ Sổ cái bối cảnh JSON và sản xuất ra đầu ra JSON chuẩn.
2.  **Sổ cái Bối cảnh có Cấu trúc (Structured JSON State Ledger):** Toàn bộ dữ liệu trung gian trong `.skill-context/{skill-name}/` được định dạng dưới dạng **Structured JSON** đi kèm Schema `.schema.json` nghiêm ngặt để đảm bảo khả năng parse tự động của AI đạt độ chính xác 100%.
3.  **Cô lập Môi trường & Đóng gói Ngữ cảnh (Context & Environment Isolation):** Tận dụng kiến trúc Subagents và Docker Sandbox để chạy các tác vụ nặng log hoặc có rủi ro bảo mật (như kiểm thử mã nguồn, nghiên cứu sâu) độc lập với session chính.
4.  **Vòng lặp Phản hồi Tự sửa lỗi (Closed-Loop Diagnostic Feedback):** Lỗi phát hiện từ sandbox tự động được Tester chuyển hóa thành chỉ dẫn sửa đổi có cấu trúc `diagnostic.json` để tự sửa lỗi khép kín (Self-correcting loop) không cần sự can thiệp của người dùng.

---

## 🗺️ 2. KHUNG VÒNG ĐỜI 6 GIAI ĐOẠN (6-STAGE PIPELINE LIFE CYCLE)

Hệ thống phân rã chuỗi cung ứng kỹ năng thành 6 giai đoạn chuyên môn hóa sâu:

```
Stage 0: Explorer        ──► GATE 0 (Duyệt duy nhất bằng Chat UI)
     │
     ▼ (Tự động hóa toàn phần phía sau)
Stage 1: Architect
     │
     ▼
Stage 2: Planner
     │
     ▼
Stage 3: Builder
     │
     ▼
Stage 4: Tester (Spawn Subagent + Docker Sandbox)  ◄──► diagnostic.json (Rollback < 85%)
     │
     ▼ (Confidence >= 85%)
Stage 5: Indexer (Packaging & Knowledge Distiller)
```

### Chi tiết các Stage & Giao thức Dữ liệu (State Ledger Contracts)

| Stage | Tên Skill | Trách nhiệm chính | Dữ liệu đầu vào (Input) | Dữ liệu sản xuất (Output) |
| :--- | :--- | :--- | :--- | :--- |
| **0** | `skill-explorer` | Khảo sát nghiệp vụ, phân tích rủi ro & sinh bộ tiêu chí chất lượng thực chất | User Request + Knowledge base | `exploration.json`<br>`criteria.json` |
| **1** | `skill-architect` | Thiết kế cấu trúc tĩnh (7 Zones) và động (sequence flow). Lập Mitigation Map | `exploration.json`<br>`criteria.json` | `blueprint.json` |
| **2** | `skill-planner` | Phân rã thiết kế thành kế hoạch công việc có cấu trúc đồ thị phi chu kỳ (DAG) | `blueprint.json`<br>`criteria.json` | `dag_plan.json` |
| **3** | `skill-builder` | Thực thi code thực chất (SKILL.md + 3 file tri thức cốt lõi), cấm mock/placeholder | `dag_plan.json`<br>`blueprint.json`<br>`criteria.json` | Thư mục mã nguồn kỹ năng |
| **4** | `skill-tester` | Spawn subagent, chạy sandbox, sinh edge cases, tính Confidence Score | `criteria.json`<br>Mã nguồn vừa build | `verification.json`<br>`diagnostic.json` (nếu hỏng) |
| **5** | `skill-indexer` | Đóng gói kỹ năng, cập nhật llms.txt và trích xuất tri thức kinh nghiệm tự học | `verification.json`<br>Mã nguồn kỹ năng | README.md + llms.txt + `knowledge/experience/` |

---

## 🤖 3. KIẾN TRÚC MULTI-AGENT & ĐÓNG GÓI NGỮ CẢNH SUBAGENT

Để giải quyết vấn đề loãng ngữ cảnh ở session chính và tận dụng ưu điểm của Subagents (cửa sổ ngữ cảnh riêng biệt), Master Skill Suite Ver_2.0.0 thiết lập **Giao thức Đóng gói Ngữ cảnh Subagent (Subagent Context Isolation Protocol)**:

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

### 3.1. Tester Subagent (Stage 4)
*   **Lý do spawn:** Việc chạy Sandbox và sinh edge cases tạo ra log khổng lồ làm đầy ngữ cảnh session chính, đồng thời tăng nguy cơ bị Prompt Injection khi chạy thử code lạ.
*   **Context Package:** Chỉ nạp `criteria.json` + Thư mục mã nguồn vừa build + file chỉ dẫn `tester_rules.yaml`. Không nạp lịch sử chat thiết kế.
*   **Hoạt động:** Chạy Sandbox Docker cô lập, tự sinh tối thiểu **2 Edge Cases độc lập**, quét Semantic Placeholders, tính Confidence Score và chỉ trả về file báo cáo chắt lọc JSON.

### 3.2. Research Subagent (Stage 0)
*   **Lý do spawn:** Khi Explorer phân tích công nghệ/API phức tạp mà tài liệu tri thức dự án chưa đầy đủ.
*   **Context Package:** Chỉ dẫn câu hỏi trọng tâm + đường dẫn mã nguồn/API cần quét.
*   **Hoạt động:** Quét sâu mã nguồn đích, chắt lọc tri thức thành tệp JSON cô đọng gửi về session chính.

---

## 🔄 4. GIAO THỨC CHẨN ĐOÁN VÀ PHỤC HỒI CASE (CASE RECOVERY @ 85%)

Khi Tester Subagent phát hiện mã nguồn không đạt chuẩn chất lượng thực chất (chỉ số tự tin calculated < 85%), hệ thống sẽ tự động kích hoạt vòng lặp chẩn đoán rollback khép kín:

### 4.1. Công thức tính toán chỉ số tự tin thực chất (Fact-Based Confidence Score)
$$\text{Confidence Score} = 0.4 \times (\text{Sandbox Test Pass Rate}) + 0.3 \times (1 - \text{Semantic Placeholder Density}) + 0.3 \times (\text{Static Analysis \& Lint Status})$$
*   *Sandbox Test Pass Rate:* Tỷ lệ test case vượt qua (bao gồm cả Edge Cases).
*   *Semantic Placeholder Density:* Mật độ hàm rỗng, hàm mock cứng hoặc cấu trúc logic thiếu xử lý lỗi. **Bắt buộc = 0 để đạt PASS.**
*   *Static Analysis & Lint Status:* Trạng thái biên dịch và kiểm tra lỗi tĩnh.

### 4.2. Vòng lặp phản hồi chẩn đoán tự sửa lỗi (Closed-Loop Diagnostic)
1.  Tester Subagent sinh tệp `diagnostic.json` chứa: ID test case bị hỏng, phân loại lỗi, tệp vật lý + số dòng bị lỗi, log stdout lỗi sandbox và gợi ý định hướng kỹ thuật sửa lỗi.
2.  Tín hiệu chẩn đoán tự động được chuyển ngược về Stage 1 (Architect) hoặc Stage 2 (Planner).
3.  Architect/Planner tự động đọc `diagnostic.json`, định vị và cập nhật lại thiết kế/kế hoạch, rồi chuyển giao cho Builder viết lại code.
4.  Vòng lặp tự sửa lỗi chạy tối đa **3 lần** tự động mà không làm phiền người dùng.

---

## 📦 5. MÔ-ĐUN HÓA ĐỘC LẬP & ĐỊNH TUYẾN PIPELINE LINH HOẠT

### 5.1. Loose Coupling (Mô-đun hóa)
Mỗi Stage được đóng gói thành một mô-đun chức năng độc lập. Có thể chạy độc lập Stage 4 (Tester Subagent) để kiểm tra một skill viết tay bất kỳ bằng cách cung cấp tệp `criteria.json` bên ngoài. Có thể chạy Stage 5 (Indexer) độc lập để đăng ký và trích xuất tri thức từ một báo cáo kiểm thử sẵn có.

### 5.2. Dynamic Re-routing (Định tuyến động)
*   **Bypass thông minh:** Khi Steve chỉ thay đổi một tài liệu tri thức nhỏ hoặc sửa lỗi cú pháp trong một kỹ năng đang chạy, hệ thống phân tích Context Diff và tự động bỏ qua Stage 0 và Stage 1, đi thẳng từ Stage 2 hoặc Stage 3.
*   **Re-routing khi lỗi:** Tester tự động phân loại lỗi để re-route về đúng stage phù hợp: lỗi logic thuật toán re-route về Stage 3 (Builder), lỗi cấu trúc/file vật lý re-route về Stage 1 (Architect).

---

## 📚 6. QUẢN LÝ VÀ SỬ DỤNG SKILL SAU KHI BUILD (POST-BUILD LIFECYCLE)

Sau khi một kỹ năng được xây dựng thành công, việc quản lý và đưa vào sử dụng phải tuân thủ quy trình an toàn tuyệt đối:

### 6.1. Đồng bộ Runtime Nguyên tử (Staging Atomic Swap Protocol)
Để tránh gây crash cho agent đang hoạt động trong session chính khi chép đè trực tiếp vào `.hermes/skills/`:
1.  Indexer tạo một bản cài đặt thử nghiệm tại `.hermes/skills/.staging/{skill-name}/`.
2.  Kích hoạt một dry-run test độc lập tại môi trường staging.
3.  Nếu vượt qua, thực hiện hoán đổi nguyên tử (atomic swap/mv) thư mục staging thành production runtime an toàn tuyệt đối.

### 6.2. Nạp Tri thức Động theo Nhu cầu (On-Demand Activation)
Để tiết kiệm 60-90% token budget và giữ session sạch sẽ, kỹ năng mới được đóng gói theo nguyên lý Layering:
*   `SKILL.md` đóng vai trò là **L0 Anchor (Mục lục Động)**, chỉ chứa metadata kích hoạt (`when_to_use`) và các liên kết markdown tuyệt đối dẫn tới các file tri thức thành phần.
*   AI agent khi sử dụng kỹ năng sẽ tự động kích hoạt luật và chỉ đọc đúng file tri thức cần thiết (`policy/guidelines.yaml` hoặc `knowledge/concepts.md`) tương ứng với tác vụ hiện tại, thay vì đọc toàn bộ thư mục.

---

## 📚 7. GIAO THỨC CHUYỂN HÓA TRI THỨC TỰ HỌC (SELF-LEARNING DISTILLER)

Để hệ thống tự học hỏi và cập nhật từ các sự cố/kinh nghiệm thực tế, Stage 5 (Indexer) vận hành một giao thức trích xuất tri thức tự động:
1.  Đọc hiểu các logs sandbox, lỗi và các tinh chỉnh thủ công của lập trình viên trong quá trình dry-run.
2.  Trích xuất bài học kinh nghiệm và mã hóa chúng thành cấu trúc chuẩn `standards.md` của Steve:
    *   **YAML:** Các ràng buộc cứng (constraints, must, must_not).
    *   **Markdown:** Giải thích kiến trúc và hiện tượng logic.
    *   **XML tags:** Các ví dụ Good/Bad minh họa thực tế.
3.  Ghi trực tiếp vào tệp tri thức tự học `knowledge/experience/{skill-name}.md`.
4.  Tự động đăng ký tệp tri thức mới vào `knowledge/README.md` để các lượt chạy sau của Suite tự động nạp làm dữ liệu tham chiếu.

---

## 🔬 8. BỘ TIÊU CHÍ ĐÁNH GIÁ THIẾT KẾ ĐẠT CHUẦN (DEFINITION OF DONE)

Một thiết kế được coi là Đạt chuẩn (Clean & Solid) khi và chỉ khi vượt qua các tiêu chí nghiệm thu kiến trúc sau:

1.  **ZPI (Zero Placeholder Integrity):** Mật độ placeholder = 0% thực chất (quét phát hiện logic mock cứng).
2.  **SCR (Self-Correction Rate):** Tự động rollback sửa lỗi logic/biên dịch thành công >= 80% qua diagnostic loop.
3.  **SAA (Subagent Autonomy):** Tester Subagent chạy hoàn toàn độc lập, không làm tràn log rác về session chính.
4.  **ECC (Edge-Case Coverage):** Tester tự sinh thành công 2 Edge Cases độc lập để tra tấn mã nguồn.
5.  **KRL (Knowledge Retrieval Latency):** Số lượng cuộc gọi công cụ đọc file của AI khi sử dụng kỹ năng mới giảm xuống dưới 3 cuộc gọi.
