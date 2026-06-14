# News Auto Update

- Chạy `python scripts/fetch_news.py` để cập nhật tin tức liên quan đến dưỡng lão.
- Để tự động chạy mỗi ngày lúc 5h sáng trên Windows, tạo lịch trình Task Scheduler bằng lệnh:

schtasks /Create /SC DAILY /ST 05:00 /TN "HiếuAn-News-Update" /TR "C:\\path\\to\\Website\\scripts\\schedule_news_update.bat" /F

Lưu ý: thay đường dẫn đúng với máy của bạn.
