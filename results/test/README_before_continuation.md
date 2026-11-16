# Kiểm tra trước test — chưa chạy test

Người dùng đã duyệt 85 nhãn dev AI-assisted và I1 (Dense, 2000 ký tự, arrival). Xác nhận được lưu tại `configs/dev_review_approval.json` và `configs/selected_for_test.json`.

Hai lần preflight không đạt điều kiện hai vòng tool protocol liên tiếp thành công. Các API request có lúc thành công, có lúc lỗi provider không trả mã HTTP; phép kiểm tra TLS trực tiếp cũng timeout. Chưa xác định nguyên nhân mạng/dịch vụ cụ thể; không có bằng chứng để kết luận key sai hoặc hết quota.

**Không có câu test nào được gửi model, không chấm gold test và chưa đăng ký held-out run.** Hai thư mục thời gian chỉ chứa code/approval snapshot, manifest preflight và log kết nối. Không có trace baseline/I1. Chi phí/usage probe được tổng hợp trong `preflight_summary.json`; request lỗi không có usage nên phí thực tế chưa xác nhận đầy đủ.

31 tests offline đạt. Agent/prompt/model/corpus/benchmark và cấu hình I1 không bị sửa sau khi duyệt. Không sửa proxy/DNS/Windows network.

Khi kết nối ổn định hơn, tiếp tục bằng môi trường Day06 từ thư mục repo Day07:

```powershell
& '..\K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion\.venv\Scripts\python.exe' -m src.run_test
```

Lệnh tiếp tục vẫn phải vượt preflight. Không dùng --resume cho hai thư mục preflight này vì chưa có registry hoặc câu test dang dở. Không cần xin lại phê duyệt cho đúng cấu hình/phạm vi đã được duyệt. Chưa commit hoặc push.
