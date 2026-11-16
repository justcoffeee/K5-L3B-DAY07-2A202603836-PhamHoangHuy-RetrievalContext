# Báo cáo Day07 — Agentic RAG trên Python Tutorial

**Học viên:** Phạm Hoàng Huy · **Mã:** 2A202603836 · **Lớp:** K5-L3B · **Ngày hoàn thiện:** 16/11/2026.

Bài thực hiện phần cơ bản của lab. Cấu hình chọn trên dev là Dense + context 2.000 ký tự + arrival order. Nhãn test đã được học viên xem và xác nhận sau khi chạy; không chỉnh model/prompt/cấu hình hoặc gold theo kết quả test. Điểm câu trả lời bên dưới không phải điểm chấm toàn bài.

## 1. Dữ liệu, quyền sử dụng và benchmark

Nguồn là **The Python Tutorial 3.14.10**, chương 3–8, của Python Software Foundation và các tác giả đóng góp. Có 6 chương HTML, 54 đơn vị nguồn chuẩn hóa, 139.067 ký tự và 411 retrieval chunks của strategy C Day06. Không gọi 54 đơn vị nguồn là 54 trang PDF: trường page giữ ID như python-3.14-ch04-u002. Chunk giữ source URL, document/source ID, chương, phiên bản, ngôn ngữ, section và char offsets. Toàn bộ text chunk đã đối chiếu với offset trong nguồn.

