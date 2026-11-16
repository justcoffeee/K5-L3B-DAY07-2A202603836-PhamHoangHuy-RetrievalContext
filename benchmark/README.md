# Benchmark Python Day07 — bước 2

Trạng thái: **người dùng đã xác nhận bước 2; đóng băng trước khi chạy dev**, ghi tại `manifest.json`. Toàn bộ câu hỏi, đáp án và đánh giá thiếu bằng chứng do AI hỗ trợ soạn. Đây không phải bộ nhãn do một người chấm độc lập giữ kín. Trường `human_review: pending` trong dữ liệu gốc lưu trạng thái lúc soạn; xác nhận sau đó được ghi riêng trong manifest để giữ nguyên hash bộ câu hỏi. Các kết quả đánh giá, nếu có, nằm ở `results/dev/`, không phải nhãn benchmark.

| Tập | Có đáp án | Thiếu bằng chứng | Tổng |
|---|---:|---:|---:|
| Dev (`D01`–`D17`) | 15 | 2 | 17 |
| Test (`T01`–`T07`) | 5 | 2 | 7 |

## Các tệp

- `dev.json`, `test.json`: câu hỏi cùng gold, đáp án, nguồn, đơn vị nguồn, chunk ID hoặc lý do thiếu bằng chứng. Dùng riêng cho đánh giá.
- `queries/dev.json`, `queries/test.json`: chỉ có `id`, `split`, `question`. Phần gọi agent chỉ được đọc tệp query tương ứng, không được đọc nhãn.
- `REVIEW.md`: bản dễ đọc để kiểm tra từng câu và bằng chứng.
- `absence_audit.json`: kết quả quét từ khóa trên toàn bộ 54 đơn vị nguồn, văn bản các đơn vị có từ khóa và các chunks thuộc mục liên quan, phục vụ xem lại 4 câu thiếu bằng chứng.
- `manifest.json`: SHA-256 corpus, index, bộ câu hỏi và query, quy tắc chia tập và mẫu số metric. Hash hiện ghi nhận bản nháp; chưa có kết quả đánh giá.

## Phạm vi và cách chấm

Corpus cố định là `data/day6/chunks.json`: 411 chunks từ 6 chương Python Tutorial 3.14.10. Câu hỏi tiếng Việt, tài liệu tiếng Anh. Không có filter dựa trên gold. Các câu có đáp án gồm tra cứu cú pháp, ví dụ, điều kiện và tình huống áp dụng; mỗi câu có thể trả lời bằng một chunk, không có câu multi-hop trong bản này. Dev bao phủ cả 6 chương.

`gold` là các bằng chứng thay thế hợp lệ. Cùng một đoạn bằng chứng có thể khớp nhiều chunks; không yêu cầu retrieval trả đúng riêng `chunk_id` ghi trong gold. Theo starter, hit yêu cầu đúng `source_id`, `page` và chứa nguyên văn evidence. `page` là ID đơn vị nguồn Day06, không phải số trang in. Khi chấm câu trả lời vẫn phải đọc ý nghĩa, điều kiện và nguồn; tìm thấy chuỗi hoặc citation ID chưa đủ chứng minh trả lời đúng.

Retrieval Hit@1/Hit@3 và Context Evidence Rate chỉ tính **15 câu dev hoặc 5 câu test có đáp án**. Abstention tính riêng 2 câu thiếu bằng chứng mỗi tập; từ chối câu có đáp án phải được báo riêng. Giữ các lỗi provider/store trong báo cáo, không chuyển thành từ chối đúng.

Starter `baseline.validate()` và CLI baseline hiện chỉ nhận câu có gold. Khi triển khai runner ở bước sau, cần tách các câu `answerable=true` cho retrieval metrics; agent vẫn chạy đủ 17/7 câu. Không sửa starter trong bước chuẩn bị benchmark này.

## Kiểm tra câu thiếu bằng chứng

Đã quét toàn bộ corpus và xem các mục liên quan, không dựa vào kết quả top-k. `dataclasses` có xuất hiện trong ví dụ match nhưng không có hướng dẫn `frozen=True`; `database.sqlite` là tên file trong ví dụ ngoại lệ, không phải tài liệu SQLite. Các đường dẫn/liên kết sang tài liệu ngoài không được coi là nội dung đã ingest. Kết luận thiếu bằng chứng chỉ áp dụng cho corpus cố định này và vẫn cần người dùng xem nhãn; không có nghĩa Python không hỗ trợ các tính năng đó.

Agent phải tìm tài liệu trước khi từ chối và nói rõ giới hạn bằng chứng, không bổ sung đáp án từ kiến thức bên ngoài. Không cần đoán một đáp án kỹ thuật cho các câu này.

## Quy trình dev/test

1. Người dùng kiểm tra bản nháp; sửa nhãn nếu cần trước khi đánh giá.
2. Đóng băng bộ câu hỏi/corpus bằng SHA-256 sau khi xác nhận. Chỉ dùng dev khi so sánh phương pháp, phân tích lỗi và thử cải tiến.
3. Công bố tiêu chí chọn và chốt cấu hình trên dev trước khi chạy test.
4. Chạy baseline và cấu hình chọn trên cùng 7 câu test; không dùng kết quả test để chỉnh rồi báo lại như holdout độc lập.

Năm câu test có đáp án là câu mới so với Day06: chuỗi nhiều dòng, keyword-only, del, with và tắt exception chaining. Việc người soạn đọc gold để xây nhãn là công việc tạo benchmark; chưa có đầu ra model/retrieval nào trên bộ mới được dùng để chọn cấu hình. Đây không phải bộ test do bên độc lập giữ kín. Nếu dùng test để tối ưu, phải tạo holdout mới.

Chưa kết nối model sinh câu trả lời, chưa gọi API và chưa phát sinh phí trong bước 2.
