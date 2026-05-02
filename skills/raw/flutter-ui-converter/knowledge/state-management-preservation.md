# State Management Preservation (Bloc)

> **Mục tiêu**: Đảm bảo AI Agent bảo toàn 100% logic quản lý trạng thái khi thay đổi giao diện. Dự án `tranphueco` sử dụng **Bloc** (không phải Cubit) làm giải pháp quản lý trạng thái chính.

## 1. Nguyên tắc Bất biến (Immutability Rules)

Tuyệt đối KHÔNG thực hiện các hành động sau:
- Không tạo thêm Bloc mới hoặc xóa Bloc hiện có.
- Không sửa đổi định nghĩa các Event (`MyBlocEvent`) hoặc State (`MyBlocState`).
- Không thay đổi logic mapping từ Event sang State bên trong file `_bloc.dart`.

## 2. Bảo toàn Bloc Widgets (UI Level)

Khi cấu trúc lại cây Widget (Widget Tree) để phù hợp với UI mới, bạn phải xác định và giữ nguyên vị trí, vai trò của các widget sau:

- **`BlocBuilder`**: Dùng để build UI dựa trên state. Khi convert, chỉ được thay đổi phần UI được return bên trong hàm `builder: (context, state) { ... }`.
- **`BlocListener`**: Dùng để xử lý side-effects (navigation, show dialog, snackbar). Tuyệt đối giữ nguyên hàm `listener: (context, state) { ... }`.
- **`BlocConsumer`**: Là sự kết hợp của Builder và Listener. Giữ nguyên phần `listener`, chỉ sửa đổi phần `builder`.

**Lưu ý quan trọng về BuildContext (Provider Loss Risk):**
Khi bọc UI mới bằng các widget cấu trúc (Column, Row, Container), đảm bảo `BlocBuilder/Consumer` không bị đẩy ra ngoài phạm vi của `BlocProvider` cung cấp nó. Nếu màn hình sử dụng `BlocProvider.value`, hãy giữ nguyên cơ chế truyền value đó.

## 3. Bảo toàn Action/Event Triggers

Trong Source project (`tranphueco-redo-AI`), các nút bấm (buttons) thường có hàm `onTap: () {}` rỗng hoặc in log.
Khi đưa sang Target project, bạn **BẮT BUỘC** phải nối lại các sự kiện cũ:

*Ví dụ cấu trúc cũ:*
```dart
onPressed: () {
  context.read<LoginBloc>().add(SubmitLoginEvent(username, password));
}
```
*UI mới có thể thay đổi nút bấm, nhưng action bên trong `onPressed` hoặc `onTap` phải được giữ nguyên hoàn toàn.*

## 4. Kiểm tra Biến State

Đảm bảo UI mới hiển thị đúng các giá trị từ `state`.
*Ví dụ:* Nếu UI mới có một Text field hiển thị số dư, bạn phải map nó đúng với `state.balance` (hoặc tên biến tương ứng đang được dùng ở codebase cũ) thay vì hardcode giá trị từ bản thiết kế prototype.

---

## Reference Data

- **Data file**: `data/forbidden-patterns.yaml` — business logic patterns to preserve (Bloc/Cubit/Event/State classes)
- **Template**: `templates/conversion-log.md.template` — section "Logic Hooks Preserved"
- **Related knowledge**: `conversion-rules.md` — UI-only constraint principles
- **Related knowledge**: `flutter-ui-patterns.md` — BuildContext and widget tree structure
