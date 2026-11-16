# Chạy bản triển khai Day07

## Phạm vi hiện tại

Ba phương pháp dùng chung corpus 411 chunks đã đóng băng: dense exact cosine trong pgvector với E5 local, TF-IDF và Hybrid RRF (k=60, depth=20 mỗi nhánh). Model agent: `deepseek-flash`, thinking disabled, temperature 0. Starter được giữ nguyên.

`src.run_dev` chỉ chạy **dev**. Runner riêng `src.run_test` chỉ đánh giá baseline/I1 đã được người dùng duyệt và đóng băng. Người dùng đã xác nhận benchmark bước 2 trước dev, sau đó xác nhận nhãn AI-assisted và I1 trước test. Các xác nhận nằm trong `configs/dev_review_approval.json` và `configs/selected_for_test.json`; nhãn gốc được giữ nguyên để bảo toàn provenance.

## Điều kiện chạy

- Repo Day06 nằm cạnh repo này, giữ nguyên model cache, `.venv`, `starter/.env` và kho vector. Phiên bản thư viện được khóa trong `requirements-lock.txt` của Day06. Không cần cài thêm package cho bản triển khai hiện tại.
- Docker Desktop chạy, container `day6_student_starter-postgres-1` healthy, cổng PostgreSQL local `55433`.
- Điền `API_KEY` vào `.env` của Day07. Endpoint `https://api.deepseek.com`, model `deepseek-flash`, `API_THINKING=disabled`. Không commit `.env`.
- Model embedding chỉ được load offline, không tải ngầm. Index C phải khớp fingerprint Day06. Không tạo schema, ghi lại corpus hoặc re-embed tài liệu.

## Lệnh PowerShell

Chạy tại thư mục repo Day07:

```powershell
# Nếu container chưa chạy:
docker start day6_student_starter-postgres-1

# Tests và replay offline, không gọi API:
python -m unittest discover -s tests -v
python scripts/demo.py

# Chạy thật toàn bộ dev; lệnh này phát sinh phí token DeepSeek:
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev
```

Mỗi lần chạy mới tạo một thư mục thời gian riêng trong `results/dev/`. `results/dev/LATEST.txt` chỉ tới lần gần nhất chạy xong. Nếu gián đoạn, dùng đúng đường dẫn in ở đầu log:

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --resume 'results\dev\TEN_THU_MUC_DA_CHAY'
```

Resume giữ nguyên các câu đã lưu (kể cả lỗi), chỉ chạy câu còn thiếu; yêu cầu code, cấu hình và input hashes không đổi. Không coi chạy lại một lỗi là kết quả ban đầu. Có thể dùng `--methods dense`, `--methods tfidf` hoặc `--methods hybrid` cho một lần chạy mới; không đổi danh sách methods khi resume.

## Cấu hình trước cải tiến

Mỗi phương pháp có tối đa 3 lượt tìm, mỗi lượt top 3. Context tích lũy loại trùng ID, giữ ưu tiên kết quả đến trước, không cắt nửa chunk, budget **800 ký tự bao gồm header nguồn**. JSON wrapper, danh sách ID, system prompt và lịch sử giao thức không nằm trong budget văn bản bằng chứng; toàn bộ token API vẫn được ghi theo usage của provider. Chỉ tool result mới nhất chứa toàn bộ context; tool results trước được thay bằng dấu superseded để không nhân budget qua nhiều lượt.

Agent có thể viết lại query sang tiếng Anh phù hợp corpus. Ranking của câu hỏi gốc tiếng Việt được đo riêng bằng cùng câu hỏi/cutoff ở cả ba phương pháp. Ranking query đầu tiên do model tạo và evidence qua các lượt tìm được báo riêng, không đánh đồng với ranking query gốc.

## Tệp kết quả

- `manifest.json`: cấu hình, code/input hashes, thời gian, trạng thái, split và đánh dấu test đã/chưa đánh giá theo từng run.
- `code_snapshot/`: mã nguồn đã dùng để chạy, gồm baseline và runtime Day06; không chứa `.env`. Lần dev đầu tiên có snapshot tương ứng hashes cũ. Các run sau có kiểm tra hash dependencies khi resume và giữ usage khi response thiếu choices. Transport/socket retry revision được ghi riêng trước test; xem approval snapshot của đúng run.
- `{method}/Dxx.json`: ranking query gốc, tool calls/arguments/results, context cuối, answer/citations, trạng thái, thời gian, các request/response model và usage. Không lưu Authorization headers hoặc key.
- `{method}/traces.json`: tổng hợp các trace, dùng xem lại và chấm.
- `{method}/summary.json` và `summary.json`: metric evidence tự động, phân bố trạng thái/tool calls, lỗi, token và ước tính khoảng phí.
- `{method}/reviews.json`: mẫu nhãn **để trống**, chưa phải điểm chất lượng.

Hit@1/Hit@3 và Context Evidence Rate dùng mẫu số 15 câu có đáp án, lỗi vẫn tính là miss. Citation ID hợp lệ chưa chứng minh citation hỗ trợ câu trả lời. Cần đọc từng câu để chấm grounded answer 0–2, context 0–2, từng citation và từ chối đúng. Không tự động coi hai câu thiếu bằng chứng là được từ chối đúng chỉ dựa vào status. Lỗi provider/retrieval/protocol được báo riêng.

Model transport timeout 45 giây, tối đa 2 retry cho 429/5xx và lỗi socket timeout/reset tạm thời; Retry-After lớn hơn 10 giây sẽ báo lỗi thay vì chờ dài. Lỗi permission/certificate hoặc JSON response không hợp lệ không được retry. Mỗi lần thất bại vẫn được log riêng; usage không được provider trả ghi là chưa biết. Retry có thể dẫn tới request đã xử lý nhưng mất response, nên phí thực tế có thể cao hơn ước tính từ usage đã biết. Bản sửa socket retry được kiểm chứng trên dev và đóng băng trước test, giữ nguyên model/prompt/I1; các run dev ban đầu vẫn giữ transport cũ.

Model load không tính vào latency từng câu. Query embedding được cache theo adapter trong một lần chạy; Hybrid có cache riêng. Thời gian là phép đo thực tế trong môi trường local, không phải benchmark phần cứng được kiểm soát.

## Các thí nghiệm dev đã hoàn tất

Đã đọc/chấm AI-assisted 85 đầu ra dev và thử hai cấu hình context. Xem `results/dev_review/context_experiments_20261116/README.md` và `REVIEW.md`. I1 Dense + 2000 ký tự + arrival order đã được học viên duyệt trước test. Bản candidate ban đầu được giữ nguyên; trạng thái xác nhận nằm trong `configs/dev_review_approval.json` và `configs/selected_for_test.json`. Sau sửa retry socket trước test, cả baseline/I1 đã chạy xong held-out.

Các tùy chọn mới (vẫn chỉ dev, mỗi lệnh chạy mới có phí API):

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy arrival
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy latest
```

