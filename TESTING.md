# Hướng dẫn Test Hệ thống

## Chuẩn bị File Test

Bạn cần file âm thanh test. Có thể:

### Option 1: Tải file mẫu từ internet

```powershell
# Tải file test từ freesound.org hoặc tự ghi âm
```

### Option 2: Tạo file test với Python

```python
import numpy as np
from scipy.io import wavfile

# Tạo file âm thanh test đơn giản
duration = 3  # giây
sample_rate = 16000

# Tạo tín hiệu sin (voiced)
t = np.linspace(0, duration, int(sample_rate * duration))
frequency = 440  # Hz (note A4)
audio = np.sin(2 * np.pi * frequency * t)

# Thêm silence
silence = np.zeros(int(sample_rate * 1))
audio = np.concatenate([silence, audio, silence])

# Normalize
audio = np.int16(audio * 32767)

# Lưu file
wavfile.write('test_audio.wav', sample_rate, audio)
print("✅ Đã tạo test_audio.wav")
```

## Test Plan

### 1. Test Server

```powershell
# Terminal 1: Chạy server
cd server
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Kiểm tra:
- ✅ Server chạy thành công
- ✅ Truy cập http://127.0.0.1:8000 thấy welcome message
- ✅ Truy cập http://127.0.0.1:8000/docs thấy Swagger UI

Test API với curl:

```powershell
# Test 1: Health check
curl http://127.0.0.1:8000/health/

# Test 2: Upload file
curl -X POST "http://127.0.0.1:8000/analyze/" `
  -F "file=@test_audio.wav"

# Kết quả mong đợi: JSON với filename, total_segments, segments
```

### 2. Test Desktop Client

```powershell
# Terminal 2: Chạy desktop app
cd desktop_client
pip install -r requirements.txt
python desktop_app.py
```

Test Cases:

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC-D1 | Launch app | ✅ App opens, shows "No file selected" |
| TC-D2 | Click "Choose Audio File" | ✅ File picker opens |
| TC-D3 | Select test_audio.wav | ✅ Filename displayed, Analyze enabled |
| TC-D4 | Click "Analyze" | ✅ Shows "Đang xử lý...", button disabled |
| TC-D5 | Wait for response | ✅ Results displayed with statistics |
| TC-D6 | Wrong file format | ✅ Error "Unsupported format" |
| TC-D7 | Server not running | ✅ Error "Cannot connect" |

### 3. Test Android Client

Chuẩn bị:
1. Mở project trong Android Studio
2. Chọn emulator hoặc device
3. Sửa IP trong `ApiClient.kt`:
   - Emulator: `http://10.0.2.2:8000/`
   - Device: `http://YOUR_PC_IP:8000/`

Test Cases:

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC-A1 | Launch app | ✅ App opens, "Sẵn sàng" status |
| TC-A2 | Click "Choose Audio File" | ✅ File picker opens |
| TC-A3 | Select audio file | ✅ Filename displayed |
| TC-A4 | Click "Analyze" | ✅ Progress bar shows, "Đang phân tích..." |
| TC-A5 | Wait for response | ✅ Results displayed in TextView |
| TC-A6 | Wrong server IP | ✅ Alert "Không thể kết nối" |
| TC-A7 | Rotate device | ✅ State preserved (ViewModel) |

### 4. Test iOS Client

Chuẩn bị:
1. Mở project trong Xcode
2. Chọn simulator hoặc device
3. Sửa IP trong `VoiceAnalysisService.swift`:
   - Simulator: `http://127.0.0.1:8000`
   - Device: `http://YOUR_MAC_IP:8000`

Test Cases:

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC-I1 | Launch app | ✅ App opens, "Sẵn sàng" status |
| TC-I2 | Click "Choose Audio File" | ✅ Document picker opens |
| TC-I3 | Select audio file | ✅ Filename displayed |
| TC-I4 | Click "Analyze" | ✅ Loading indicator, button disabled |
| TC-I5 | Wait for response | ✅ Results displayed |
| TC-I6 | Wrong server IP | ✅ Alert with error message |
| TC-I7 | Background/foreground | ✅ State preserved |

