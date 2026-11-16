# Kết quả đọc/chấm dev và hai cấu hình cải tiến

**Trạng thái: AI-assisted, chờ người dùng xác nhận nhãn và cấu hình đề xuất. Chưa chạy test.**

Người dùng đã duyệt kết quả dev ban đầu. Bước này bổ sung 51 đánh giá nguồn/đáp án cho ba phương pháp ban đầu và chạy thêm 34 lượt agent thật (2 × 17 câu). Không dùng model làm judge; nhãn do Codex đọc câu trả lời, context và nguồn để đề xuất. Đây không phải đánh giá độc lập của con người.

| Cấu hình | Điểm grounded answer trên toàn bộ 15 câu /30 | Từ chối đúng /2 | Evidence đủ trong context đã chuẩn bị /15 | Lỗi thực thi |
|---|---:|---:|---:|---:|
| Dense 800 / arrival | 26/30 | 2/2 | 13/15 | 1 (protocol) |
| TF-IDF 800 / arrival | 22/30 | 2/2 | 11/15 | 2 (protocol) |
| Hybrid 800 / arrival | 24/30 | 2/2 | 12/15 | 3 (protocol) |
| Dense 2000 / arrival | 28/30 | 2/2 | 14/15 | 1 (provider) |
| Dense 2000 / latest | 14/30 | 1/2 | 10/15 | 9 (provider) |

Điểm 0/1/2 chỉ dành cho mức đúng và được nguồn hỗ trợ, không phải điểm chấm toàn bài lab. Lỗi và từ chối sai trên câu có đáp án nhận 0 trong mẫu số đủ 15 câu. Các aggregate chỉ trên câu chạy thành công được giữ riêng trong JSON; không dùng mean 2/2 trên ít câu thành công để thay điểm toàn bộ.

## Kết luận và đề xuất

**Đề xuất I1: Dense, budget 2000 ký tự, arrival order**, giữ DeepSeek Flash/thinking disabled/temperature 0, top 3 và tối đa 3 lượt tìm. Đã chọn theo quy tắc ghi trước thí nghiệm trong `docs/superpowers/plans/2026-11-16-context-experiments.md`: grounded points trên toàn bộ câu, abstention, lỗi, context, token. Cấu hình ở `configs/dev_selected_candidate.json` vẫn là candidate chờ duyệt, chưa cho phép chạy test.

I1 tăng từ 26/30 lên 28/30 trong lần đo này. D04 đã trả lời đúng với citation quy tắc innermost. D07 của I1 lỗi provider trước khi agent tìm tài liệu, nên không được tính đạt hoặc loại khỏi mẫu số.

I2 đã chuẩn bị đúng evidence cho D04, D07, D09 ở các lượt có retrieval, nhưng nhiều request sinh câu trả lời lỗi. Không thể quy kết điểm 14/30 là do latest policy kém: thí nghiệm bị nhiễu bởi 9 lỗi provider. Chưa có bằng chứng đáng tin để chọn latest thay arrival. Không chạy lại riêng các câu lỗi để thay kết quả ban đầu.

## Hai lỗi dev làm cơ sở cải tiến

1. **D04, baseline Dense:** chunk đúng `6f16320109f4a36189eb5033ecbb89b2` có trong top 3 và lần tìm sau top 1. Context 800 ký tự giữ đoạn loop-else ban đầu, không chứa quy tắc innermost; agent từ chối sai. **Giả thuyết:** budget nhỏ và ưu tiên kết quả cũ làm mất evidence. **I1:** context đủ và đáp án đúng 2/2.

2. **D07, baseline Dense:** chunk singleton `a14a0c62dbc9ade9275bb1cfd18bbc57` được tìm nhưng không vào context; chỉ có tuple tổng quát, chấm context mức 1. Phản hồi từ chối có citation bị lỗi giao thức. **I1:** provider lỗi trước search, chưa kiểm chứng được đáp án. **I2:** evidence singleton đã vào context chuẩn bị, nhưng request sinh đáp án lỗi nên answer vẫn 0. Điều này minh họa cần tách retrieval, context và generation.

## Citation và context

Đã đọc từng citation và ghi lý do trong `citation_reviews`. Mỗi ID duy nhất trong một câu là một đơn vị citation, không đếm lặp lại cùng ID trong cùng câu. Các kết quả accepted đều có nguồn hỗ trợ phần được gắn citation; điều đó không làm một false refusal thành câu trả lời đúng.

Dense D04 baseline có ID trong văn bản từ chối nhưng không nằm trong mảng citations. Trường hợp này được gắn cờ `unlisted_inline_citations`, tính riêng trong metric citation quan sát, không sửa trace gốc. Các citation trong raw output bị từ chối vì lỗi giao thức cũng còn trong trace nhưng không được tính là câu trả lời thành công.

Bảng trên đánh giá **context đã chuẩn bị**. Với I2, 10/15 context có đủ evidence, nhưng chỉ 7/15 kết thúc pipeline thành công. Ba trường hợp D04/D07/D09 có evidence nhưng provider lỗi sau khi tạo payload; không xác nhận model đã nhận context. Các file summary ban đầu dùng định nghĩa pipeline thành công và giữ nguyên số 7/15; comparison JSON báo cả hai để tránh đánh đồng.

## Chi phí và độ tin cậy

I1: 35 request, 40.291 token đã biết; I2: 30 request, 23.215 token đã biết. Phí từ token đã biết của hai lần mới ước tính **$0.00760–$0.01520**. Có tổng 10 request lỗi không trả usage, nên đây không phải giới hạn trên của tổng hóa đơn. Không có phí gọi model để judge.

API liệt kê model xác thực đã trả HTTP 200 khi kiểm tra, nên key vẫn dùng được. Lỗi chat provider không có mã HTTP; telemetry chỉ phân loại transport/response, chưa xác định nguyên nhân cụ thể. Trước khi đánh giá test cần kiểm tra chat/tool endpoint ổn định. Không kết luận đây là hết quota hay lỗi model từ dữ liệu hiện có.

Mỗi cấu hình chỉ chạy một lần; query model viết lại có thể khác dù temperature 0. Model provider trả alias deepseek-flash, không cung cấp checkpoint bất biến. Kết quả chỉ là dev trên corpus Python nhỏ này, không bảo đảm chất lượng tổng quát.

## Kiểm tra và tái tạo

- `comparison.json`: tổng hợp, denominator, lỗi, chi phí và xếp hạng candidate.
- `REVIEW.md`: toàn bộ 85 câu/đầu ra/context/nhãn/lý do để người dùng xem.
- Từng thư mục run giữ `reviews_ai_assisted.json`, `semantic_summary_ai_assisted.json`; trace gốc và mẫu review trống được giữ nguyên.
- Mã nguồn, input và dependency hashes có trong manifest/snapshot từng run.
- 29 tests offline đạt; không cài thêm thư viện và không thay đổi corpus/index.

Chạy lại hai cấu hình từ repo Day07 bằng môi trường Day06 (có phí API):

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy arrival
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy latest
```

## Chờ duyệt

Người dùng xác nhận các nhãn AI-assisted và candidate I1 trước khi chốt cấu hình/chạy test. Hiện chưa chạy test, chưa hoàn tất báo cáo cá nhân/demo, chưa commit hoặc push.