Giấy phép PSF License Version 2; ví dụ mã còn có Zero-Clause BSD theo thông báo gốc. Bản license/copyright, nguồn và manifest được giữ trong [data/day6](../../data/day6/README.md). Không có dữ liệu mật. Corpus và code phụ thuộc ở [repo Day06](https://github.com/justcoffeee/K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion), commit `43b4a97419b7193c6b2306287a0833b7d5eb7922`.

Embedding: `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, CPU, 384 chiều, normalized, tối đa 512 token, prefix query: / passage:. Không random vectors, truncate ngầm hoặc tải model ngầm. Store là PostgreSQL 16 + pgvector 0.8.7, bảng public.lab_chunks, index C; exact cosine SQL, không ANN. B/C Day06 có cùng nội dung/vector; Day07 không tự áp chapter filter. Fingerprint vector store được giữ nguyên trước/sau chạy.

Agent dùng DeepSeek API trực tiếp, `deepseek-flash`, thinking disabled, temperature 0, output tối đa 640 token/call. API chỉ trả alias model, không trả checkpoint bất biến. Môi trường đã chạy: Windows, Python 3.14.8, Docker Desktop/WSL2; package lock tại [requirements-lock.txt](../../requirements-lock.txt), sử dụng venv và cache Day06. Không cài framework agent mới.

| Split | Có đáp án | Thiếu evidence | Tổng |
|---|---:|---:|---:|
| Dev | 15 | 2 | 17 |
| Test | 5 | 2 | 7 |
| Tổng | 20 | 4 | 24 |

Câu hỏi tiếng Việt, tài liệu tiếng Anh. Câu có đáp án giữ expected answer, source/page/evidence và chunk ID. Các gold entries là bằng chứng thay thế, không phải multi-hop AND; benchmark hiện không có câu multi-hop. Câu thiếu evidence gần chủ đề Python; đã quét toàn bộ 54 đơn vị nguồn, đọc các mục/đoạn có từ khóa và ghi absence audit, không dựa vào top-k miss. Ví dụ database.sqlite chỉ là tên file trong ví dụ ngoại lệ, không phải hướng dẫn PRAGMA.

[Benchmark](../../benchmark/README.md) đã chia/freeze trước inference. Test mới so với Day06, không phải diễn đạt lại test cũ để chỉnh cấu hình. Người soạn đã đọc gold để gán nhãn; không tuyên bố holdout được một bên độc lập giữ kín. Agent chỉ nhận query-only, không nhận expected_answer, gold, answerable hoặc absence_reason. Dev dùng cho thí nghiệm/chọn; gold test chỉ được runner nối để chấm sau khi cả baseline/I1 thực thi xong.

## 2. Retrieval, context và thí nghiệm

Ba phương pháp khác nhau: **Dense** E5/pgvector; **TF-IDF** cosine lexical, bỏ kết quả score 0; **Hybrid RRF** hợp hai ranking depth 20, k=60, tie-break chunk ID. Không coi thay đổi top-k/chunking là phương pháp retrieval mới. Không reranker model và không filter từ gold. Cùng corpus/labels/query gốc và top 3 cho mọi phương pháp.

Agent có thể viết query tiếng Anh trung thành với câu hỏi. Báo riêng ranking query gốc, first model search và evidence qua nhiều lượt; không đánh đồng việc rewrite với ranking query gốc. Context tích lũy bỏ trùng ID, không cắt nửa chunk; budget tính ký tự gồm header nguồn. Arrival giữ candidates đến trước; latest đưa ranking mới nhất lên đầu, giữ phần cũ dự phòng. Chỉ tool result mới nhất giữ context đầy đủ; các result trước được đánh dấu superseded. Token system/history/JSON wrapper vẫn có trong provider usage, không nằm trong budget text evidence.

| Cấu hình | Retrieval, budget/policy | Split | Hit@1 query gốc | Evidence Hit@3 query gốc | CER strict/pipeline | Median agent s/câu | Phí USD từ usage đã biết |
|---|---|---|---|---|---|---|---|
| Dense baseline | dense, 800 chars/arrival | dev | 7/15 (46.7%) | 11/15 (73.3%) | 13/15 (86.7%) | 3.432 | 0.004224–0.008449 |
| TF-IDF | tfidf, 800 chars/arrival | dev | 5/15 (33.3%) | 7/15 (46.7%) | 11/15 (73.3%) | 2.987 | 0.004258–0.008515 |
| Hybrid RRF | hybrid, 800 chars/arrival | dev | 6/15 (40.0%) | 10/15 (66.7%) | 12/15 (80.0%) | 3.026 | 0.003838–0.007676 |
| I1 — budget | dense, 2000 chars/arrival | dev | 7/15 (46.7%) | 11/15 (73.3%) | 14/15 (93.3%) | 3.363 | 0.004790–0.009580 |
| I2 — priority | dense, 2000 chars/latest | dev | 7/15 (46.7%) | 11/15 (73.3%) | 7/15 (46.7%) | 17.763 | 0.002810–0.005620 |
| I1 đã chọn | I1, 2000 chars/arrival | test | 3/5 (60.0%) | 4/5 (80.0%) | 4/5 (80.0%) | 5.067 | 0.002280–0.004560 |
| Dense baseline | baseline, 800 chars/arrival | test | 3/5 (60.0%) | 4/5 (80.0%) | 4/5 (80.0%) | 6.233 | 0.001774–0.003548 |

Tất cả top-k=3, filter=None, max 3 lượt tìm. Hit là source_id/page khớp và evidence nguyên văn nằm trong chunk. Mẫu số retrieval/context: 15 dev hoặc 5 test có đáp án, không gồm câu thiếu evidence. CER strict trong bảng dùng gold cố định và pipeline thành công; lỗi giữ trong mẫu số và nhận miss. Context có thể gom nhiều query nên CER có thể cao hơn Hit@3 query gốc. I2 có 10/15 context đã chuẩn bị đủ evidence theo đọc nguồn nhưng chỉ 7/15 pipeline thành công; không xem payload đã tạo là bằng chứng model đã nhận khi provider lỗi.

**Hai lỗi dev và giả thuyết:**

- D04 Dense baseline: chunk quy tắc innermost có trong top 3 và top 1 ở lượt sau, nhưng context 800 ký tự giữ đoạn loop-else cũ dài 496 ký tự; chunk đúng không lọt budget. Agent từ chối sai. I1 tăng budget lên 2.000, trả lời đúng có source.
- D07 Dense baseline: chunk singleton được tìm nhưng không vào context 785 ký tự, chỉ còn tuple tổng quát. Model từ chối kèm citations không rỗng, trái schema nên lỗi protocol. I1 nguyên bản gặp lỗi provider trước search; không loại lỗi đó khỏi mẫu số hoặc ghi đạt giả. I2 chuẩn bị được evidence singleton nhưng request sinh answer lỗi. Sau khi sửa transport, hai dev case D04/D07 đã được kiểm chứng riêng, không thay kết quả benchmark cũ.

I1 chỉ đổi budget 800→2.000; I2 giữ 2.000 và đổi cách ưu tiên candidates mới. I1 đạt 28/30 so với Dense baseline 26/30. I2 có 9 lỗi provider nên điểm thấp không chứng minh latest intrinsically kém hơn; kết quả bị nhiễu hạ tầng. Không chạy lại riêng câu lỗi để thay số gốc.

Quy tắc chọn ghi trước thí nghiệm: grounded points trên toàn bộ 15 câu (lỗi/false refusal=0), rồi valid abstention /2, ít lỗi, CER cao, ít token và arrival nếu vẫn hòa. I1 được chọn **trên dev**, rồi học viên duyệt trước test. [Kế hoạch và quy tắc](../../docs/superpowers/plans/2026-11-16-context-experiments.md), [so sánh dev](../../results/dev_review/context_experiments_20261116/README.md).

## 3. Agent và đánh giá nguồn

Tool thật `search_documents(query)` dùng retriever cấu hình; model quyết định query và tìm lại nếu thiếu evidence. Dừng ở answer JSON hợp lệ, explicit refusal hoặc tối đa 3 search/4 model turns; mỗi logical call có tối đa 2 retry phù hợp. Giới hạn này là thiết lập thí nghiệm, không phải quy định chung của lab. Unknown citation, JSON/schema sai, gọi tool quá giới hạn và provider/store failure giữ thành lỗi, không đổi thành từ chối đúng.

Citation phải có trong context và xuất hiện trong answer. Đây chỉ là kiểm tra cấu trúc; nhãn ngữ nghĩa đọc từng phần được gắn nguồn. Context 0=không hỗ trợ, 1=thiếu điều kiện/quan hệ/nguồn, 2=đủ. Answer 0=sai/thiếu evidence/false refusal/lỗi, 1=một phần, 2=đúng đủ và có nguồn. Valid refusal phải từ chối và không thêm khẳng định vô căn cứ.

| Cấu hình / split | Tool use thành công | Phân bố search calls | Answer 0/1/2; điểm và mean /2 trên mọi câu có đáp án | Citation đã đọc | Answer có citation | Valid abstention | False refusal / toàn bộ answerable |
|---|---|---|---|---|---|---|
| Dense baseline / dev | 16/16 | 2 lần: 13 câu, 3 lần: 4 câu | 2/0/13; 26/30; 1.733/2 | 15/15 | 13/13 | 2/2 | 1/15 |
| TF-IDF / dev | 15/15 | 2 lần: 11 câu, 3 lần: 6 câu | 4/0/11; 22/30; 1.467/2 | 12/12 | 11/11 | 2/2 | 2/15 |
| Hybrid RRF / dev | 14/14 | 2 lần: 12 câu, 3 lần: 5 câu | 3/0/12; 24/30; 1.600/2 | 13/13 | 12/12 | 2/2 | 0/15 |
| I1 — budget / dev | 16/16 | 0 lần: 1 câu, 2 lần: 14 câu, 3 lần: 2 câu | 1/0/14; 28/30; 1.867/2 | 18/18 | 14/14 | 2/2 | 0/15 |
| I2 — priority / dev | 8/8 | 0 lần: 5 câu, 2 lần: 11 câu, 3 lần: 1 câu | 8/0/7; 14/30; 0.933/2 | 9/9 | 7/7 | 1/2 | 0/15 |
| I1 đã chọn / test | 7/7 | 2 lần: 6 câu, 3 lần: 1 câu | 0/0/5; 10/10; 2.000/2 | 10/10 | 5/5 | 2/2 | 0/5 |
| Dense baseline / test | 7/7 | 2 lần: 5 câu, 3 lần: 2 câu | 0/1/4; 9/10; 1.800/2 | 5/6 | 5/5 | 1/2 | 0/5 |

Tool use loại lỗi và báo N thành công riêng theo rubric; grounded totals luôn giữ toàn bộ 15/5 câu để không tăng điểm bằng cách loại lỗi. Ví dụ I2 mean trên 7 câu thành công là 2/2 nhưng tổng thật chỉ 14/30 khi giữ 8 câu answerable lỗi. Citation tính ID duy nhất mỗi câu, không đếm lặp ID trong cùng answer. Dense D04 dev có inline citation ngoài mảng declared; đã gắn cờ và đọc riêng (15/15 observed so với 14/14 declared), không sửa trace gốc.

### Đọc từng câu test I1

| ID | Loại | Tool và kết quả/đáp án | Nhãn và lý do chính |
|---|---|---|---|
| T01 | Có đáp án | 2 search; triple quotes giữ newline; backslash cuối dòng bỏ newline đầu; 994429862692bd5708095b1fa49fd3f0 | answer=2, context=2 |
| T02 | Có đáp án | 2 search; dấu * ngay trước keyword-only đầu tiên; e5a6879e3f04a49ee60f47f27e202599, e0314b602ac6d5516855f20afe6c1d66, 152e1f92cf8f8f2c493ff147cb500c70 | answer=2, context=2 |
| T03 | Có đáp án | 2 search; del xóa index/slice, khác pop trả giá trị; e12d5e0b102af3fb583cc06e854db00b, e4976e7c8c03d1c6a37a18f46e14e9dd | answer=2, context=2 |
| T04 | Có đáp án | 2 search; with đóng file cả khi exception; nguồn thay thế chương 8; f75f860f3d3396f0a832c86aa44c9a01, af4e9b992542a8f255a34c2e182dc1f8, 52ea2a41af6c0b37599d089c0178c2c9 | answer=2, context=2 |
| T05 | Có đáp án | 2 search; raise ... from None tắt chaining; ff3919a7aecf66d4113ecfab1a1fe6b0 | answer=2, context=2 |
| T06 | Thiếu evidence | 2 search; từ chối SQLite PRAGMA/đơn vị, không đoán; không có citation | abstention_correct=True |
| T07 | Thiếu evidence | 3 search; từ chối TypeVar variance, không dùng kiến thức ngoài corpus; không có citation | abstention_correct=True |

Đã đọc đủ 5 câu có đáp án + 2 câu thiếu evidence cho **cả baseline và I1**. [Bản 14 câu cùng context/citation/lý do](../../results/test/20261116T034326996108Z/REVIEW.md). Hai khác biệt quan trọng:

- **Baseline T04:** source đầy đủ có ví dụ with nhưng text thực sự gửi chỉ nói After the statement, không có antecedent; câu còn lại là open() thường. Chấm answer/context=1 và citation không hỗ trợ đủ quan hệ with/exception. I1 có thêm f75 gắn with với file closing nên ghép evidence đủ, chấm 2. Không dùng phần nguồn không gửi model để bù context baseline.
- **Baseline T06:** có từ chối nhưng khẳng định sai cả corpus chỉ có lỗi/exception. Corpus thực tế gồm chương 3–8, nên observed refusal=true nhưng valid abstention=false. I1 mô tả đúng phạm vi và từ chối không đoán.

**Gold không thay đổi:** T04 thực tế dùng evidence chương 8, khác gold chương 7. Strict CER đều 4/5, dù context đọc ngữ nghĩa là baseline 4/5 đủ + 1/5 một phần và I1 5/5 đủ. Không bổ sung alternative sau test để tăng hit. Kết quả mới chỉ trên 7 câu, không bảo đảm generalization hoặc điểm toàn bài.

## 4. Lỗi provider, thời gian và chi phí

Chẩn đoán ngoài test tìm được URLError/TimeoutError, WinError 10060 trước HTTP status; client cũ chỉ retry HTTP. Trước khi bất kỳ câu test nào được thực thi, bổ sung retry socket timeout/reset trong giới hạn 2 retry, kiểm tra 33 tests và hai câu dev, giữ model/prompt/I1. Bản phê duyệt/code cũ được lưu, transport revision có hash và lý do trong selected_for_test.json. Hai cấu hình test dùng cùng transport mới; không quy toàn bộ thay đổi lỗi dev-vs-test cho context budget. Không thay proxy/DNS hoặc cho rằng Internet chung của học viên hỏng.

Test phục hồi 5 failed attempts (baseline 3, I1 2), 0 lỗi case cuối; mọi attempt vẫn có trong trace. Có 36 request attempts và 33.875 token đã biết. Phí usage đã biết khoảng $0.00405–$0.00811 cho test, không gồm probe/diagnostic và usage không biết của failed attempts. Retry có thể lặp request đã được provider xử lý nhưng mất response; không coi khoảng phí là giới hạn trên hoặc hóa đơn. Embedding/retrieval local không có phí API, chưa tính điện/máy.

Tổng các benchmark 5 cấu hình dev + 2 cấu hình test: 218 request attempts, 209.981 token đã biết, khoảng $0.02397–$0.04795 theo đơn giá peak/off-peak đã dùng khi đo; 15 requests lỗi không trả usage. Không gồm smoke/probe/diagnostic và hai câu dev validation. Model loading không nằm trong median từng case; query embeddings cache theo adapter. Thời gian có ảnh hưởng của mạng, retry, cache và model rewrite không hoàn toàn xác định; không tuyên bố benchmark phần cứng/latency nhân quả.

## 5. Tái lập, demo và provenance

- [Hướng dẫn chạy](../../RUN_STUDENT.md), [tái tạo Day06/phụ thuộc](../../REPRODUCIBILITY.md), [demo](../../DEMO.md). Replay đọc ba trace model thật, kiểm tra hash, không gọi API và không tạo benchmark mới.
- [Baseline 3 phương pháp](../../results/dev/20261116T024332489435Z/summary.json); [I1 dev](../../results/dev/20261116T030001129031Z/dense/summary.json); [I2 dev](../../results/dev/20261116T030303500415Z/dense/summary.json); [test](../../results/test/20261116T034326996108Z/README.md).
- Mỗi case giữ original top 3, query rewrite, tool arguments/results, context, answer/citations, status/error, latency và usage. Manifest giữ input/index/runtime hashes, code snapshot và approval snapshot; không có key trong đó.
- Chỉ có một run test được đăng ký. Runner chặn chạy lại; resume chỉ điền case thiếu, không thay lỗi. Không tối ưu trên test rồi công bố lại như holdout độc lập. Nếu cải tiến thêm cần holdout mới.

**Vai trò AI:** AI hỗ trợ code, soạn benchmark, phân tích và đề xuất 85 nhãn dev + 14 nhãn test sau đọc nguồn; học viên đã xem và xác nhận riêng từng giai đoạn. Xác nhận ở [dev_review_approval](../../configs/dev_review_approval.json) và [test_review_approval](../../configs/test_review_approval.json). Bản nhãn AI gốc giữ trường pending lúc soạn để không đổi hash; bản xác nhận riêng là trạng thái hiện hành. Không tuyên bố chấm blind bởi người độc lập. Học viên chịu trách nhiệm hiểu code, nguồn và kết luận.

## 6. Phần nâng cao và việc nộp

Không thực hiện thử thách tài liệu ít nhất 100 trang có bảng/ảnh/biểu đồ; không yêu cầu cộng 15 điểm bonus. Bài theo phạm vi cơ bản tối đa 85 điểm, không tự khẳng định được 85 hoặc 100 điểm.

Code/dữ liệu public có quyền chia sẻ; API key/.env/model cache không nộp. Repo Day06/Day07 đã kiểm tra public qua GitHub metadata. Bản hoàn thiện hiện là file local; commit/push và nộp link theo giảng viên là bước sau khi học viên kiểm tra bản đóng gói. Deadline và phương thức nộp theo thông báo lớp, không suy từ checkpoint gợi ý.
