# 🚀 Quick Start Guide

## Khởi động trong 5 phút!

### Bước 1: Cài đặt Python Dependencies (2 phút)

```powershell
# Server
cd server
pip install fastapi uvicorn python-multipart librosa numpy

# Desktop Client (nếu muốn test)
cd ..\desktop_client
pip install requests
```

### Bước 2: Tạo File Test (30 giây)

```powershell
cd ..
pip install scipy
python create_test_audio.py
```

Kết quả:
- ✅ `test_audio.wav` (5 giây)
- ✅ `test_60s.wav` (60 giây - cho performance test)

### Bước 3: Chạy Server (30 giây)

```powershell
cd server
python main.py
```

Mở browser: http://127.0.0.1:8000/docs

### Bước 4: Test với Desktop Client (1 phút)

```powershell
# Terminal mới
cd desktop_client
python desktop_app.py
```

1. Click "Choose Audio File"
2. Chọn `test_audio.wav`
3. Click "🔍 Analyze"
4. Xem kết quả!

---

## Test từng thành phần riêng lẻ

### Server Only

```powershell
# Test với curl
curl -X POST "http://127.0.0.1:8000/analyze/" `
  -F "file=@test_audio.wav"
```

### Desktop Client

```powershell
cd desktop_client
python desktop_app.py
```

### Android Client

1. Mở trong Android Studio: `android_client`
2. Sửa IP trong `ApiClient.kt`:
   ```kotlin
   // Emulator
   private const val BASE_URL = "http://10.0.2.2:8000/"
   
   // Hoặc Device (thay YOUR_IP)
   // private const val BASE_URL = "http://192.168.1.100:8000/"
   ```
3. Run (▶️)

**Lấy IP máy tính**:
```powershell
ipconfig
# Tìm "IPv4 Address" trong phần WiFi/Ethernet
```

### iOS Client

1. Mở trong Xcode: `ios_client/VoiceAnalysis.xcodeproj`
2. Sửa IP trong `VoiceAnalysisService.swift`:
   ```swift
   // Simulator
   private let baseURL = "http://127.0.0.1:8000"
   
   // Hoặc Device (thay YOUR_IP)
   // private let baseURL = "http://192.168.1.100:8000"
   ```
3. Run (⌘R)

**Lấy IP Mac**:
```bash
ifconfig | grep "inet "
```

---

## Troubleshooting Nhanh

### ❌ "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### ❌ "Cannot connect to server" (Desktop/iOS Simulator)
- Kiểm tra server đang chạy
- URL: `http://127.0.0.1:8000`

### ❌ "Unable to resolve host" (Android Emulator)
- URL phải là: `http://10.0.2.2:8000`

### ❌ "Connection refused" (Device thật)
1. Tìm IP máy tính/Mac
2. Cập nhật trong code client
3. Đảm bảo cùng WiFi
4. Tắt firewall (nếu cần)

---

## Next Steps

📖 Đọc thêm:
- [README.md](README.md) - Tài liệu đầy đủ
- [TESTING.md](TESTING.md) - Hướng dẫn test chi tiết
- [COMPLIANCE.md](COMPLIANCE.md) - Checklist tuân thủ

🎯 Phát triển thêm:
- Thêm tính năng ghi âm (F-C2)
- Vẽ biểu đồ (Charts)
- Export kết quả (CSV, JSON)
- Authentication (NF-2)

---

**Chúc bạn code vui! 🎉**
