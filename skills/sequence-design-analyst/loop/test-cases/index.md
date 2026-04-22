# Test Cases for Sequence Design Analyst

## TC01: Luồng Đăng Nhập (Auth Flow)
- **Input**: "Vẽ sơ đồ sequence cho chức năng đăng nhập thành công."
- **Expected**:
    - Actor: User.
    - Path: LoginForm -> AuthService -> Payload -> MongoDB.
    - Fragment: `alt` for login success/fail.
    - Logic: Set cookie after success.

## TC02: Luồng Thanh Toán (Payment Flow)
- **Input**: "Vẽ luồng thanh toán qua VNPay."
- **Expected**:
    - Actor: User, VNPay (External).
    - Path: CheckoutPage -> OrderService -> VNPayService -> Gateway.
    - Logic: Redirect logic and IPN callback.

## TC03: Luồng CRUD Sản Phẩm (Product Management)
- **Input**: "Vẽ luồng Admin tạo mới một bó hoa (Product Bouquet)."
- **Expected**:
    - Actor: Admin.
    - Path: AdminPage -> ProductService -> Payload (products collection) -> MongoDB.
    - Logic: Validation trước khi create.
