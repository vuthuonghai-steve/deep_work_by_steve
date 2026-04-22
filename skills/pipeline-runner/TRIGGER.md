# Pipeline Trigger — UML Generation

```
/pipeline-runner <path-to-docs>
```

## Mục tiêu

Scan toàn bộ file trong thư mục input, phân tích nội dung, và sinh complete UML documentation bao gồm:
- Flow Diagrams (Business Process)
- Sequence Diagrams (User/System/DB interactions)
- Class Diagrams (Data models)
- Activity Diagrams (Detailed workflows)

## Input

- **Path**: Thư mục chứa tài liệu đầu vào (FR, specs, requirements...)
- **Output**: Thư mụcDocs/life-2/diagrams/

## Pipeline Configuration

Pipeline sẽ chạy tuần tự các skills:

```
flow-design-analyst
    ↓
sequence-design-analyst
    ↓
class-diagram-analyst
    ↓
activity-diagram-design-analyst
```

## Execution

1. **Khởi động**: Pipeline runner đọc pipeline.yaml
2. **Stage 1**: flow-design-analyst tạo flow diagrams
3. **Stage 2**: sequence-design-analyst tạo sequence diagrams
4. **Stage 3**: class-diagram-analyst tạo class diagrams
5. **Stage 4**: activity-diagram-design-analyst tạo activity diagrams
6. **Hoàn thành**: Tạo summary.md với tất cả outputs

## Usage

```bash
# Run pipeline với docs đầu vào
/pipeline-runner Docs/life-1/01-vision/FR/

# Resume nếu bị gián đoạn
/pipeline-runner --resume

# Check status
/pipeline-runner --status
```
