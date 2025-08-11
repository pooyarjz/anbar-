
# راه‌اندازی سریع ویندوز (وقتی اپ بالا نمی‌آید)
1) روی فایل زیر راست‌کلیک > Run as administrator:
   - `installer/windows/diagnose_and_fix.ps1`
   این اسکریپت: Python را بررسی/نصب می‌کند، venv می‌سازد، وابستگی‌ها را نصب می‌کند، migrate می‌زند، پورت 8000 را چک می‌کند و سرور را بالا می‌آورد.
2) اگر خطا دیدید، اجرا کنید:
   - `installer/windows/start_app_console.bat`
   و محتوای فایل `logs/server.err.log` یا `logs/server_console.log` را برای من بفرستید.
3) برای شروع/توقف آسان:
   - Start: `installer/windows/start_app.bat`
   - Stop : `installer/windows/stop_app.bat`
