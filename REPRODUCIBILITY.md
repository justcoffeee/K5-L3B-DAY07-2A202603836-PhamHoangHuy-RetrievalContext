# Phụ thuộc và tái lập

## Kiểm tra bản nộp mà không gọi API

Python 3.11+ có thể đọc JSON, chạy tests offline và demo replay. Môi trường đã kiểm chứng là Windows/Python 3.14.8. Repo chứa corpus được phép chia sẻ, labels, source/index hashes, code snapshots và trace thật. Không có model weights, database volume, API key hoặc `.env` trong bài nộp.

```powershell
python -m unittest discover -s tests -v
python scripts/demo.py --case all
```

Các câu test đã được đánh giá và registry giữ một run chính thức. Kiểm tra lại bằng artifacts/replay không tạo benchmark mới. Không xóa registry, sửa gold hoặc chạy lại để chọn kết quả đẹp hơn. Lệnh thực tế của các thí nghiệm được ghi trong [RUN_STUDENT.md](RUN_STUDENT.md) và báo cáo; code snapshot đúng phiên bản của từng run nằm cùng kết quả.

## Runtime phụ thuộc Day06

Day07 tái sử dụng venv, model cache và schema/store của repo Day06 công khai ở commit:

`43b4a97419b7193c6b2306287a0833b7d5eb7922`

[Repo Day06](https://github.com/justcoffeee/K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion), [hướng dẫn setup Day06](https://github.com/justcoffeee/K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion/blob/43b4a97419b7193c6b2306287a0833b7d5eb7922/starter/README.md).

Đặt hai repo cạnh nhau. `requirements-lock.txt` trong Day07 là bản sao byte-for-byte của lock môi trường Day06 đã dùng, không phải danh sách package mới cài ở Day07. Các package chính: sentence-transformers 6.3.0, torch 2.15.0, transformers 5.23.0, psycopg/psycopg-binary 3.3.8, python-dotenv 1.2.4. Venv hiện tại ở root **Day06**, không ở starter/ hoặc Day07. Toàn bộ lock giữ các dependency bắc cầu để đối chiếu.

## Trên máy mới, tạo lại môi trường nguồn

Các lệnh dưới dành cho môi trường tái tạo mới; không được thực thi lại trong phiên chuẩn bị báo cáo này. Cần Git, Python tương thích lock (đã kiểm chứng 3.14.8), Docker Desktop/WSL2. Cài package/tải weights lần đầu cần mạng và dung lượng đĩa. Không có yêu cầu framework agent bổ sung.

Từ thư mục cha của hai repo:

```powershell
git clone https://github.com/justcoffeee/K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion
cd K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion
git checkout 43b4a97419b7193c6b2306287a0833b7d5eb7922
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
if (-not (Test-Path starter/.env)) { Copy-Item starter/.env.example starter/.env }
.\.venv\Scripts\python.exe scripts/check_embedding_setup.py --download
cd starter
docker compose -p day6_student_starter up -d --wait
..\.venv\Scripts\python.exe scripts/check_setup.py
```

Compose dùng PostgreSQL 16/pgvector 0.8.7, project day6_student_starter, database day6_lab, chỉ bind `127.0.0.1:55433`. Không đưa thông tin kết nối production vào template; không mở cổng public hoặc xóa volume để xử lý lỗi.

Trên **database mới**, từ starter/ Day06, nạp corpus/vector thật bằng pipeline đã có:

```powershell
..\.venv\Scripts\python.exe -u -m src.run --split dev
```

Pipeline tạo A/B/C; Day07 chỉ đọc `public.lab_chunks` strategy C. Corpus raw/processed và cấu hình đã có trong commit nguồn. Đây là tái tạo index trên dev Day06, không chạy test Day07. Trên máy hiện tại index đã sẵn sàng, không cần nạp lại hoặc rebuild để xem demo/kết quả.

E5 cố định revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, 384 chiều/CPU, normalize, query:/passage:. Cache được tải vào Day06/.cache/huggingface; inference sau đó offline. Embedding giả hoặc model khác sẽ không được dùng để thay kết quả. Khác nền tảng/numeric precision có thể làm fingerprint khác; không tắt guard để giả là cùng index. Muốn đo index mới phải ghi phiên bản và run riêng.

## Day07 thật

Từ root Day07, sao chép `.env.example` thành `.env` nếu chưa có; tự điền key DeepSeek locally. Không in hoặc commit key. Giữ endpoint/model/thinking đã duyệt. Script `scripts/prepare_day6_data.py --day6 PATH` có thể xuất lại corpus và kiểm tra store bằng môi trường Day06; lệnh sẽ cập nhật manifest xuất nên không dùng để thay artifacts đã freeze mà không ghi nhận.

Lệnh đã dùng cho dev (có phí API):

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy arrival
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_dev --methods dense --budget 2000 --context-policy latest
```

Lệnh test đã dùng là `-m src.run_test`; nó yêu cầu approval/runtime hashes, hai probe thành công và chỉ đăng ký một run. Repo đã có run hoàn tất nên lệnh mới bị chặn, không tự tạo phiên đánh giá độc lập thứ hai. Nếu muốn nghiên cứu thêm sau khi xem test, tạo holdout mới và ghi protocol mới. Các snapshot cũ lưu cả transport trước/sau sửa timeout, nên không coi lần chạy lại với code mới là chính xác cùng thí nghiệm cũ.

Các giới hạn tái lập: API trả alias model, không có checkpoint bất biến; network/cache/retry làm thay đổi latency; model rewrite có thể khác dù temperature=0. Các lệnh setup trên máy mới là quy trình tái tạo từ dependency nguồn, không phải tuyên bố đã cài thử trên máy thứ hai. Trong phiên này không cài thêm package hoặc gọi model thêm để chuẩn bị báo cáo/demo.
