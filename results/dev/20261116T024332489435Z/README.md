# Kết quả dev trước cải tiến

Run: `20261116T024332489435Z`. Đã chạy thật 51 lượt agent bằng DeepSeek Flash, chưa chạy test.

| Phương pháp | Hit@1 query gốc | Hit@3 query gốc | Evidence trong context cuối | Answered / abstain / lỗi |
|---|---:|---:|---:|---:|
| dense | 7/15 | 11/15 | 13/15 | 13 / 3 / 1 |
| tfidf | 5/15 | 7/15 | 11/15 | 11 / 4 / 2 |
| hybrid | 6/15 | 10/15 | 12/15 | 12 / 2 / 3 |

Tổng: 117 requests, 112,600 tokens. Phí token ước tính $0.01232–$0.02464; không phải số tiền xác nhận từ hóa đơn.

Mẫu số retrieval/context là 15 câu có đáp án. Các chỉ số hit dựa trên gold literal đã đóng băng. Answered chỉ có nghĩa vượt kiểm tra giao thức/citation ID, chưa phải câu trả lời đúng. Grounded answer, hỗ trợ citation và abstention correctness chưa chấm; xem `reviews.json` của từng phương pháp.

## Lỗi dev đã đối chiếu trace

1. **Dense D04 — evidence bị loại ở bước chọn context.** Câu hỏi break trong vòng lặp lồng nhau. Chunk đúng `6f16320109f4a36189eb5033ecbb89b2` nằm ở top 3 lần đầu và top 1 lần sau, nhưng context chỉ giữ chunk else-clause ban đầu dài 496 ký tự; thêm chunk đúng sẽ vượt 800 ký tự. Agent từ chối. Đây là false refusal trên câu có đáp án, không phải corpus thiếu dữ liệu.

2. **Dense D07 — evidence đúng bị giữ ngoài context, sau đó lỗi hợp đồng đầu ra.** Chunk tuple một phần tử `a14a0c62dbc9ade9275bb1cfd18bbc57` đã được tìm ở lần đầu/lần sau nhưng không được pack vào context 785 ký tự. Model trả `abstain=true` kèm danh sách citation không rỗng nên bị ghi lỗi giao thức. Không phải key/quota lỗi.

3. **TF-IDF D06/D09/D10 và Hybrid D04/D06/D09 — cùng nguy cơ ưu tiên kết quả cũ.** Các lượt tìm tiếp theo đã có chunk chứa gold nhưng context tích lũy vẫn ưu tiên nội dung đến trước. Riêng Hybrid D06, query do model tạo còn bỏ mất ký hiệu `**` trong câu hỏi, cho thấy cần giữ nguyên token cú pháp khi viết lại query.

Tất cả 6 lỗi trong run này là lỗi protocol: model từ chối nhưng trả citation array không rỗng, trái hợp đồng hiện tại. Không có lỗi HTTP/store trong 117 request đã ghi. D16/D17 đều có status abstain ở cả ba phương pháp; việc từ chối có hợp lý về nội dung vẫn cần đọc và chấm riêng.

## Đề xuất cho bước cải tiến — chưa thực hiện

- Cấu hình 1: tăng context budget từ 800 lên 2000 ký tự, giữ phương pháp/prompt/số lượt tìm để đo ảnh hưởng riêng của budget.

- Cấu hình 2: với cùng budget đã chọn, thử cách hợp nhất/xếp lại candidates để lượt tìm mới có thể đưa evidence tốt hơn vào context, thay vì bị kết quả đầu chặn. Giữ query gốc và trace rewrite để phân biệt thay đổi ở retrieval với context.

- Tách rõ schema từ chối có nguồn và schema trả lời; nếu cho phép citation trong từ chối thì vẫn phải kiểm tra ID và ý nghĩa. Không đổi lại kết quả cũ hoặc tự biến các lỗi này thành từ chối đúng.

Chưa chốt cấu hình thắng: Dense đang dẫn về query-gốc Hit@3 và final-context evidence, nhưng cần xem chất lượng câu trả lời và các thí nghiệm cải tiến trước khi chọn.

## Tái lập và giới hạn

Mã thực tế của run được lưu trong `code_snapshot/`; các src hashes khớp manifest. Dependencies được snapshot trong lúc chạy. Sau khi chạy xong đã sửa hai vấn đề kiểm toán: giữ usage khi provider trả JSON thiếu choices và hash cả baseline/runtime Day06 khi resume. Bản sửa chỉ kiểm tra offline, không phát sinh lượt API lại và không thay đổi kết quả ở đây.

Xem `REVIEW.md` để đọc từng câu, context, câu trả lời và phản hồi thô ở các lỗi. Chưa commit hoặc push.