Defaults vẫn là 800 ký tự/arrival. Latest đưa ranking của lần tìm mới lên trước và giữ candidates cũ làm dự phòng, không dùng gold. Cấu hình/nhãn dev đã được duyệt trước khi chạy test. Báo cáo cá nhân và demo replay nằm trong bản nộp hiện tại.

## Đánh giá test đã được duyệt

Người dùng đã duyệt I1: Dense, 2000 ký tự, arrival order. `src.run_test` kiểm tra SHA-256 cấu hình/runtime/benchmark và yêu cầu hai vòng tool protocol thành công liên tiếp bằng câu thử ngoài benchmark trước khi đọc query test. Nó chạy baseline Dense 800 và I1 Dense 2000 trên cùng bảy query, chỉ đọc gold sau khi cả hai cấu hình chạy xong. Không sửa agent/prompt theo test.

```powershell
# Lệnh đã dùng; hiện bị chặn vì đã có run test hoàn tất. Không cần chạy lại để xem kết quả.
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_test
```

Kết quả nằm trong `results/test/<timestamp>/`, gồm manifest/code snapshot/approval snapshot, tất cả probe, từng trace baseline/I1, summaries và mẫu review. `results/test/registry.json` chỉ tới run đã đăng ký. Nếu gián đoạn, `--resume 'results\test\<timestamp>'` chỉ thực hiện câu còn thiếu; không thay câu đã lỗi, không chạy lại run hoàn tất. Nếu preflight không đạt thì không chạy thêm câu test. Kiểm tra preflight không thể bảo đảm tất cả request sau đó thành công; lỗi vẫn được báo nguyên trạng.

Nhãn test AI-assisted được ghi riêng và học viên đã xác nhận sau khi đọc kết quả. Xác nhận dev không thay cho test: hai artifact riêng là `configs/dev_review_approval.json` và `configs/test_review_approval.json`. Các review JSON gốc giữ trạng thái lúc soạn để bảo toàn hash; approval là trạng thái hiện hành.

Test đã chạy đủ trong `results/test/20261116T034326996108Z`; xem README/REVIEW trong thư mục đó. Nhãn AI-assisted đề xuất: baseline 9/10, I1 10/10 trên 5 câu có đáp án; valid abstention lần lượt 1/2 và 2/2. Strict frozen-gold evidence metric giữ nguyên 4/5, không sửa nhãn sau khi thấy nguồn thay thế ở T04. Năm socket timeouts đã được retry, không có case cuối bị lỗi. Các nhãn test đã được học viên xác nhận riêng; không chạy lại test để tìm kết quả tốt hơn. Báo cáo: `report/individual/2A202603836_PhamHoangHuy.md`; demo: `DEMO.md`; kiểm tra nộp: `SUBMISSION_CHECKLIST.md`.
