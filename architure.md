# AGENT SKILL FRAMEWORK - TÀI LIỆU KIẾN TRÚC

================================================================================
                        PHẦN 1: TỔNG QUAN KIẾN TRÚC
================================================================================

## 1.1. Mô hình Meta-Skill Framework

Mô hình này định nghĩa cách tiếp cận tổng thể để xây dựng một bộ Agent Skill
có cấu trúc, logic và khả năng kiểm soát chất lượng.

```mermaid
graph TD
    subgraph MetaSkillFramework [MÔ HÌNH KIỂM CÁCH - META-SKILL FRAMEWORK]
        P1[PHA 1: NHẬN DIỆN<br/>Input/Output] --> P2[PHA 2: CHIẾN LƯỢC<br/>Checklist/Plan]
        P2 --> P3[PHA 3: THỰC THI<br/>Research/Action]
        
        P1 --> D1[Dữ liệu Gốc]
        P2 --> D2[Quy trình Chuẩn]
        P3 --> D3[Tương tác & Thẩm định]
        
        D1 --> LC[VÒNG LẶP KIỂM SOÁT<br/>Verify/Fix/Loop]
        D2 --> LC
        D3 --> LC
    end

    style MetaSkillFramework fill:#f9f9f9,stroke:#333,stroke-width:2px
    style LC fill:#e1f5fe,stroke:#01579b
```


## 1.2. Kiến trúc "Ngôi nhà" (Building Metaphor)

```mermaid
graph TD
    Outcome[MÁI NHÀ: GIÁ TRỊ ĐẦU RA - Outcome<br/>- Sản phẩm hoàn thiện, chính xác, có thẩm mỹ<br/>- Người dùng hài lòng và tin tưởng]
    
    subgraph Pillars [CÁC TRỤ CỘT]
        T1[TRỤ 1: TRI THỨC<br/>Knowledge]
        T2[TRỤ 2: QUY TRÌNH<br/>Logic/Steps]
        T3[TRỤ 3: KIỂM SOÁT<br/>Guardrails]
    end
    
    Foundation[NỀN MÓNG: NGHIÊN CỨU & PHÂN TÍCH<br/>Input, Tools, Environment, User Pain-points]
    
    Foundation --> Pillars
    Pillars --> Outcome

    style Outcome fill:#e8f5e9,stroke:#2e7d32
    style Foundation fill:#fff3e0,stroke:#ef6c00
    style Pillars fill:#f3e5f5,stroke:#7b1fa2
```


================================================================================
                  PHẦN 2: CÁC THÀNH PHẦN KIẾN TRÚC (ZONES)
================================================================================

## 2.1. Cấu trúc thư mục chuẩn

```mermaid
mindmap
  root((your-skill-name))
    SKILL.md:::core
    .skillfish.json
    knowledge
      standards.md
      best-practices.md
      design-patterns.md
    scripts
      python
        analyzer.py
        validator.py
        generator.py
      javascript
        formatter.js
        mermaid-render.js
      bash
        scan-project.sh
        setup-env.sh
        export-diagram.sh
    templates
      sequence.mmd
      class.mmd
      activity.mmd
    data
      config.yaml
      schema.json
      seed-data.csv
    loop
      checklist.md
      tasks.md
      phase-verify.md
      final-verify.md
      test-cases
        login-flow.md
        order-flow.md
    assets
      icons
      fonts
      images

    classDef core fill:#f96
```


## 2.2. Chi tiết từng Zone

