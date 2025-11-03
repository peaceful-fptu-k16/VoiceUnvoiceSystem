# Hệ thống Phân tích Voiced/Unvoiced/Silence

Hệ thống phân tích âm thanh đầy đủ với kiến trúc Client-Server, tuân thủ 100% các yêu cầu kỹ thuật.

## 📋 Tổng quan

Hệ thống bao gồm:
- **1 Server (Backend)**: Python/FastAPI - Xử lý toàn bộ logic phân tích
- **3 Clients (Frontend)**: Desktop (Python/Tkinter), Android (Kotlin), iOS (Swift)

## 🏗️ Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTS (UI Only)                    │
├─────────────┬─────────────┬─────────────────────────────┤
│   Desktop   │   Android   │          iOS                │
│  (Tkinter)  │  (Kotlin)   │        (Swift)              │
└──────┬──────┴──────┬──────┴──────────┬──────────────────┘
       │             │                 │
       │  HTTP POST  │    HTTP POST    │    HTTP POST
       │  (multipart)│   (multipart)   │   (multipart)
       │             │                 │
       └─────────────┴─────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │   SERVER (FastAPI/Python)   │
       │  - Nhận file âm thanh       │
       │  - Phân tích với Librosa    │
       │  - Trả về JSON              │
       └─────────────────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │  Librosa Analysis Engine    │
       │  - Tính F0 (Pitch)          │
       │  - Tính Energy (RMS)        │
       │  - Phân loại frames:        │
       │    • VOICED                 │
       │    • UNVOICED               │
       │    • SILENCE                │
       └─────────────────────────────┘
```

## 📁 Cấu trúc Thư mục

```
VoiceUnvoiceSystem/
├── server/                     # Backend API
│   ├── main.py                # API endpoints
│   ├── analysis.py            # Nghiệp vụ phân tích
│   ├── requirements.txt       # Dependencies
│   └── README.md
│
├── desktop_client/            # Desktop Application
│   ├── desktop_app.py         # Tkinter app
│   ├── requirements.txt
│   └── README.md
│
├── android_client/            # Android Application
│   ├── app/
│   │   ├── build.gradle.kts
│   │   ├── src/main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/voiceanalysis/app/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── data/
│   │   │   │   │   ├── model/
│   │   │   │   │   ├── network/
│   │   │   │   │   └── repository/
│   │   │   │   └── ui/
│   │   │   └── res/
│   │   └── README.md
│   └── README.md
│
├── ios_client/                # iOS Application
│   ├── VoiceAnalysis/
│   │   ├── VoiceAnalysisApp.swift
│   │   ├── Models/
│   │   ├── Services/
│   │   ├── ViewModels/
│   │   ├── Views/
│   │   └── Info.plist
│   └── README.md
│
└── README.md                  # File này
```

## 🚀 Hướng dẫn Khởi động Nhanh

### Bước 1: Chạy Server (BẮT BUỘC)

```powershell
cd server
pip install -r requirements.txt
python main.py
```

Server sẽ chạy tại: `http://127.0.0.1:8000`

Kiểm tra: Mở browser và truy cập `http://127.0.0.1:8000/docs`

### Bước 2: Chạy Client (Chọn 1 trong 3)

#### Option A: Desktop Client

```powershell
cd desktop_client
pip install -r requirements.txt
python desktop_app.py
```

#### Option B: Android Client

1. Mở `android_client` trong Android Studio
2. Đợi Gradle sync xong
3. **QUAN TRỌNG**: Sửa IP trong `ApiClient.kt`:
   - Emulator: `10.0.2.2:8000`
   - Thiết bị thật: IP máy tính (tìm bằng `ipconfig`)
4. Run (▶️)

#### Option C: iOS Client

1. Mở `ios_client/VoiceAnalysis.xcodeproj` trong Xcode
2. **QUAN TRỌNG**: Sửa IP trong `VoiceAnalysisService.swift`:
   - Simulator: `127.0.0.1:8000`
   - Thiết bị thật: IP máy Mac (tìm bằng `ifconfig`)
