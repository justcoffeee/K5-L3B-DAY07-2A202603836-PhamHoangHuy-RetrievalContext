> Trạng thái hiện hành: dữ liệu bước 1 đã được học viên duyệt, benchmark/dev/test đã hoàn tất. Nội dung bên dưới ghi lại việc chuẩn bị ban đầu; xem README root và các approval trong configs để theo dõi các giai đoạn sau. Manifest xuất được giữ nguyên cho provenance.

# Dữ liệu Day06 dùng cho Day07 — bước 1

Nguồn: The Python Tutorial 3.14.10, chương 3–8, Python Software Foundation và các tác giả đóng góp. Giữ bản quyền và giấy phép trong `license.html`, `copyright.html`; nguồn và quy trình trích xuất nằm trong `source_manifest.json`. Tài liệu dùng PSF License Version 2; ví dụ mã còn có Zero-Clause BSD theo thông báo gốc.

## Đã chuẩn bị

- `chunks.json`: 411 chunks từ strategy C đã được chọn trên dev Day06, định dạng Day07 (`id`, `source_id`, `source`, `page`, `text`, `metadata`). B/C có cùng nội dung index; C khác chính sách filter. Không tự áp filter vào mọi truy vấn Day07.
- `source_units.jsonl`: 54 đơn vị nguồn thuộc 6 chương, dùng đối chiếu bằng chứng và xem văn bản lân cận. `page` là ID đơn vị nguồn, không phải số trang in.
- `manifest.json`: thời điểm kiểm tra, phiên bản embedding, dấu vân tay index, SHA-256 các tệp, số lượng, và kết quả truy vấn smoke test.

Đã kiểm tra ID duy nhất, văn bản từng chunk khớp chính xác offset trong nguồn, toàn bộ vector có 384 chiều, hữu hạn và chuẩn hóa. Dấu vân tay index khớp lần chạy dev Day06 đã lưu. Đã dùng E5 local tạo một query vector và tìm top 3 thật trong PostgreSQL. Đây chỉ là kiểm tra kết nối, không phải benchmark hoặc điểm chất lượng.

Không xuất vector vào JSON. Dense retrieval sẽ dùng lại kho PostgreSQL Day06 `public.lab_chunks`, strategy C, exact cosine. Chưa triển khai adapter agent Day07. Không thay đổi dữ liệu trong database, không tạo embedding lại cho corpus và không gọi API trả phí.

## Tái tạo

Chạy tại thư mục repo Day07 bằng PowerShell, sau khi Docker Desktop và container PostgreSQL Day06 đã hoạt động:

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' scripts\prepare_day6_data.py --day6 '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion'
```

Script dùng môi trường, model cache offline và `starter/.env` của Day06; không ghi thông tin kết nối ra kết quả. Script cần repo Day06 ở commit tương thích và snapshot dev `20261114T035115831944Z`. Chưa cài môi trường riêng cho Day07. Lệnh chạy lại sẽ cập nhật các tệp xuất và thời điểm trong manifest.

## Chờ duyệt trước bước tiếp theo

Chưa tạo benchmark Day07, chưa chạy dev/test và chưa kết nối model sinh câu trả lời. Test Day06 đã được xem/phân tích; nên chuẩn bị tập test mới khi xây benchmark Day07. Cần chọn model agent trước khi thiết lập phần gọi model.
