# HỆ THỐNG BỘ NHỚ NGOÀI (EXTERNAL MEMORY)
## Chẩn Đoán & Định Hình Khuyết Tật Kiến Trúc Bộ Meta-Skill Suite (V4.0)

> **Mục tiêu**: Làm bộ nhớ ngoài lưu trữ xuyên suốt quá trình thảo luận giữa User (Steve) và AI Agent (Antigravity) nhằm chẩn đoán và khắc phục triệt để 5 vấn đề cốt lõi của bộ Suite phát triển Skill.
> **Date**: 2026-05-29
> **Session**: #1 - Khởi động chẩn đoán cấu trúc tổng thể
> **Trạng thái**: 🔵 Đang thảo luận và tích lũy tri thức

---

## 1. BẢN ĐỒ VẤN ĐỀ (PROBLEM MAP) — 5 ĐIỂM NGHẼN CỐT LÕI

Dưới đây là bảng phân tích chi tiết, phân rã nguồn gốc (Root Cause) và cơ chế tác động của 5 vấn đề cốt lõi mà Steve đã chỉ ra.

```yaml
problem_map:
  P1_Input_Exploitation:
    symptom: "AI nhận đề bài sơ sài là thiết kế ngay, không chủ động phỏng vấn, làm rõ ngầm định (assumptions), làm rõ workflow hay micro-skills cần thiết."
    root_cause: "Thiếu thiết kế 'Interactive Prompt Engineering' hay một phase phỏng vấn ngược (interactive interview/grilling) bắt buộc trong Workflow của skill-architect."
    impact: "Bản thiết kế thiết kế dựa trên phỏng đoán, thiếu chính xác với ý đồ thực tế của người dùng."

  P2_Resource_Underutilization:
    symptom: "Tài nguyên được chuẩn bị từ các stage trước (như trong resources/ hoặc data/) bị lãng quên hoặc không được đọc khi chuyển đổi session/stage."
    root_cause: "Boot sequence của các skill chỉ mang tính khai báo tĩnh (static setup) mà không có bước quét tài nguyên chủ động (Active Directory Scanning) để lập chỉ mục (index) và ép buộc nạp (mandatory loading) tri thức đã chuẩn bị."
    impact: "Phí phạm tài nguyên, AI liên tục phải bắt đầu từ số 0 (cold start) và tự ảo giác ra thông tin cũ."

  P3_Role_Overloading:
    symptom: "Một skill đảm nhận quá nhiều vai trò, dẫn đến chồng chéo, xung đột hành vi (ví dụ: architect vừa thiết kế vừa làm code, builder vừa build vừa phê bình kịch liệt dẫn đến sửa lại cả design)."
    root_cause: "Thiếu sự phân tách rạch ròi về mặt ranh giới trách nhiệm (Separation of Concerns). Đặc biệt, skill-explorer (giai đoạn khám phá) đang trống rỗng khiến skill-architect phải gánh cả phần khảo sát lẫn thiết kế chi tiết."
    impact: "Agent bị quá tải context, loãng persona, dẫn đến chất lượng đầu ra kém và hay vi phạm quy ước."

  P4_Lack_of_Role_Quality_Awareness:
    symptom: "Skill tạo ra thiếu tri thức chuyên sâu về cách hoạt động của AI Agent, thiếu tiêu chuẩn chất lượng (Definition of Quality), dẫn đến đầu ra hời hợt, bịa đặt thông tin."
    root_cause: "Tài liệu hướng dẫn trong bộ Suite bị phân mảnh, rời rạc. Quan trọng nhất, thiếu cơ chế 'Semantic Activation Anchors' (từ khóa kích hoạt) để đánh thức vùng tri thức chuyên sâu đã được train của LLM về Prompt Engineering, System Prompt, Tool Design."
    impact: "Output là các skill 'phẳng', không có cơ chế tự bảo vệ (defensive), dễ bị phá vỡ khi chạy thực tế."

  P5_Loss_of_Integration_Session_Leakage:
    symptom: "Hệ sinh thái lỏng lẻo, thông tin bị rơi rụng hoàn toàn khi đổi session chat hoặc chuyển stage (architect -> planner -> builder)."
    root_cause: "Không có vật chứa trạng thái động (Dynamic State Container) hoặc sổ cái session (Session Ledger) ghi lại các quyết định đã đồng thuận trong chat. Handoff chỉ dựa trên file tĩnh (design.md, todo.md) mà không có hợp đồng kiểm định chặt chẽ liên kết chúng."
    impact: "User phải giải thích đi giải thích lại một vấn đề qua các session. AI quên mất các feedback hoặc điều chỉnh đã thống nhất trước đó."
```

