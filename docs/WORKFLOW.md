# Quy trình xây dựng sản phẩm

1. **Khảo sát:** đọc hướng dẫn, git status và code; xác định sản phẩm, nền tảng,
   SDK, giới hạn và tiêu chí nghiệm thu. Chỉ hỏi thông tin chặn lựa chọn sản phẩm.
2. **Đặc tả:** tạo/cập nhật brief, kiến trúc và contracts trong docs sản phẩm.
   Chọn stack theo yêu cầu; không tạo cả web/mobile/desktop khi chỉ cần một target.
3. **Chia việc:** ghi PLAN.md: nhiệm vụ, vai trò, file được sửa, dependency, đầu ra,
   tiêu chí và lệnh kiểm tra. Worker chỉ triển khai khi contracts và ownership rõ.
4. **Triển khai:** dựng luồng đầu cuối chạy được trước. Đánh dấu mock và thay bằng
   tích hợp thật nếu yêu cầu. Root xử lý dependencies và file dùng chung tuần tự.
5. **Tích hợp:** thu kết quả worker, đọc diff, nối API/UI/native và sửa xung đột.
   Không ghi đè thay đổi người dùng, xóa test hay bỏ qua lỗi để đạt xanh.
6. **Kiểm chứng:** cài dependencies theo lockfile, cấu hình check thật và chạy
   verify. Kiểm tra luồng chính, lỗi, từ chối truy cập trên browser/device cụ thể.
   Ghi bằng chứng và gate chưa chạy; dừng đúng process do phiên làm việc tạo ra.
7. **Review:** kiểm tra logic, contracts, bảo mật và ảnh hưởng nền tảng. Chỉ báo lỗi
   có bằng chứng; sửa lỗi liên quan và chạy lại kiểm tra bị ảnh hưởng.
8. **Bàn giao:** README có setup/run/build; VERIFICATION.md có kết quả và giới hạn.
   Báo rõ phần đã triển khai, đã kiểm chứng và còn bị chặn. Chỉ publish, deploy
   hoặc ký/phát hành khi yêu cầu người dùng đã cho phép.

## Mẫu giao việc cho worker

```text
Mục tiêu và sản phẩm:
Vai trò:
Được sửa các đường dẫn:
Chỉ đọc các đường dẫn:
Contracts và dependency đã hoàn thành:
Tiêu chí nghiệm thu:
Lệnh kiểm chứng và môi trường:
Không sửa manifest/lockfile chung; gửi đề xuất cho root.
Trả về: thay đổi, commands + kết quả, integration notes và blockers.
Không tự tạo worker con trừ khi root yêu cầu.
```

## Khi không đủ môi trường

Tiếp tục phần độc lập có thể làm. Ghi chính xác tool, device, credential hoặc dịch
vụ thiếu; đưa bước tiếp theo để xác minh. Không chuyển check bị chặn thành N/A,
không giả lập kết quả build/device và không tự mua dịch vụ thay thế.
