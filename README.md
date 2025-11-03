# 🎙️ Voice Analysis System - Hệ Thống Phân Tích Âm Thanh

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Swift](https://img.shields.io/badge/Swift-5.7+-orange.svg)](https://swift.org)
[![Kotlin](https://img.shields.io/badge/Kotlin-1.9.20-purple.svg)](https://kotlinlang.org)

**Hệ thống phân tích âm thanh đầy đủ** phân loại các đoạn âm thanh thành **Voiced** (có thanh), **Unvoiced** (không thanh), và **Silence** (im lặng).

🌟 **Server**: Python/FastAPI + Librosa  
📱 **Clients**: Desktop (Python/Tkinter) | Android (Kotlin) | iOS (Swift)

---

## 📋 Mục Lục

- [Tính Năng](#-tính-năng)
- [Kiến Trúc](#-kiến-trúc-hệ-thống)
- [Cài Đặt Nhanh](#-cài-đặt-nhanh)
- [Sử Dụng](#-hướng-dẫn-sử-dụng)
- [API Documentation](#-api-documentation)
- [Cấu Trúc Project](#-cấu-trúc-project)
- [Testing](#-testing)

---

## ✨ Tính Năng

### 🎯 **Phân Tích Âm Thanh**
- ✅ **VOICED**: Phát hiện âm có thanh quản (F0 > 0)
- ✅ **UNVOICED**: Phát hiện âm không thanh (F0 = 0, energy cao)
- ✅ **SILENCE**: Phát hiện im lặng (energy thấp)
- ✅ Tính **F0 (Pitch)** bằng thuật toán pYIN (65-2093 Hz)
- ✅ Tính **Energy (RMS)** cho từng frame
- ✅ Frame size: 32ms, hop: 32ms

### 🖥️ **Desktop Client (Python/Tkinter)**
- ✅ Chọn file audio (WAV, MP3, M4A, FLAC, OGG)
- ✅ **Ghi âm trực tiếp** từ microphone (16kHz, mono)
- ✅ Hiển thị kết quả dạng **Table** với color coding:
  - 🔊 VOICED: màu xanh lá nhạt
  - 💨 UNVOICED: màu cam nhạt
  - 🔇 SILENCE: màu xám nhạt
- ✅ Thống kê với **Progress Bars**
- ✅ Giao diện hiện đại, card-based design
- ✅ Recording timer MM:SS

### 📱 **Android Client (Kotlin)**
- ✅ Material Design 3
- ✅ MVVM Architecture (ViewModel + LiveData)
- ✅ Retrofit 2.9.0 + OkHttp 4.12.0
- ✅ Coroutines 1.7.3 cho async operations
- ✅ File picker từ device storage
- ✅ Progress indicator khi analyzing

### 🍎 **iOS Client (Swift/SwiftUI)**
- ✅ SwiftUI native interface
- ✅ ObservableObject pattern
- ✅ URLSession cho HTTP requests
- ✅ Document picker integration
- ✅ Codable JSON parsing
- ✅ iOS 15.0+

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌────────────────────────────────────────────────┐
│              CLIENTS (UI Layer)                │
├──────────┬──────────┬────────────────────────┬─┤
│ Desktop  │ Android  │         iOS            │ │
│ Tkinter  │ Kotlin   │        Swift           │ │
└────┬─────┴────┬─────┴────────┬───────────────┘ │
     │          │              │                  │
     │  HTTP    │   HTTP       │   HTTP          │
     │  POST    │   POST       │   POST          │
     │          │              │                  │
     └──────────┴──────────────┘                  │
                │                                 │
                ▼                                 │
     ┌──────────────────────┐                    │
     │   FastAPI Server     │                    │
     │  - Receive Audio     │                    │
     │  - Analyze w/Librosa │                    │
     │  - Return JSON       │                    │
     └──────────┬───────────┘                    │
                │                                 │
                ▼                                 │
     ┌──────────────────────┐                    │
     │  Analysis Engine     │                    │
     │  (Librosa 0.10.1)    │                    │
     │  • F0 Extraction     │                    │
     │    (pyin method)     │                    │
     │  • RMS Energy Calc   │                    │
     │  • Classification:   │                    │
     │    - VOICED          │                    │
     │    - UNVOICED        │                    │
     │    - SILENCE         │                    │
     └──────────────────────┘                    │
```

**Nguyên tắc:**
- Client chỉ làm UI, không xử lý logic
- Server tập trung toàn bộ xử lý audio
- RESTful API với JSON response
- Multipart/form-data upload

---

## 🚀 Cài Đặt Nhanh

### **Yêu Cầu Hệ Thống**
- Python 3.9+
- FFmpeg (để xử lý MP3, M4A)
- PyAudio (cho ghi âm desktop)

### **1️⃣ Clone Repository**

```bash
git clone https://github.com/peaceful-fptu-k16/VoiceUnvoiceSystem.git
cd VoiceUnvoiceSystem
```

### **2️⃣ Setup Server (Bắt Buộc)**

```bash
cd server
pip install -r requirements.txt
python main.py
```

✅ Server chạy tại: **http://localhost:8000**  
📚 API Docs: **http://localhost:8000/docs**

**Server Config:**
- Host: `0.0.0.0` (cho phép kết nối từ network)
- Port: `8000`
- CORS: Enabled (allow all origins)

### **3️⃣ Setup Desktop Client**

```bash
cd desktop_client
pip install -r requirements.txt

# Windows: Cài PyAudio cho recording
pip install pyaudio

# Chạy app
python desktop_app.py
```

**Desktop Features:**
- ✅ Browse files
- ✅ Record from microphone
- ✅ Analyze và view results
- ✅ Clear results

### **4️⃣ Setup Android Client**

**Yêu cầu:**
- Android Studio Arctic Fox+
- Android SDK 34
- Kotlin 1.9.20

**Các bước:**
1. Mở `android_client` trong Android Studio
2. Sync Gradle dependencies
3. Cập nhật server URL trong `ApiClient.kt`:
   ```kotlin
   private const val BASE_URL = "http://10.0.2.2:8000/"  // Emulator
   // hoặc
   private const val BASE_URL = "http://192.168.x.x:8000/"  // Real device
   ```
4. Run trên emulator hoặc device (cùng WiFi)

**Dependencies:**
```kotlin
// Networking
implementation("com.squareup.retrofit2:retrofit:2.9.0")
implementation("com.squareup.okhttp3:okhttp:4.12.0")
implementation("com.google.code.gson:gson:2.10.1")

// Coroutines
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

// ViewModel & LiveData
implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2")
```

### **5️⃣ Setup iOS Client**

**Yêu cầu:**
- macOS 12.0+ (Monterey)
- Xcode 14+
- iOS 15.0+ device/simulator

**Các bước:**
1. Copy `ios_client` sang Mac
2. Mở Xcode, tạo new iOS App project (SwiftUI)
3. Copy tất cả files vào project:
   - `Models/AnalysisResponse.swift`
   - `Services/VoiceAnalysisService.swift`
   - `ViewModels/ContentViewModel.swift`
   - `Views/ContentView.swift`
   - `VoiceAnalysisApp.swift`
4. Copy nội dung `Info.plist`
5. Cập nhật server URL trong `VoiceAnalysisService.swift`:
   ```swift
   private let baseURL = "http://192.168.20.100:8000"  // IP máy chạy server
   ```
6. Select iPhone/Simulator và Run (Cmd + R)

**Lưu ý iOS:**
- iPhone và máy chạy server phải **cùng WiFi**
- Info.plist cần `NSAppTransportSecurity` để cho phép HTTP
- Simulator có thể dùng `localhost` hoặc IP máy Mac

---

## 📖 Hướng Dẫn Sử Dụng

### **Desktop Client**

1. **Khởi động server** (trong terminal riêng):
   ```bash
   cd server
   python main.py
   ```

2. **Chạy Desktop app**:
   ```bash
   cd desktop_client
   python desktop_app.py
   ```

3. **Sử dụng:**
   - **Option 1: Browse file**
     - Click "📂 BROWSE FILES"
     - Chọn file audio (.wav, .mp3, .m4a, .flac, .ogg)
     - Click "🔍 ANALYZE AUDIO"
   
   - **Option 2: Record from mic**
     - Click "⚫ START RECORDING"
     - Nói vào microphone
     - Click "⏹️ STOP RECORDING" khi xong
     - File tự động được chọn
     - Click "🔍 ANALYZE AUDIO"

4. **Xem kết quả:**
   - Statistics: Tổng số frames và phần trăm từng loại
   - Table: Toàn bộ segments với màu sắc

### **Android Client**

1. **Setup server URL:**
   - Emulator: `http://10.0.2.2:8000/`
   - Real device: `http://192.168.x.x:8000/` (IP máy chạy server)

2. **Test:**
   - Click "Choose File"
   - Select audio file
   - Click "Analyze"
   - View results

### **iOS Client**

1. **Chuẩn bị:**
   - Server chạy trên Windows/Mac
   - iPhone và máy chạy server cùng WiFi
   - Tìm IP máy server: `ipconfig` (Windows) hoặc `ifconfig` (Mac)

2. **Update server URL** trong `VoiceAnalysisService.swift`

3. **Test:**
   - Click "Choose Audio File"
   - Select từ Files app
   - Click "Analyze"
   - View results

---

## 📊 API Documentation

### **Endpoint: POST /analyze/**

Phân tích file âm thanh và trả về danh sách segments.

**Request:**
```http
POST /analyze/
Content-Type: multipart/form-data

file: <audio_file>
```

**Supported Formats:**
- WAV (recommended)
- MP3
- M4A
- FLAC
- OGG

**Response (200 OK):**
```json
{
  "filename": "audio.wav",
  "total_segments": 1178,
  "segments": [
    {
      "time": 0.000,
      "type": "UNVOICED",
      "f0": 0.00,
      "energy": 0.214100
    },
    {
      "time": 0.032,
      "type": "VOICED",
      "f0": 156.25,
      "energy": 0.301700
    },
    {
      "time": 0.064,
      "type": "SILENCE",
      "f0": 0.00,
      "energy": 0.001234
    }
  ]
}
```

**Classification Rules:**
- **SILENCE**: `energy < 0.02`
- **VOICED**: `energy >= 0.02` AND `f0 > 0`
- **UNVOICED**: `energy >= 0.02` AND `f0 == 0`

**Error Responses:**
```json
// 400 Bad Request
{
  "detail": {
    "code": "INVALID_FILE",
    "message": "File không hợp lệ hoặc định dạng không được hỗ trợ"
  }
}

// 500 Internal Server Error
{
  "detail": {
    "code": "PROCESSING_ERROR",
    "message": "Lỗi khi xử lý file audio"
  }
}
```

**Interactive Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Test với cURL:**
```bash
curl -X POST http://localhost:8000/analyze/ \
  -F "file=@test_audio.wav"
```

---

## 📁 Cấu Trúc Project

```
VoiceUnvoiceSystem/
│
├── server/                      # 🔧 Backend API Server
│   ├── main.py                 # FastAPI endpoints, CORS config
│   ├── analysis.py             # AudioAnalyzer class, Librosa logic
│   └── requirements.txt        # Python dependencies
│
├── desktop_client/             # 🖥️ Desktop Application
│   ├── desktop_app.py          # Tkinter GUI với recording feature
│   └── requirements.txt        # includes tkinter, requests, pyaudio
│
├── android_client/             # 📱 Android Application
│   └── app/
│       ├── build.gradle.kts    # Dependencies config
│       └── src/main/
│           ├── java/com/voiceanalysis/app/
│           │   ├── MainActivity.kt          # Main UI
│           │   ├── ui/MainViewModel.kt      # MVVM ViewModel
│           │   ├── data/
│           │   │   ├── model/AnalysisResponse.kt
│           │   │   ├── network/VoiceAnalysisApi.kt
│           │   │   ├── network/ApiClient.kt
│           │   │   └── repository/VoiceAnalysisRepository.kt
│           │   └── res/
│           │       ├── layout/activity_main.xml
│           │       └── values/strings.xml
│           └── AndroidManifest.xml
│
├── ios_client/                 # 🍎 iOS Application
│   └── VoiceAnalysis/
│       ├── Models/
│       │   └── AnalysisResponse.swift      # Codable data models
│       ├── Services/
│       │   └── VoiceAnalysisService.swift  # URLSession API calls
│       ├── ViewModels/
│       │   └── ContentViewModel.swift      # ObservableObject
│       ├── Views/
│       │   └── ContentView.swift           # SwiftUI main view
│       ├── VoiceAnalysisApp.swift          # App entry point
│       └── Info.plist                      # App config, permissions
│
├── create_test_audio.py        # Script tạo file test audio
├── .gitignore                  # Git ignore patterns
└── README.md                   # This file
```

**Tổng số files:** 36 files  
**Tổng số dòng code:** ~5,700 lines  
**Ngôn ngữ:** Python, Kotlin, Swift

---

## 🧪 Testing

### **1. Generate Test Audio Files**

```bash
python create_test_audio.py
```

Tạo 2 files:
- `test_audio.wav` (5 giây) - Test nhanh
- `test_60s.wav` (60 giây) - Test full

### **2. Test Server**

```bash
# Terminal 1: Chạy server
cd server
python main.py

# Terminal 2: Test API
curl -X POST http://localhost:8000/analyze/ \
  -F "file=@test_audio.wav"
```

**Expected response:**
- Status: 200 OK
- JSON với filename, total_segments, segments array
- Segments có time, type, f0, energy

### **3. Test Desktop Client**

```bash
cd desktop_client
python desktop_app.py
```

**Test cases:**
1. ✅ Browse file → Select test_audio.wav → Analyze → Xem kết quả
2. ✅ Record 5s → Stop → Analyze → Xem kết quả
3. ✅ Clear results → UI reset
4. ✅ Test error: Tắt server → Analyze → Hiện error alert

### **4. Test Android**

**Emulator:**
1. Update BASE_URL = `http://10.0.2.2:8000/`
2. Run trong Android Studio
3. Choose file → Analyze

**Real Device:**
1. Tìm IP máy chạy server: `ipconfig`
2. Update BASE_URL = `http://192.168.x.x:8000/`
3. iPhone và Android cùng WiFi
4. Run app → Test

### **5. Test iOS**

**Simulator:**
1. Server URL có thể dùng localhost
2. Run trong Xcode
3. Choose file → Analyze

**Real iPhone:**
1. iPhone và máy server cùng WiFi
2. Update baseURL với IP máy server
3. Trust developer certificate trong Settings
4. Run app → Test

### **Firewall (Windows)**

Nếu mobile không kết nối được server:
```powershell
netsh advfirewall firewall add rule name="Python Server" dir=in action=allow protocol=TCP localport=8000
```

---

## 🛠️ Công Nghệ & Dependencies

### **Backend (Server)**

| Package | Version | Mục đích |
|---------|---------|----------|
| FastAPI | 0.104.1 | Web framework |
| Uvicorn | 0.24.0 | ASGI server |
| Librosa | 0.10.1 | Audio analysis |
| NumPy | 1.24.3 | Array processing |
| python-multipart | 0.0.6 | File upload |

**Install:**
```bash
pip install fastapi==0.104.1 uvicorn==0.24.0 librosa==0.10.1 numpy==1.24.3 python-multipart==0.0.6
```

### **Desktop Client**

| Package | Version | Mục đích |
|---------|---------|----------|
| tkinter | Built-in | GUI framework |
| requests | 2.31.0 | HTTP client |
| pyaudio | 0.2.14 | Microphone recording |

**Install:**
```bash
pip install requests==2.31.0 pyaudio==0.2.14
```

### **Android Client**

```gradle
// Networking
implementation 'com.squareup.retrofit2:retrofit:2.9.0'
implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
implementation 'com.squareup.okhttp3:okhttp:4.12.0'
implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0'

// Coroutines
implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3'

// ViewModel & LiveData
implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.6.2'

// Material Design
implementation 'com.google.android.material:material:1.10.0'
```

### **iOS Client**

- Swift 5.7+
- iOS 15.0+
- SwiftUI (native)
- URLSession (native)
- Codable (native)

**No external dependencies!**

---

## 🎯 Tuân Thủ Yêu Cầu

### **Functional Requirements**

#### **Server (F-S1 đến F-S6)**
- ✅ F-S1: POST endpoint `/analyze/` nhận file audio
- ✅ F-S2: Tính F0 cho từng frame (pYIN, 65-2093 Hz)
- ✅ F-S3: Tính Energy (RMS) cho từng frame
- ✅ F-S4: Phân loại VOICED/UNVOICED/SILENCE
- ✅ F-S5: Trả về JSON với filename, total_segments, segments
- ✅ F-S6: Error handling với status codes và messages

#### **Clients (F-C1 đến F-C9)**
- ✅ F-C1: File picker UI
- ✅ F-C2: Recording từ microphone (Desktop only)
- ✅ F-C3: Hiển thị tên file đã chọn
- ✅ F-C4: Button "Analyze"
- ✅ F-C5: Upload file lên server qua HTTP POST
- ✅ F-C6: Disable button khi đang analyze, loading indicator
- ✅ F-C7: Parse JSON response
- ✅ F-C8: Hiển thị kết quả (filename, stats, segments)
- ✅ F-C9: Error handling với alerts/dialogs

### **Non-Functional Requirements**

- ✅ NF-1: Async operations (không block UI)
- ✅ NF-2: Basic auth ready (server config)
- ✅ NF-3: UI đơn giản, trực quan
- ✅ NF-4: Server handle multiple requests (Uvicorn ASGI)

### **Code Standards**

- ✅ S-1: Async/background threads
- ✅ S-2: Try-catch error handling
- ✅ S-3: UI feedback (loading, success, error)
- ✅ S-4: Data models (AnalysisResponse)
- ✅ S-5: Config variables (không hardcode)

---

## 🚨 Troubleshooting

### **Server không khởi động**

```bash
# Check port 8000 đã bị chiếm chưa
netstat -ano | findstr :8000

# Kill process nếu cần
taskkill /PID <pid> /F

# Hoặc đổi port trong main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### **Desktop: PyAudio install lỗi**

**Windows:**
```bash
# Cách 1: Dùng wheel file
pip install pyaudio

# Cách 2: Dùng pipwin
pip install pipwin
pipwin install pyaudio
```

### **Android: Cannot connect to server**

**Emulator:** Dùng `10.0.2.2` thay vì `localhost`  
**Real device:**
1. Check cùng WiFi
2. Dùng IP máy chạy server
3. Check firewall không chặn port 8000

### **iOS: App Transport Security blocked**

Thêm vào `Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

⚠️ Trong production nên dùng HTTPS!

### **Analysis lỗi với MP3/M4A**

Cài FFmpeg:
- **Windows**: Download từ ffmpeg.org, thêm vào PATH
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

---

## 📞 Support & Contributing

### **Báo Lỗi**
- Tạo Issue trên GitHub với:
  - Mô tả lỗi
  - Steps to reproduce
  - Screenshots nếu có
  - OS version, Python version

### **Contributing**
1. Fork repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📄 License

MIT License - Free to use, modify, distribute.

---

## 👥 Authors

**Voice Unvoice System Team**  
GitHub: [@peaceful-fptu-k16](https://github.com/peaceful-fptu-k16)

---

## � Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Librosa](https://librosa.org/) - Audio analysis library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI
- [Retrofit](https://square.github.io/retrofit/) - Android HTTP client
- [SwiftUI](https://developer.apple.com/xcode/swiftui/) - iOS UI framework

---

<p align="center">
  <strong>⭐ Star this repo if you find it helpful!</strong><br>
  Made with ❤️ by peaceful-fptu-k16
</p>


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
