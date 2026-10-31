# Kết quả kiểm tra ngày 31/10/2026

## Đánh giá

Ban đầu thư mục chỉ có 9 mô tả vai trò, AGENTS.md trống, chưa có code sản phẩm.
Task VS Code trỏ tới projects/premium-ecommerce không tồn tại. Lockfile dưới
projects/ không có package.json hay dependency. Chưa có quy trình cho app native,
phân quyền file, contracts, bằng chứng nghiệm thu hoặc kiểm tra cấu hình.

Sau chỉnh sửa, bộ khung có thể dùng để **bắt đầu phát triển web và app** bằng
runtime hỗ trợ agent. Chưa có sản phẩm để kết luận web/app đã chạy được.

## Những phần đã bổ sung

- AGENTS.md có quy trình triển khai, phối hợp worker và tiêu chí theo nền tảng.
- 12 vai trò cho VS Code và bản TOML đồng bộ cho Codex; có mobile, desktop, design.
- Giới hạn mặc định ba worker; không tự đổi model hay quyền người dùng.
- Template đặc tả, kiến trúc, contracts, ownership và verification theo sản phẩm.
- Tool Python không cần thư viện ngoài: doctor, init, sync-agents, verify.
- Task VS Code tổng quát, ignore file sinh/secret và workflow CI Windows/Linux.
- Bỏ task trỏ sai và lockfile rỗng không gắn với ứng dụng nào.

## Bằng chứng và giới hạn kiểm chứng

Môi trường kiểm tra tại máy hiện tại: Windows, Python 3.14.0, Node 24.21.0,
Codex CLI 0.166.0-alpha.5.1.

- `python tools/factory.py doctor`: PASS cấu hình; 12 agent đồng bộ và TOML parse
  được, tasks JSON hợp lệ. Danh sách SDK chỉ là thông tin tìm executable trên PATH.
- `python -m unittest discover -s tests -v`: 12 test PASS trên Windows, bao gồm
  thực thi process thật, npm.cmd, timeout, exit code lỗi, lệnh thiếu, path không hợp
  lệ, từ chối ghi đè, cấu hình thiếu và phát hiện vai trò mất đồng bộ.
- `git diff --check`: PASS cho các thay đổi tracked. CI đã cấu hình nhưng chưa
  chạy trên GitHub; chưa kiểm chứng Linux tại máy này.
- Chưa chạy một phiên Codex/VS Code mới để chứng minh việc tự load vai trò và
  điều phối đầy đủ. Kiểm tra cú pháp/đồng bộ không thay thế kiểm tra runtime đó.
- Chưa có ứng dụng: chưa có browser smoke, native build, emulator/device run,
  installer, signing hoặc deploy để nghiệm thu.

Có git, node/npm, codex, Java và dotnet trên PATH. Chưa tìm thấy flutter, dart,
adb và cargo trên PATH; điều này không chứng minh chúng chưa được cài ở nơi khác.
Chưa xác minh Android SDK/emulator, Apple build environment hay workload .NET.

## Bước dùng tiếp theo

Mở phiên Codex mới tại thư mục gốc hoặc chọn Software Factory Orchestrator trong
VS Code. Nêu sản phẩm và target cụ thể; agent tạo dự án, chọn stack, kiểm tra SDK,
triển khai code thật và cấu hình lệnh verify theo sản phẩm. Cài toolchain còn thiếu
khi đã chốt nền tảng, rồi nghiệm thu bằng browser/device/package thực tế.
