# AI Software Factory

Bộ khung hướng dẫn và công cụ để agent xây dựng **web, mobile và desktop**.
Đây chưa phải ứng dụng và không phải dịch vụ tự chạy nhiều AI. Runtime Codex hoặc
VS Code/Copilot thực hiện việc gọi agent; các file vai trò quy định cách làm việc.

## Bắt đầu

Yêu cầu công cụ factory: **Python 3.11+**. Mỗi sản phẩm cài SDK và dependencies riêng.
Chạy từ thư mục gốc (máy dùng `python3` thì thay `python` bằng `python3`):

```powershell
python tools/factory.py doctor
python tools/factory.py init my-web --kind web
```

Lệnh `init` tạo brief, kiến trúc, hợp đồng API, kế hoạch, báo cáo kiểm chứng và
`factory.project.json`; không cài thư viện hay tạo code ứng dụng. Không ghi đè dự
án đã có. Các loại khác: `mobile`, `desktop`, `fullstack`. `fullstack` là web có
backend; nếu nhiều client, ghi rõ từng nền tảng trong brief.

Sau đó gửi agent yêu cầu, ví dụ:

> Hãy xây dựng website quản lý công việc trong projects/my-web. Đọc AGENTS.md,
> hoàn thiện brief và chọn stack phù hợp. Dùng subagent cho các phần độc lập,
> phân quyền file rõ ràng, tích hợp và kiểm thử luồng tạo/sửa/hoàn thành công việc.
> Ghi các lệnh thực tế vào factory.project.json và báo rõ phần chưa kiểm chứng.

Ví dụ cho app:

> Tạo app quản lý chi tiêu Android trong projects/expense-app. Dùng quy trình
> factory và các subagent phù hợp. Kiểm tra SDK sẵn có trước khi chọn stack;
> xác minh lưu dữ liệu, quyền truy cập và chạy trên thiết bị/emulator nếu có.

Nếu chỉ nói "app", agent cần xác định Android/iOS hay desktop trước khi chọn SDK.
Không ép mọi dự án dùng cùng framework; giữ stack hiện có khi sửa sản phẩm cũ.

## Dùng với Codex và VS Code

- **Codex:** mở thư mục gốc này. `AGENTS.md` là hướng dẫn chung;
  `.codex/agents/*.toml` là các vai trò dành cho Codex. Cấu hình dự án giới hạn
  ba worker đồng thời, không đổi model hoặc quyền của người dùng. Mức hỗ trợ phụ
  thuộc phiên bản/runtime. Nếu vai trò chưa xuất hiện, mở phiên mới; nếu host
  không hỗ trợ vai trò đặt tên, root truyền nội dung vai trò cho worker có sẵn.
- **VS Code/Copilot:** chọn `Software Factory Orchestrator` trong danh sách agent.
  Các vai trò chuyên môn ở `.github/agents/`. Khả năng gọi subagent và tool phụ
  thuộc harness đang chọn. Dùng Terminal → Run Task để chạy các task `Factory:`.
- Nếu mở riêng thư mục con làm repository độc lập, phải mang theo hướng dẫn và
  cấu hình agent cần dùng; không giả định runtime tìm thấy cấu hình của cha.
- Không có API key bắt buộc cho chính bộ factory. Tài khoản, quyền truy cập model
  và chi phí thuộc runtime bạn chọn. Chưa cấu hình gọi API/model tự động.

Nguồn chính thức: [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents).

## Vai trò và phối hợp

| Vai trò | Trách nhiệm |
| --- | --- |
| Orchestrator | Làm rõ yêu cầu, chia việc, quản lý file chung, tích hợp và nghiệm thu |
| Researcher / Architect | Đọc code, kiểm tra ràng buộc, đề xuất kiến trúc và contracts |
| Product Designer | Luồng người dùng, màn hình, trạng thái và khả năng tiếp cận |
| Frontend / Backend | Web UI, API, phân quyền và dữ liệu |
| Mobile / Desktop | Native integration, vòng đời ứng dụng và đóng gói theo nền tảng |
| Tester / Debugger | Kiểm thử có bằng chứng, tái hiện và sửa lỗi |
| Reviewer / Security | Đánh giá có dẫn chứng, không tự sửa code |

