# Kết quả held-out: baseline và I1

**Đã chạy đủ 14 lượt test. Học viên đã xem và xác nhận 14 nhãn AI-assisted.** Xem `configs/test_review_approval.json` ở root repo. Các JSON review giữ trạng thái lúc soạn để bảo toàn hash; không phải chấm blind bởi người độc lập.

Baseline và I1 được chốt trước test. Cả hai dùng DeepSeek Flash, E5/pgvector/corpus đã đóng băng, cùng 7 query (5 có đáp án, 2 thiếu evidence). Baseline budget 800 và I1 budget 2000 ký tự, cùng arrival policy. Không sửa cấu hình theo kết quả test.

| Cấu hình | Grounded answer /10 | Từ chối đúng /2 | Citation hỗ trợ /tổng | Lỗi case |
|---|---:|---:|---:|---:|
| baseline | 9/10 | 1/2 | 5/6 | 0 |
| I1 | 10/10 | 2/2 | 10/10 | 0 |

Grounded answer là 0/1/2 cho 5 câu có đáp án, không phải điểm toàn bài lab. Mọi câu đã được đọc cùng context và citation; không chấm đúng chỉ vì có ID hợp lệ. Model trả lời cả 5 câu và từ chối cả 2 câu ở mỗi cấu hình, nhưng đúng về nội dung là đánh giá riêng.

## Retrieval và context

Query gốc: cả hai Hit@1 **3/5**, Evidence Hit@3 **4/5**. Strict frozen-gold Context Evidence Rate đều **4/5**. Đây là kết quả máy theo source/page/evidence nguyên văn, giữ nguyên gold trước test.

Đánh giá ngữ nghĩa context: baseline có 4 câu mức 2 và 1 câu mức 1; I1 có 5 câu mức 2. T04 dùng nguồn chương 8 khác gold chương 7, nên không tự thêm alternative vào gold sau test.

## Hai khác biệt cần người dùng đọc

**T04 — với with/exception:** baseline chỉ gửi đoạn af4 có câu After the statement... file always closed, nhưng thiếu đoạn trước xác định statement là with. Chunk còn lại chỉ có open() thường. Đáp án đúng theo tài liệu đầy đủ nhưng context/citation chưa thiết lập đủ quan hệ with và ngoại lệ; chấm bảo thủ answer=1, context=1, citation chưa hỗ trợ đủ. I1 còn có đoạn f75 liên hệ with với đóng file và tài nguyên, nên có thể kết hợp với af4; answer/context=2. Nguồn đầy đủ xác nhận antecedent, nhưng văn bản không gửi model không được dùng để bù cho context baseline.

**T06 — từ chối nhưng nói quá phạm vi:** baseline không đoán SQLite, nhưng nói cả corpus chỉ chứa tutorial về lỗi/exception. Corpus thật có chương 3–8. Vì rubric yêu cầu từ chối mà không thêm khẳng định vô căn cứ, lưu refusal_observed=true nhưng abstention_correct=false. I1 mô tả đúng corpus là Python Tutorial và không bịa lệnh/đơn vị; chấm đúng. Cùng quy tắc đã dùng trên dev: mô tả context được phép; suy rộng sai ra toàn corpus không được tính đạt.

## Sửa lỗi kết nối trước khi chạy test

Các lần preflight ban đầu không đạt. Chẩn đoán ngoài benchmark tìm được URLError do TimeoutError, WinError/errno 10060; client cũ chỉ retry HTTP nên dừng ngay. Bổ sung retry socket tạm thời trong cùng giới hạn tối đa 2 retry (3 attempts), không retry permission/certificate/response JSON hỏng. Mỗi lỗi vẫn có record riêng, không có thông tin key.

Bản sửa qua 33 tests và hai query dev D04/D07 trước test; cả hai trả lời có nguồn. Approval v1 được giữ ở configs/selected_for_test_transport_v1.json; bản execution freeze ghi rõ transport_revision và source hashes. Model/prompt/retrieval/I1 không đổi, chưa có query test nào thực thi khi sửa/freeze. Baseline và I1 test đều dùng cùng transport mới. Không so sánh lỗi mạng dev-vs-test như bằng chứng chỉ riêng budget tốt hơn.

Trong lần test: baseline phục hồi 3 lần timeout, I1 phục hồi 2 lần; cả 14 case hoàn tất, 0 lỗi case cuối. Năm failed attempts không trả usage, vẫn có trong trace. Không thay/re-run riêng một câu test đã lỗi; chỉ có một run test được đăng ký.

## Chi phí và giới hạn

Các case test dùng **33.875 token đã biết**, 36 request attempts tính cả retry. Phí theo usage đã biết ước tính **$0.00405–$0.00811**, không phải hóa đơn hoặc giới hạn trên của tổng phí; chưa gồm phần usage không biết từ 5 failed attempts và các probe/diagnostic ngoài benchmark. Các probe được lưu riêng trong preflight history.

Kết quả chỉ có 5 câu trả lời được/2 câu thiếu evidence, một lần chạy mỗi cấu hình. Nhãn do AI hỗ trợ và đã có đọc chéo bằng AI, không phải chấm độc lập của con người. Alias model không cung cấp checkpoint bất biến. Học viên đã xác nhận các nhãn mới trước khi hoàn thiện bản nộp.

## Tệp để kiểm tra

- comparison_ai_assisted.json: tổng hợp nhãn và giới hạn.
- REVIEW.md: đầy đủ 14 đầu ra/context/citation/nhãn/lý do.
- baseline/I1: từng trace T01–T07, traces.json, summary.json, reviews_ai_assisted.json và semantic_summary_ai_assisted.json. Các summary máy và mẫu review trống được giữ nguyên.
- manifest.json, code_snapshot, approval_snapshot.json: cấu hình và mã thực tế đã dùng.

## Tiếp theo

Học viên đã xác nhận 14 nhãn AI-assisted. Báo cáo cá nhân, demo replay có nguồn/từ chối/lỗi và checklist nộp đã được chuẩn bị; xem README root. Không chỉnh pipeline trên test rồi báo lại như holdout độc lập; nếu muốn tối ưu thêm phải lập holdout mới. Chưa commit hoặc push.