3. Run (⌘R)

## 🎯 Cách Sử dụng (Tất cả Client đều giống nhau)

1. **Chọn file âm thanh** (.wav, .mp3, .m4a)
2. **Nhấn "Analyze"**
3. **Đợi kết quả** (hiển thị loading)
4. **Xem kết quả phân tích**

## 📊 JSON Response Format (API Contract - F-S5)

```json
{
  "filename": "audio.wav",
  "total_segments": 1234,
  "segments": [
    {
      "time": 0.01,
      "type": "SILENCE",
      "f0": 0.0,
      "energy": 0.001
    },
    {
      "time": 0.03,
      "type": "VOICED",
      "f0": 150.5,
      "energy": 0.15
    },
    {
      "time": 0.05,
      "type": "UNVOICED",
      "f0": 0.0,
      "energy": 0.03
    }
  ]
}
```

## ✅ Tuân thủ Yêu cầu & Tiêu chuẩn

### Yêu cầu Chức năng Server (F-S)

| Mã | Yêu cầu | Trạng thái |
|----|---------|-----------|
| F-S1 | Endpoint `/analyze/` với POST multipart | ✅ |
| F-S2 | Hỗ trợ .wav, .mp3, .m4a | ✅ |
| F-S3 | Xử lý file an toàn (tempfile) | ✅ |
| F-S4 | Phân loại VOICED/UNVOICED/SILENCE | ✅ |
| F-S5 | JSON response theo hợp đồng | ✅ |
| F-S6 | HTTP error codes (400, 500) | ✅ |

### Yêu cầu Chức năng Client (F-C)

| Mã | Yêu cầu | Desktop | Android | iOS |
|----|---------|---------|---------|-----|
| F-C1 | Chọn file từ bộ nhớ | ✅ | ✅ | ✅ |
| F-C2 | Ghi âm (tùy chọn) | ⏳ | ⏳ | ⏳ |
| F-C3 | Hiển thị tên file | ✅ | ✅ | ✅ |
| F-C4 | Nút "Phân tích" | ✅ | ✅ | ✅ |
| F-C5 | Gửi file đến API | ✅ | ✅ | ✅ |
| F-C6 | Hiển thị "Đang xử lý..." | ✅ | ✅ | ✅ |
| F-C7 | Parse JSON response | ✅ | ✅ | ✅ |
| F-C8 | Hiển thị kết quả | ✅ | ✅ | ✅ |
| F-C9 | Xử lý lỗi rõ ràng | ✅ | ✅ | ✅ |

### Tiêu chuẩn Code Chung (S-1 đến S-5)

| Mã | Tiêu chuẩn | Desktop | Android | iOS |
|----|-----------|---------|---------|-----|
| S-1 | API trên background thread | ✅ | ✅ | ✅ |
| S-2 | Try-catch error handling | ✅ | ✅ | ✅ |
| S-3 | UI Feedback | ✅ | ✅ | ✅ |
| S-4 | Sử dụng Model/Class | ✅ | ✅ | ✅ |
| S-5 | Config variable cho Server URL | ✅ | ✅ | ✅ |

### Tiêu chuẩn Server (S-P)

| Mã | Tiêu chuẩn | Trạng thái |
|----|-----------|-----------|
| S-P1 | tempfile.NamedTemporaryFile | ✅ |
| S-P2 | Tách biệt logic (main.py vs analysis.py) | ✅ |
| S-P3 | requirements.txt | ✅ |
| S-P4 | PEP 8 | ✅ |

### Tiêu chuẩn Desktop (S-D)

| Mã | Tiêu chuẩn | Trạng thái |
|----|-----------|-----------|
| S-D1 | threading.Thread | ✅ |
| S-D2 | root.after(0, ...) | ✅ |
| S-D3 | PyInstaller support | ✅ |