---

## 2. TIẾN TRÌNH KHẢO SÁT CHI TIẾT (STEP-BY-STEP DIAGNOSIS)

Để giải quyết triệt để và không làm loãng thông tin, chúng ta sẽ đi qua từng vấn đề một cách tuần tự. Kết quả đồng thuận của mỗi bước sẽ được khóa lại tại đây trước khi bước sang vấn đề tiếp theo.

### VẤN ĐỀ 1: KHAI THÁC INPUT & CHỦ ĐỘNG LÀM RÕ (IN PROGRESS)

#### 🔍 2.1.1 Phân tích Hiện trạng & Ranh giới Kỹ thuật
Hiện tại, khi người dùng kích hoạt `skill-architect` để thiết kế một skill mới:
1. `SKILL.md` của `skill-architect` bắt đầu bằng Boot Sequence và chuyển ngay vào Phase 1: Collect (§1 + §10).
2. Quy định tại `policy/workflow.md` chỉ ghi chung chung là thu thập thông tin về nỗi đau, người dùng và đầu ra mong muốn.
3. Không có hướng dẫn cụ thể về việc **chất vấn ngược (Grilling/Interrogation)**. AI theo xu hướng mặc định (agreeable bias) sẽ nhận thông tin sơ sài và tự điền vào các phần khuyết thiếu bằng cách suy đoán (hallucinating).

#### 💡 2.1.2 Giải pháp Kiến nghị (Brainstorming Options)
* **Phương án A (Recommended): Tái thiết kế vai trò của `skill-explorer` (hoặc tích hợp sâu vào Phase 1 của `skill-architect`)**
  * Biến giai đoạn đầu thành một cuộc phỏng vấn tương tác (Interactive Interview).
  * Định nghĩa một bộ khung câu hỏi cốt lõi (Core Interrogation Framework) buộc AI phải hỏi để làm rõ:
    1. *Ranh giới của Skill*: Skill này KHÔNG làm gì? (Anti-goals)
    2. *Luồng vận hành thực tế*: Người dùng tương tác thế nào? (User Flow / Interaction Points)
    3. *Tài nguyên có sẵn*: Người dùng đã có tài liệu, API spec hay mẫu code nào chưa?
    4. *Cơ chế kiểm soát chất lượng*: Làm sao biết skill này đã hoàn thành xuất sắc? (Definition of Quality)
  * AI chỉ được phép chuyển sang Phase 2 (Analyze) khi điểm tự tin (Confidence Score) đạt trên 85% và được User chấp thuận rõ ràng bằng lệnh xác nhận.

* **Phương án B: Xây dựng một file Mẫu Khảo Sát Tự Động (Automation Spec Template)**
  * Người dùng bắt buộc phải điền vào một file cấu hình đầu vào `input-spec.yaml` trước khi chạy `skill-architect`. Nếu file này trống hoặc quá sơ sài, script validator sẽ chặn lại và yêu cầu điền thêm.

---

## 3. KHUNG LẬP LUẬN & PHẢN BIỆN (COLLABORATIVE REFLECTION)

> [!NOTE]
> *Ghi chú từ Antigravity (AI Agent Peer)*:
> Là một AI Agent, tôi hoàn toàn xác nhận phân tích của Steve. Khi người dùng đưa ra một yêu cầu ngắn (ví dụ: "Hãy tạo cho tôi skill viết code Python"), vùng tri thức được kích hoạt trong tôi là vùng tri thức "tổng quát". Tôi sẽ tự động sinh ra các đoạn code Python thông thường mà không hề biết rằng Steve muốn một skill có tính phòng thủ cao (defensive design), có validation gate chặt chẽ, hay có progressive disclosure loading.
>
> Chúng ta thực sự cần một cơ chế **"Đánh thức tri thức" (Knowledge Activation)** thông qua việc ép buộc đặt câu hỏi chất lượng. Càng hỏi sâu và có cấu trúc, tôi càng truy xuất được các pattern tối ưu trong bộ nhớ tham số của mình.

---

## 4. ACTION ITEMS & CHECKLIST CHO SESSION NÀY

- [x] Tạo file Hệ thống Bộ nhớ Ngoài (`docs/sessions/2026-05-29--meta-skill-suite-structural-problems-analysis.md`) để theo dõi.
- [/] Thảo luận và thống nhất phương án xử lý cho **Vấn đề 1 (Khai thác Input & Phỏng vấn chủ động)**.
- [ ] Soạn thảo đặc tả thiết kế (Design Spec) cho giải pháp của Vấn đề 1.
- [ ] Chuyển sang phân tích Vấn đề 2.