| ZONE | MỤC ĐÍCH | VÍ DỤ NỘI DUNG | KHI NÀO AI ĐỌC? |
| :--- | :--- | :--- | :--- |
| **SKILL.md (Core)** | Linh hồn điều khiển | Persona, Steps, Guardrails | LUÔN LUÔN (khi skill được kích hoạt) |
| **knowledge/** | Tri thức chuẩn | UML rules, Design patterns | Khi cần tham khảo quy tắc |
| **scripts/** | Công cụ tự động hóa | Python analyzer, Bash generator | Khi cần thực thi logic phức tạp |
| **templates/** | Mẫu đầu ra | Mermaid templates, Code stubs | Khi cần tạo output chuẩn |
| **data/** | Cấu hình & dữ liệu cứng | YAML config, JSON schema | Khi cần đọc cấu hình cố định |
| **loop/** | Kiểm soát chất lượng | Checklist, Tasks, Test cases | SAU mỗi phase để tự kiểm tra |
| **assets/** | Tài nguyên tĩnh | Icons, Fonts, Images | Khi tạo output có media |



================================================================================
                     PHẦN 3: WORKFLOW XÂY DỰNG SKILL
================================================================================

## 3.1. Quy trình 5 bước

```mermaid
flowchart LR
    B1[BƯỚC 1: KHẢO SÁT<br/>Research] --> B2[BƯỚC 2: THIẾT KẾ<br/>Design]
    B2 --> B3[BƯỚC 3: XÂY DỰNG<br/>Build]
    B3 --> B4[BƯỚC 4: KIỂM ĐỊNH<br/>Verify]
    B4 --> B5[BƯỚC 5: BẢO TRÌ<br/>Maintenance]

    subgraph Details [Chi tiết từng bước]
        direction TB
        D1["- Xác định Pain Point<br/>- Thu thập Use Cases<br/>- Liệt kê Input/Output"]
        D2["- Phân vùng thành phần<br/>- Vẽ sơ đồ kiến trúc<br/>- Định nghĩa luồng làm việc"]
        D3["- Tạo cấu trúc thư mục<br/>- Nạp dữ liệu vào các vùng<br/>- Viết SKILL.md"]
        D4["- Chạy Test Cases<br/>- Verify Checklist<br/>- Rollback nếu Fail"]
        D5["- Feedback Loop<br/>- Version Control<br/>- Cập nhật Skill"]
    end

    B1 -.-> D1
    B2 -.-> D2
    B3 -.-> D3
    B4 -.-> D4
    B5 -.-> D5

    style B1 fill:#f9f,stroke:#333
    style B5 fill:#0ff,stroke:#333
```


## 3.2. Chi tiết từng bước

### Bước 1: Khảo sát (Research & Discovery)

    Mục tiêu: Hiểu rõ "vùng đất" mình định xây.
    
    Việc cần làm:
    [1] Xác định Input: Người dùng sẽ đưa cái gì? (Rác hay vàng?)
    [2] Xác định Tools: AI sẽ dùng Terminal, Browser hay Library nào?
    [3] Tìm ra "Điểm mù" của AI: AI thường sai ở đâu trong công việc này?

### Bước 2: Thiết kế (System Design)

    Mục tiêu: Tạo ra logic "tường minh" cho AI.
    
    Việc cần làm:
    [1] Xây dựng Quy trình logic (Flowchart): Bước A -> Bước B
    [2] Xác định Điểm dừng tương tác: Khi nào AI PHẢI hỏi người dùng?
    [3] Định nghĩa Định dạng Output: Mermaid, Markdown, hay Code?

### Bước 3: Xây dựng (Build)

    Mục tiêu: Viết file SKILL.md và nạp tài nguyên.
    
    Việc cần làm:
    [1] Persona: Định vị AI là Senior Architect hay Senior Coder
    [2] Phase-based Steps: Chia nhỏ công việc thành các Pha
    [3] Tạo templates, scripts, knowledge files

### Bước 4: Kiểm định (Verify)

    Mục tiêu: Đảm bảo Skill hoạt động đúng.
    
    Việc cần làm:
    [1] Chạy Test Cases
    [2] Verify Checklist
    [3] Rollback nếu phát hiện lỗi

### Bước 5: Bảo trì (Maintenance)

    Mục tiêu: Giữ cho Skill không bị "lỗi thời".
    
    Việc cần làm:
    [1] Feedback Loop: Ghi lại chỗ AI làm dở
    [2] Version Control: Cập nhật khi môi trường thay đổi


================================================================================
                   PHẦN 4: CƠ CHẾ KIỂM SOÁT (LOOP/VERIFY)
================================================================================

## 4.1. Hai chế độ kiểm soát

```mermaid
flowchart TD
    subgraph LoopZone [VÙNG LOOP - KIỂM SOÁT CHẤT LƯỢNG]
        direction TB
        Simple[SIMPLE MODE<br/>1 lần cuối]
        Phase[PHASE MODE<br/>Mỗi phase]
        
        SimpleCheck{Khi nào dùng?}
        PhaseCheck{Khi nào dùng?}
        
        SimpleFlow[Input -> Work -> Output<br/>-> VERIFY]
        PhaseFlow[Phase 1 -> V<br/>Phase 2 -> V<br/>Phase 3 -> V<br/>Final -> VV]

        Simple --> SimpleCheck
        Phase --> PhaseCheck
        
        SimpleCheck -->|Yêu cầu đơn giản| SimpleFlow
        PhaseCheck -->|Yêu cầu phức tạp| PhaseFlow
    end

    style Simple fill:#fff9c4,stroke:#fbc02d
    style Phase fill:#c8e6c9,stroke:#388e3c
```


## 4.2. Cấu trúc thư mục loop/

```
loop/
+-- checklist.md            <-- Danh sách kiểm tra chung
+-- tasks.md                <-- Công việc cần hoàn thành
+-- phase-verify.md         <-- Checklist riêng cho từng Phase
+-- final-verify.md         <-- Checklist kiểm tra cuối cùng
+-- test-cases/
    +-- login-flow.md
    +-- order-flow.md
```


================================================================================
                    PHẦN 5: VÙNG SCRIPTS (CÔNG CỤ)
================================================================================

## 5.1. Ba loại script

```mermaid
graph LR
    subgraph ScriptsZone [VÙNG SCRIPTS - CÔNG CỤ THỰC THI]
        direction TB
        Python[Python<br/>Xử lý logic, phân tích text]
        JS[JavaScript<br/>Xử lý frontend, JSON, DOM]
        Bash[Bash<br/>Lệnh hệ thống, file system]
        
        Python --- P1[analyzer.py<br/>validator.py<br/>generator.py]
        JS --- J1[formatter.js<br/>mermaid-render.js]
        Bash --- B1[scan-project.sh<br/>setup-env.sh<br/>export-diagram.sh]
    end

    style Python fill:#e3f2fd,stroke:#1e88e5
    style JS fill:#fffde7,stroke:#fdd835
    style Bash fill:#f5f5f5,stroke:#757575
```


## 5.2. Ma trận chọn script theo công việc

| LOẠI CÔNG VIỆC | SCRIPT ƯU TIÊN |
| :--- | :--- |
| **Phân tích text, NLP** | Python |
| **Xử lý JSON, format data** | JavaScript |
| **Quét thư mục, đọc cấu trúc** | Bash |
| **Validate syntax** | Python |
| **Render diagram** | JavaScript |
| **Tạo file, copy template** | Bash |
| **Gọi API bên ngoài** | Python/JS |



================================================================================
               PHẦN 6: PROGRESSIVE DISCLOSURE (NẠP TÀI NGUYÊN)
================================================================================

## 6.1. Hai tầng nạp file

```mermaid
flowchart TD
    subgraph ProgressiveDisclosure [CƠ CHẾ NẠP TÀI NGUYÊN]
        direction TB
        Mandatory[TẦNG 1: BẮT BUỘC ĐỌC<br/>Mandatory Loading]
        Optional[TẦNG 2: TỰ QUYẾT ĐỊNH<br/>Conditional Loading]
        
        Mandatory --- M1["- SKILL.md<br/>- knowledge/standards.md<br/>- loop/checklist.md"]
        Optional --- O1["- knowledge/design-patterns.md<br/>- templates/*.mmd<br/>- data/schema.json"]
        
        Mandatory -->|Sau khi đọc xong| Optional
    end

    style Mandatory fill:#ffcdd2,stroke:#e53935
    style Optional fill:#c5cae9,stroke:#3f51b5
```



================================================================================
                  PHẦN 7: LUỒNG HOẠT ĐỘNG CỦA AI AGENT
================================================================================

## 7.1. Execution Flow

```mermaid
sequenceDiagram
    participant U as USER
    participant A as AI AGENT
    participant K as Knowledge Zone
    participant S as Scripts Zone
    participant T as Templates Zone
    participant L as Loop Zone

    U->>A: Input "Vẽ sequence cho Login"
    A->>A: STEP 1: Đọc SKILL.md (Persona & Steps)
    A->>A: STEP 2: Phân tích Input (Use Case)
    Note over A,U: [Interaction Point] Hỏi nếu thiếu thông tin
    A->>K: STEP 3: Tham khảo standards.md, uml-rules.md
    A->>S: STEP 4: Chạy analyzer.py (Bóc tách entities)
    A->>T: STEP 5: Áp dụng seq.mmd làm khung
    A->>A: STEP 6: Tạo Output (Mermaid code)
    A->>L: STEP 7: Tự kiểm tra với checklist.md
    alt Fail?
        L-->>A: Quay lại Step tương ứng
    else Pass?
        A->>U: Trả kết quả cuối cùng
    end
```



================================================================================
                   PHẦN 8: KIẾN TRÚC TỔNG HỢP (v2.0)
================================================================================

```mermaid
graph TD
    Skill((SKILL.md<br/>CORE))
    
    subgraph Tier1 [TẦNG 1: BẮT BUỘC]
        K1[knowledge/standards]
        L1[loop/checklist]
    end
    
    subgraph Tier2 [TẦNG 2: TỰ QUYẾT]
        S1[scripts/]
        T1[templates/]
        D1[data/]
        A1[assets/]
        K2[knowledge/patterns]
    end

    Skill --> Tier1
    Skill --> Tier2

    style Skill fill:#f96,stroke:#333,stroke-width:4px
    style Tier1 fill:#fff9c4,stroke:#fbc02d
    style Tier2 fill:#e1f5fe,stroke:#01579b
```



================================================================================
                            PHẦN 9: PHỤ LỤC
================================================================================

## 9.1. Nguyên tắc viết SKILL.md

    [1] Imperative Form: Luôn bắt đầu bằng động từ mạnh
        Ví dụ: "Analyze the input", "Generate the code"
        KHÔNG dùng: "You should analyze"
    
    [2] Progressive Disclosure: Chỉ để những gì AI cần làm NGAY LẬP TỨC
        trong SKILL.md. Tài liệu tham khảo dài để trong references/
    
    [3] Verified Steps: Mỗi giai đoạn (Phase) phải kết thúc bằng:
        "Check the output against the checklist in loop/checklist.md"

## 9.2. Điểm dừng tương tác (Interaction Points)

    AI PHẢI dừng lại và hỏi người dùng khi:
    [1] Thông tin đầu vào không đủ để xử lý
    [2] Có nhiều cách hiểu khác nhau
    [3] Cần xác nhận trước khi thực hiện hành động có rủi ro
    [4] Confidence Score dưới 70%

## 9.3. Cơ chế Rollback

    Nếu ở Phase N phát hiện lỗi từ Phase M (M < N):
    [1] Ghi nhận lỗi và nguyên nhân
    [2] Thông báo người dùng về việc quay lại
    [3] Quay lại Phase M và sửa lỗi
    [4] Tiếp tục lại từ Phase M

================================================================================
                               KẾT THÚC TÀI LIỆU
================================================================================
Phiên bản: 2.0
Ngày tạo: 2026-02-09
Tác giả: Vũ Thương Hải (với sự hỗ trợ của AI Agent)
================================================================================