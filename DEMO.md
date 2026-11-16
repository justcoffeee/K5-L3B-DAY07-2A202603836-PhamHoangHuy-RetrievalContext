# Demo Day07 — trace model thật, chế độ replay

Demo phát lại đầu ra đã đo, **không gọi model mới, không giả lập agent và không tạo điểm benchmark mới**. Mỗi trace được kiểm tra SHA-256 qua nhãn AI-assisted đã được học viên xác nhận. Chạy được với Python stdlib, không cần key, Docker, E5 hoặc mạng.

Chạy tại root repo:

```powershell
python scripts/demo.py
```

## Kịch bản 3–5 phút

1. Giới thiệu corpus Python Tutorial, 411 chunks, E5/pgvector, DeepSeek Flash. Nêu ba phương pháp đã so sánh và lý do chọn I1 trên dev.
2. Chạy câu có bằng chứng:

   ```powershell
   python scripts/demo.py --case answer
   ```

   Đây là I1/T02 từ test thật. Theo tool calls tới context và câu trả lời: dấu `*` đứng ngay trước keyword-only parameter đầu tiên. Chỉ ra citation ID có trong context và đoạn text hỗ trợ, không chỉ kiểm tra hình thức ID.

3. Chạy câu thiếu bằng chứng:

   ```powershell
   python scripts/demo.py --case abstain
   ```

   Đây là I1/T06: hỏi SQLite PRAGMA busy_timeout. Retrieval đã chạy, nhưng corpus chỉ có tên file database.sqlite trong ví dụ ngoại lệ, không có cấu hình SQLite. Agent từ chối, không điền lệnh/đơn vị bằng kiến thức ngoài tài liệu. Lý do corpus thiếu evidence còn có benchmark absence audit; không suy từ top-k miss.

4. Chạy trường hợp lỗi thật trước đây:

   ```powershell
   python scripts/demo.py --case error
   ```

   Đây là Dense dev/D07 trước cải tiến. Context thiếu đoạn singleton vì budget 800; model từ chối nhưng trả mảng citations không rỗng, trái schema. Trace giữ `status=error`, stage protocol và raw output bị từ chối. Không đổi lỗi thành từ chối đúng, không giả vờ lỗi này vừa xảy ra trong test.

5. Mở [báo cáo cá nhân](report/individual/2A202603836_PhamHoangHuy.md) và [test review](results/test/20261116T034326996108Z/REVIEW.md). Giải thích baseline T04 thiếu antecedent của with và T06 nói quá phạm vi corpus; strict gold vẫn giữ nguyên. Không tuyên bố đạt 100 điểm toàn bài.

## Artifact demo

```powershell
python scripts/demo.py --case all --export demo/replay.json
```

[demo/replay.json](demo/replay.json) là ba bản phát lại kèm provenance, không phải một lần inference. Script không in key hoặc đọc `.env`. Nếu sửa trace/nhãn mà không có xác nhận tương ứng, script dừng thay vì hiển thị kết quả như đã được xác nhận.

Demo live nếu giảng viên yêu cầu sẽ phát sinh phí và cần môi trường thật. Bản chuẩn bị hiện tại là replay có thể kiểm chứng; không chạy lại tập test hoặc thay kết quả để quay video đẹp hơn. Nếu lớp yêu cầu video/link demo thì học viên cần quay/gửi theo thông báo lớp; chưa có video được tạo trong phiên này.
