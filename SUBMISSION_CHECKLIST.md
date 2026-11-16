# Kiểm tra bản nộp cá nhân Day07

Đối chiếu với [SUBMISSION.md](SUBMISSION.md), [BENCHMARK.md](BENCHMARK.md) và [RUBRIC.md](RUBRIC.md). Đánh dấu dựa trên artifacts thực tế, không tự chấm điểm toàn bài.

- [x] Đúng thông tin Phạm Hoàng Huy — 2A202603836 — K5-L3B và repo cá nhân đúng tên.
- [x] Code agent thật, DeepSeek Flash và tool retrieval; Dense/TF-IDF/Hybrid RRF, không dùng mock làm benchmark.
- [x] Corpus Python hợp lệ: nguồn/license, 54 source units/411 chunks, E5 384d và pgvector Day06; có cách kết nối/tái tạo và dependency lock.
- [x] Benchmark 24 câu: dev 15+2, test 5+2, query-only tách gold, absence audit và frozen hashes.
- [x] Ba phương pháp trên dev, hai cấu hình cải tiến, giả thuyết/hai lỗi dev, chọn I1 trên dev trước test.
- [x] Top-3, tool arguments/results, context, answer/citations, lỗi, latency và token/cost được lưu theo query.
- [x] Baseline/I1 trên cùng 7 câu test; đọc đủ 5 answerable+2 insufficient mỗi cấu hình; không sửa gold theo test.
- [x] 85 nhãn dev + 14 nhãn test AI-assisted đã được học viên xác nhận bằng artifact riêng. Không tuyên bố chấm blind bởi người độc lập.
- [x] [Báo cáo cá nhân](report/individual/2A202603836_PhamHoangHuy.md) đã điền kết quả thật, denominator, chi phí chưa biết, lỗi và giới hạn.
- [x] [Demo replay](DEMO.md) đủ có nguồn/từ chối/lỗi từ trace model thật, không cần key hoặc thêm API calls.
- [x] Tests offline, demo và kiểm tra hash/key được dùng để xác minh; runtime đã chạy test được giữ nguyên.
- [x] Repo Day06 và Day07 public (kiểm tra metadata GitHub ngày 16/11/2026), thuận tiện cấp quyền xem. Nội dung hoàn thiện mới hiện vẫn local.
- [x] `.env` được Git bỏ qua; không đưa key/cache/model weights/database volume vào bài nộp.
- [ ] Commit và push bản hoàn thiện sau khi học viên kiểm tra/yêu cầu. Chưa thực hiện trong bước này.
- [ ] Nộp link repo theo kênh/deadline giảng viên thông báo; không có công cụ nào đã gửi bài thay học viên.
- [ ] Nếu giảng viên yêu cầu video/link demo: học viên cần quay/gửi theo thông báo. Hiện có kịch bản và demo replay, chưa có video.

Phần nâng cao 100 trang đa phương thức **không thực hiện**; không yêu cầu cộng bonus 15 điểm. Để mẫu tài liệu gốc của đề nguyên trạng không có nghĩa báo cáo cá nhân còn thiếu: bản chính là file mang MSSV/họ tên ở trên.