## Test Results Template

### Desktop Client Test Report

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-D1 | ⬜ Pass / ⬜ Fail | |
| TC-D2 | ⬜ Pass / ⬜ Fail | |
| TC-D3 | ⬜ Pass / ⬜ Fail | |
| TC-D4 | ⬜ Pass / ⬜ Fail | |
| TC-D5 | ⬜ Pass / ⬜ Fail | |
| TC-D6 | ⬜ Pass / ⬜ Fail | |
| TC-D7 | ⬜ Pass / ⬜ Fail | |

### Android Client Test Report

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-A1 | ⬜ Pass / ⬜ Fail | |
| TC-A2 | ⬜ Pass / ⬜ Fail | |
| TC-A3 | ⬜ Pass / ⬜ Fail | |
| TC-A4 | ⬜ Pass / ⬜ Fail | |
| TC-A5 | ⬜ Pass / ⬜ Fail | |
| TC-A6 | ⬜ Pass / ⬜ Fail | |
| TC-A7 | ⬜ Pass / ⬜ Fail | |

### iOS Client Test Report

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-I1 | ⬜ Pass / ⬜ Fail | |
| TC-I2 | ⬜ Pass / ⬜ Fail | |
| TC-I3 | ⬜ Pass / ⬜ Fail | |
| TC-I4 | ⬜ Pass / ⬜ Fail | |
| TC-I5 | ⬜ Pass / ⬜ Fail | |
| TC-I6 | ⬜ Pass / ⬜ Fail | |
| TC-I7 | ⬜ Pass / ⬜ Fail | |

## Performance Test

Test NF-1: Xử lý file 1 phút < 15 giây

```powershell
# Tạo file âm thanh 1 phút
python -c "
import numpy as np
from scipy.io import wavfile
sr = 16000
duration = 60
audio = np.random.randn(sr * duration) * 0.3
audio = np.int16(audio * 32767)
wavfile.write('test_60s.wav', sr, audio)
"

# Test với curl và đo thời gian
Measure-Command {
  curl -X POST "http://127.0.0.1:8000/analyze/" `
    -F "file=@test_60s.wav" -o result.json
}

# Kết quả mong đợi: TotalSeconds < 15
```

## Common Issues & Solutions

### Issue 1: Server không chạy được
```
ModuleNotFoundError: No module named 'librosa'
```

**Solution**:
```powershell
pip install librosa soundfile
```

### Issue 2: Desktop - "Cannot connect"
```
ConnectionError: [Errno 10061] No connection
```

**Solution**:
- Kiểm tra server đang chạy
- Kiểm tra `Config.API_BASE_URL` đúng

### Issue 3: Android - "Unable to resolve host"
```
UnknownHostException: Unable to resolve host
```

**Solution**:
- Emulator: Dùng `10.0.2.2` thay vì `127.0.0.1`
- Device: Dùng IP máy tính (tìm bằng `ipconfig`)
- Kiểm tra cả device và PC cùng WiFi

### Issue 4: iOS - "The resource could not be loaded"
```
NSURLErrorDomain Code=-1004
```

**Solution**:
- Kiểm tra `Info.plist` có `NSAppTransportSecurity`
- Simulator: Có thể dùng `localhost`
- Device: Dùng IP Mac (tìm bằng `ifconfig`)

### Issue 5: Librosa lỗi với MP3
```
RuntimeError: Audioread not installed
```

**Solution**:
```powershell
pip install audioread
# Hoặc install ffmpeg:
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
```

## Automated Testing (Optional)

### Server API Test với pytest

```python
# test_api.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_endpoint():
    with open("test_audio.wav", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/analyze/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert "total_segments" in data
    assert "segments" in data
    assert len(data["segments"]) > 0

# Chạy: pytest test_api.py
```

## Sign-off

Sau khi test xong tất cả, điền thông tin:

- **Tester**: ___________________
- **Date**: ___________________
- **Overall Status**: ⬜ PASS / ⬜ FAIL
- **Notes**: 
  - Server: _________________
  - Desktop: _________________
  - Android: _________________
  - iOS: _________________
