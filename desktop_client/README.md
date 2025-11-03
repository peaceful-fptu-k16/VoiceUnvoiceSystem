# Voice Analysis Desktop Client

Ứng dụng Desktop (Python/Tkinter) cho hệ thống phân tích Voiced/Unvoiced/Silence.

**✨ Tính năng mới: Ghi âm trực tiếp từ microphone!**

## Cài đặt

### 1. Cài đặt Python (3.8 trở lên)

### 2. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

**Lưu ý**: PyAudio yêu cầu:
- **Windows**: Có thể cần cài đặt từ wheel file nếu gặp lỗi
  ```powershell
  pip install pipwin
  pipwin install pyaudio
  ```
- **macOS**: 
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- **Linux**: 
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  pip install pyaudio
  ```

## Chạy Ứng dụng

### Development

```powershell
python desktop_app.py
```

## Đóng gói thành Executable (S-D3)

### Windows (.exe)

```powershell
# Cài đặt PyInstaller
pip install pyinstaller

# Đóng gói
pyinstaller --onefile --windowed --name="VoiceAnalysis" desktop_app.py
```

File .exe sẽ nằm trong thư mục `dist/`.

### macOS (.app)

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Đóng gói
pyinstaller --onefile --windowed --name="VoiceAnalysis" desktop_app.py
```

## Hướng dẫn Sử dụng (NF-3: Dưới 10 giây)

### Phương án 1: Chọn file có sẵn
1. **Chọn file**: Click nút "📂 Choose Audio File"
2. **Phân tích**: Click nút "🔍 Analyze"
3. **Xem kết quả**: Kết quả hiển thị trong vùng "Analysis Results"

### Phương án 2: Ghi âm trực tiếp (F-C2) ✨
1. **Bắt đầu ghi**: Click nút "🎤 Start Recording"
2. **Nói vào microphone**: Ứng dụng sẽ ghi âm (hiển thị thời gian)
3. **Dừng ghi**: Click nút "⏹️ Stop Recording"
4. **Phân tích**: Click nút "🔍 Analyze"
5. **Xem kết quả**: Kết quả hiển thị ngay lập tức

## Cấu hình Server (S-5)

Địa chỉ server được cấu hình trong class `Config`:

```python
class Config:
    API_BASE_URL = "http://127.0.0.1:8000"
```

Để thay đổi địa chỉ server, sửa biến `API_BASE_URL`.

## Tuân thủ Tiêu chuẩn

### Client General (S-1 đến S-5)
- ✅ S-1: Gọi API trên background thread (`threading.Thread`)
- ✅ S-2: Error handling với try-catch
- ✅ S-3: UI Feedback rõ ràng (Loading, Success, Error)
- ✅ S-4: Sử dụng class `AnalysisResponse` để parse JSON
- ✅ S-5: Server URL trong biến config

### Desktop Specific (S-D1 đến S-D3)
- ✅ S-D1: Sử dụng `threading.Thread` cho API calls
- ✅ S-D2: Sử dụng `root.after(0, ...)` để cập nhật UI an toàn
- ✅ S-D3: Hỗ trợ đóng gói với PyInstaller

### Functional Requirements (F-C1 đến F-C9)
- ✅ F-C1: Chọn file từ bộ nhớ
- ✅ F-C2: Ghi âm trực tiếp từ microphone ✨ NEW!
- ✅ F-C3: Hiển thị tên file đã chọn
- ✅ F-C4: Nút "Analyze"
- ✅ F-C5: Gửi file đến API
- ✅ F-C6: Hiển thị "Đang xử lý..." và vô hiệu hóa nút
- ✅ F-C7: Parse JSON response theo hợp đồng
- ✅ F-C8: Hiển thị kết quả với thống kê
- ✅ F-C9: Xử lý và hiển thị lỗi rõ ràng

## Troubleshooting

### Không kết nối được server

Đảm bảo:
1. Server đã chạy: `python ../server/main.py`
2. Địa chỉ server đúng trong `Config.API_BASE_URL`
3. Firewall không chặn port 8000

### Lỗi PyAudio / Microphone

**"No Default Input Device"**:
- Kiểm tra microphone đã được kết nối và bật
- Kiểm tra quyền microphone trong Windows Settings

**Lỗi cài đặt PyAudio trên Windows**:
```powershell
# Sử dụng pipwin
pip install pipwin
pipwin install pyaudio

# Hoặc tải wheel file từ:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio‑0.2.13‑cp39‑cp39‑win_amd64.whl
```

**macOS**: Cần cài portaudio trước
```bash
brew install portaudio
pip install pyaudio
```

### Lỗi khi đóng gói

Nếu gặp lỗi với PyInstaller, thử:
```powershell
pyinstaller --onefile --windowed --hidden-import=tkinter --hidden-import=pyaudio desktop_app.py
```
