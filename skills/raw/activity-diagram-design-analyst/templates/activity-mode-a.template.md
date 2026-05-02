# Mode A: New Activity Diagram Design
> **Target**: {{Use Case Name}}

---

## 1. Mermaid Source (Clean Architecture Model)
```mermaid
flowchart TD
    subgraph Actor [{{Actor Name}}]
        Start((Start)) --> A1[Action 1 {{Trace: context_source}}]
    end
    
    subgraph Application [App / Use Case]
        B1[Wait for input...]
    end
    
    subgraph Domain [Core Business Logic]
        D1{Decision Rule? {{Trace: business_rule_id}}}
    end
    
    subgraph External [Infra / Systems]
        E1[Save to DB {{Trace: technical_spec}}]
    end

    %% Flow connections
    A1 --> B1 --> D1
    D1 -- Yes --> E1 --> End(((End)))
    D1 -- No --> EndFail(((Report Error)))
```

---

## 2. Design Decisions Rationale
- **Layering**: Giải thích lý do phân tách các Action vào từng lane cụ thể.
- **Rule Enforcement**: Chỉ ra các Decision Node tương ứng với Business Rules trong Context.
- **Exception handling**: Liệt kê các luồng lỗi đã được cover.

---

## 3. Interaction Gate 2 Checklist
- [ ] Assumptions đã được liệt kê ở mục Open Questions?
- [ ] Swimlanes đã tuân thủ B-U-E?
- [ ] Trace tags đã được gắn vào các node quan trọng?