Không cần gọi đủ tất cả vai trò cho mỗi việc. Một file chỉ có một người sửa tại
một thời điểm; root quản lý manifest/lockfile. Xem [quy trình](docs/WORKFLOW.md).

Nguồn vai trò duy nhất để chỉnh là `.github/agents/*.agent.md`. Sau khi sửa:

```powershell
python tools/factory.py sync-agents
python tools/factory.py sync-agents --check
```

Các bản TOML được sinh và đưa vào Git để Codex đọc trực tiếp. Không chỉnh bản sinh.
Quy tắc read-only trong vai trò Codex là chỉ dẫn hành vi, không phải sandbox riêng.

## Cấu hình kiểm chứng cho từng sản phẩm

Manifest mới để mọi check là `null`, nghĩa là **chưa cấu hình**, không phải PASS.
Sau khi tạo code ứng dụng, thay bằng lệnh thực sự của sản phẩm, ví dụ một check:

```json
{
  "argv": ["npm.cmd", "run", "build"],
  "cwd": "apps/web",
  "timeout_seconds": 600
}
```

Trên macOS/Linux dùng `npm` thay `npm.cmd`. Đây chỉ là ví dụ: script `build` phải
tồn tại trong package.json. Lệnh Flutter, .NET, Cargo hoặc công cụ khác cũng dùng
mảng argv như trên. Không dùng chuỗi shell, `&&`, pipe hoặc dev server chạy vô hạn
làm check. `cwd` phải tồn tại trong thư mục sản phẩm.

```powershell
python tools/factory.py verify my-web
python tools/factory.py verify my-web --only build
python -m unittest discover -s tests -v
```

Các gate: `lint`, `typecheck`, `test`, `build`, `smoke`. Smoke phải kết thúc và kiểm
tra hành vi thật; với web có thể là test trình duyệt quản lý server bằng test
runner. App nhiều nền tảng cần script tổng hợp kiểm tra từng target và báo riêng
kết quả trong `docs/VERIFICATION.md`.

Chỉ dùng `{"not_applicable": "lý do kiến trúc cụ thể"}` khi một gate thực sự không
áp dụng. Không dùng N/A cho thiếu SDK, credentials, device hay test chưa viết.
Mã thoát: `0` các check đã chọn thành công/N/A có lý do; `1` có lệnh thất bại;
`2` chưa cấu hình, cấu hình lỗi hoặc bị chặn. Lệnh dừng khi một check fail/bị chặn;
các check phía sau chưa được chạy. `--only` chỉ xác nhận check được chọn.

Chỉ chạy manifest đáng tin cậy vì check chạy code của dự án. Tool không tự cài
dependencies, cấp secret, deploy, chạy agent hay khởi động server. Kết quả terminal
cần được ghi lại vào `docs/VERIFICATION.md` cùng bằng chứng kiểm tra thủ công.

## Giới hạn nền tảng

`doctor` xác nhận cấu hình factory và liệt kê executable trên PATH; nó không chứng
minh SDK, emulator, tài khoản hay signing đã sẵn sàng. Android cần toolchain và
thiết bị phù hợp; iOS native cần môi trường Apple phù hợp hoặc dịch vụ build được
cho phép. Desktop cần toolchain của framework và target OS. Build web không thay
thế kiểm tra thiết bị hoặc gói cài đặt native.

CI kiểm tra công cụ và đồng bộ vai trò trên Windows/Linux, không build các sản
phẩm tương lai. Mỗi sản phẩm phải bổ sung CI theo stack của nó.
