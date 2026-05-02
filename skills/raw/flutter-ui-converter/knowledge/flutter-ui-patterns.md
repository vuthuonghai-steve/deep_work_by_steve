# Flutter UI Patterns

> **Mục tiêu**: Cung cấp cho AI Agent kiến thức về các pattern xây dựng giao diện (UI) chuẩn xác trong Flutter để áp dụng khi convert UI.

## 1. Widget Tree Structure (Cấu trúc Cây Widget)

- **Tránh "Spaghetti Code" trong Widget Tree:** Không viết một file màn hình dài hàng ngàn dòng. Nếu một component phức tạp (như header, list item, bottom sheet), hãy tách (extract) nó ra thành một `StatelessWidget` riêng rẽ.
- **Sự khác biệt khi tách hàm vs tách class:** Luôn ưu tiên tách UI thành một `class Khac extends StatelessWidget` thay vì một hàm `Widget _buildKhac()`. Việc dùng class giúp Flutter tối ưu hóa rebuild (chỉ rebuild khi params thay đổi).

## 2. StatelessWidget vs StatefulWidget

- **Quy tắc mặc định:** Luôn bắt đầu bằng `StatelessWidget`.
- **Chỉ dùng StatefulWidget khi:** Màn hình hoặc component đó CẦN quản lý trạng thái nội bộ tạm thời KHÔNG liên quan đến Business Logic (ví dụ: `AnimationController`, `ScrollController`, `FocusNode`, trạng thái mở/đóng tạm thời của một dropdown local).
- **Khi convert:** Nếu Source project dùng `StatefulWidget` chỉ để UI nhấp nháy, nhưng Target project sử dụng `Bloc` hoặc `Cubit` (tức là state được quản lý từ bên ngoài), AI nên ưu tiên chuyển nó thành `StatelessWidget` kết hợp với `BlocBuilder`.

## 3. Quản lý BuildContext

- `BuildContext` cực kỳ quan trọng trong Flutter để truy xuất `Theme`, `MediaQuery`, và các `Provider`.
- Khi extract widget thành class, KHÔNG cần truyền `context` vào constructor. Tham số `context` sẽ có sẵn trong hàm `build(BuildContext context)`.
- Khi cấu trúc lại Widget Tree (bọc thêm `Container`, `Column`...), AI phải cực kỳ cẩn thận không làm mất đi các Provider đang được wrap ở node trên. Ví dụ: Nếu một widget dùng `BlocProvider.of(context)`, widget đó phải nằm bên dưới node `BlocProvider` trong cây giao diện.

## 4. Xử lý UI Asynchronous (FutureBuilder/StreamBuilder)

- Khi giao diện phụ thuộc vào dữ liệu load từ mạng, hạn chế sử dụng `setState`. 
- Target project đã có hệ thống quản lý trạng thái riêng (Bloc/Cubit). AI Agent KHÔNG tự ý bọc UI bằng `FutureBuilder` nếu hệ thống cũ đang dùng `BlocBuilder`. Giữ nguyên logic lấy dữ liệu của Target.

## 5. Tối ưu hóa UI

- Sử dụng từ khóa `const` ở bất cứ nơi nào có thể (cho các widget tĩnh như `Text`, `Padding`, `Icon`) để giảm tải cho Garbage Collector của Flutter.
- Khi làm việc với list dài, LUÔN LUÔN dùng `ListView.builder` hoặc `SliverList` thay vì dùng `ListView` thông thường hay `SingleChildScrollView` với `Column` để tránh vỡ bộ nhớ (Out of Memory).

---

## Reference Data

- **Related knowledge**: `state-management-preservation.md` — Bloc/Cubit patterns and BuildContext usage
- **Related knowledge**: `responsive-layout-rules.md` — widget tree structure for responsive layouts
- **Related knowledge**: `component-mapping-guide.md` — widget substitution and extraction patterns
- **Data file**: `data/forbidden-patterns.yaml` — anti-patterns to avoid (setState with async, etc.)