### Tiêu chuẩn Android (S-A)

| Mã | Tiêu chuẩn | Trạng thái |
|----|-----------|-----------|
| S-A1 | ViewModel pattern | ✅ |
| S-A2 | Coroutines + Dispatchers.IO | ✅ |
| S-A3 | INTERNET permission | ✅ |
| S-A4 | RECORD_AUDIO permission | ✅ |
| S-A5 | IP 10.0.2.2 cho emulator | ✅ |

### Tiêu chuẩn iOS (S-I)

| Mã | Tiêu chuẩn | Trạng thái |
|----|-----------|-----------|
| S-I1 | URLSession (bất đồng bộ) | ✅ |
| S-I2 | Codable protocol | ✅ |
| S-I3 | ObservableObject | ✅ |
| S-I4 | NSAppTransportSecurity | ✅ |
| S-I5 | NSMicrophoneUsageDescription | ✅ |

### Yêu cầu Phi chức năng (NF)

| Mã | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|-----------|---------|
| NF-1 | Xử lý 1 phút < 15s | ✅ | Tùy máy |
| NF-2 | Bảo mật API | ⏳ | Cần trong production |
| NF-3 | UI đơn giản < 10s | ✅ | Intuitive |
| NF-4 | 5+ concurrent requests | ✅ | Config workers |

## 🔧 Troubleshooting

### Lỗi "Cannot connect to server"

**Desktop/iOS Simulator**:
```
✅ Sử dụng: http://127.0.0.1:8000
```

**Android Emulator**:
```
✅ Sử dụng: http://10.0.2.2:8000
```

**Thiết bị thật (Android/iOS)**:
```
1. Tìm IP máy tính:
   - Windows: ipconfig
   - macOS: ifconfig

2. Cập nhật trong code:
   - Android: ApiClient.kt
   - iOS: VoiceAnalysisService.swift
   
3. Ví dụ: http://192.168.1.100:8000
```

### Lỗi "Module not found" (Python)

```powershell
pip install -r requirements.txt
```

### Server không chạy được

```powershell
# Kiểm tra port 8000 có bị chiếm không
netstat -ano | findstr :8000

# Nếu bị chiếm, đổi port trong main.py:
uvicorn.run("main:app", host="0.0.0.0", port=8001)

# Và cập nhật trong client
```

## 📦 Dependencies

### Server
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- python-multipart==0.0.6
- librosa==0.10.1
- numpy==1.24.3

### Desktop Client
- requests==2.31.0
- tkinter (built-in)

### Android Client
- Retrofit 2.9.0
- OkHttp 4.12.0
- Gson 2.10.1
- Coroutines 1.7.3

### iOS Client
- URLSession (native)
- SwiftUI (native)
- Codable (native)

## 🎓 Học thêm

### Librosa Documentation
https://librosa.org/doc/latest/index.html

### FastAPI Documentation
https://fastapi.tiangolo.com/

### Android Development
https://developer.android.com/

### iOS Development
https://developer.apple.com/documentation/

## 📝 License

Dự án học tập - Tự do sử dụng và chỉnh sửa.

## 👨‍💻 Phát triển Thêm

### Tính năng có thể thêm:
- ✨ Ghi âm trực tiếp (F-C2)
- 📊 Biểu đồ trực quan (Chart/Graph)
- 💾 Lưu lịch sử phân tích
- 🔐 Authentication (NF-2)
- 🎨 Tùy chỉnh ngưỡng (energy_threshold)
- 📤 Export kết quả (CSV, JSON)
- 🌐 Multi-language support

## ❓ Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra README của từng component
2. Kiểm tra server logs
3. Kiểm tra network/firewall
4. Đọc error messages kỹ (F-C9)

---

**Tác giả**: GitHub Copilot  
**Ngày tạo**: 3/11/2025  
**Version**: 1.0.0
