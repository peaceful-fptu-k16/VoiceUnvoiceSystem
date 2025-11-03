# 🎙️ Voice Analysis System

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Swift](https://img.shields.io/badge/Swift-5.7+-orange.svg)](https://swift.org)
[![Kotlin](https://img.shields.io/badge/Kotlin-1.9.20-purple.svg)](https://kotlinlang.org)

**Hệ thống phân tích âm thanh thành Voiced/Unvoiced/Silence** với kiến trúc Client-Server hoàn chỉnh.

🌟 **Server**: Python/FastAPI + Librosa  
📱 **Clients**: Desktop (Python/Tkinter) | Android (Kotlin) | iOS (Swift)

---

## 📸 Demo

### Desktop Client
![Desktop App](https://via.placeholder.com/800x500/2c3e50/ecf0f1?text=Desktop+Client+-+Beautiful+UI+with+Table+View)

### Mobile Clients
<p align="center">
  <img src="https://via.placeholder.com/300x600/e74c3c/ffffff?text=Android+App" width="250"/>
  <img src="https://via.placeholder.com/300x600/3498db/ffffff?text=iOS+App" width="250"/>
</p>

---

## ✨ Tính Năng Chính

### 🎯 **Phân Tích Âm Thanh**
- ✅ Phát hiện **VOICED** (có thanh quản: F0 > 0)
- ✅ Phát hiện **UNVOICED** (không có thanh quản: F0 = 0, energy cao)
- ✅ Phát hiện **SILENCE** (im lặng: energy thấp)
- ✅ Tính toán **F0 (Pitch)** bằng thuật toán pYIN
- ✅ Tính toán **Energy (RMS)** cho mỗi frame

### 🖥️ **Desktop Client**
- ✅ Chọn file audio (WAV, MP3, M4A, FLAC, OGG)
- ✅ **Ghi âm trực tiếp** từ microphone
- ✅ Hiển thị kết quả dạng **Table** với màu sắc
- ✅ Thống kê với **Progress Bars**
- ✅ Giao diện đẹp, hiện đại

### 📱 **Android Client**
- ✅ Material Design 3
- ✅ MVVM Architecture
- ✅ Coroutines + Flow
- ✅ Retrofit + OkHttp
- ✅ File picker từ storage

### 🍎 **iOS Client**
- ✅ SwiftUI
- ✅ ObservableObject pattern
- ✅ Native URLSession
- ✅ Document picker
- ✅ Codable JSON parsing

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
     │  • F0 Extraction     │                    │
     │  • Energy Calc       │                    │
     │  • Classification    │                    │
     └──────────────────────┘                    │
```

---

## 🚀 Cài Đặt Nhanh

### **1️⃣ Clone Repository**

```bash
git clone https://github.com/peaceful-fptu-k16/VoiceUnvoiceSystem.git
cd VoiceUnvoiceSystem
```

### **2️⃣ Setup Server**

```bash
cd server
pip install -r requirements.txt
python main.py
```

Server chạy tại: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### **3️⃣ Setup Desktop Client**

```bash
cd desktop_client
pip install -r requirements.txt
python desktop_app.py
```

### **4️⃣ Setup Android Client**

1. Mở `android_client` trong Android Studio
2. Sync Gradle
3. Cập nhật server URL trong `ApiClient.kt`
4. Run trên emulator/device

### **5️⃣ Setup iOS Client**

1. Mở `ios_client` trong Xcode
2. Cập nhật server URL trong `VoiceAnalysisService.swift`
3. Run trên Simulator/iPhone

---

## 📚 Tài Liệu Chi Tiết

| File | Mô Tả |
|------|-------|
| [QUICKSTART.md](QUICKSTART.md) | Hướng dẫn nhanh 5 phút |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Kiến trúc chi tiết |
| [TESTING.md](TESTING.md) | Hướng dẫn test |
| [COMPLIANCE.md](COMPLIANCE.md) | Tuân thủ yêu cầu |
| [FILE_LIST.md](FILE_LIST.md) | Danh sách file |
| [server/README.md](server/README.md) | Server docs |
| [desktop_client/README.md](desktop_client/README.md) | Desktop docs |
| [android_client/README.md](android_client/README.md) | Android docs |
| [ios_client/README.md](ios_client/README.md) | iOS docs |

---

## 🛠️ Công Nghệ Sử Dụng

### **Backend**
- ![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python) **Python 3.9+**
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?logo=fastapi) **FastAPI** - Web framework
- ![Librosa](https://img.shields.io/badge/Librosa-0.10.1-orange) **Librosa** - Audio analysis
- ![NumPy](https://img.shields.io/badge/NumPy-1.24.3-blue?logo=numpy) **NumPy** - Array processing
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.24.0-green) **Uvicorn** - ASGI server

### **Desktop Client**
- ![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python) **Python 3.9+**
- ![Tkinter](https://img.shields.io/badge/Tkinter-Native-blue) **Tkinter** - GUI framework
- ![PyAudio](https://img.shields.io/badge/PyAudio-0.2.14-red) **PyAudio** - Microphone recording
- ![Requests](https://img.shields.io/badge/Requests-2.31.0-green) **Requests** - HTTP client

### **Android Client**
- ![Kotlin](https://img.shields.io/badge/Kotlin-1.9.20-purple?logo=kotlin) **Kotlin 1.9.20**
- ![Android](https://img.shields.io/badge/Android-SDK%2034-green?logo=android) **Android SDK 34**
- ![Retrofit](https://img.shields.io/badge/Retrofit-2.9.0-blue) **Retrofit** - HTTP client
- ![Coroutines](https://img.shields.io/badge/Coroutines-1.7.3-purple) **Coroutines** - Async
- ![ViewModel](https://img.shields.io/badge/ViewModel-2.6.2-green) **ViewModel** - MVVM

### **iOS Client**
- ![Swift](https://img.shields.io/badge/Swift-5.7-orange?logo=swift) **Swift 5.7+**
- ![iOS](https://img.shields.io/badge/iOS-15.0+-black?logo=apple) **iOS 15.0+**
- ![SwiftUI](https://img.shields.io/badge/SwiftUI-Native-blue) **SwiftUI** - UI framework
- ![URLSession](https://img.shields.io/badge/URLSession-Native-green) **URLSession** - HTTP client

---

## 📊 API Documentation

### **POST /analyze/**

Phân tích file âm thanh và trả về kết quả.

**Request:**
```http
POST /analyze/
Content-Type: multipart/form-data

file: <audio_file>
```

**Response:**
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
    }
  ]
}
```

**Supported Formats:** WAV, MP3, M4A, FLAC, OGG

Interactive API docs: `http://localhost:8000/docs`

---

## 🧪 Testing

### **Test Server**
```bash
cd server
python main.py

# Trong terminal khác
curl -X POST http://localhost:8000/analyze/ \
  -F "file=@test_audio.wav"
```

### **Generate Test Files**
```bash
python create_test_audio.py
# Tạo test_audio.wav (5s) và test_60s.wav (60s)
```

### **Run All Tests**
```bash
# Test Desktop
cd desktop_client && python desktop_app.py

# Test Android
# Mở Android Studio → Run

# Test iOS
# Mở Xcode → Run
```

---

## 📁 Cấu Trúc Project

```
VoiceUnvoiceSystem/
├── server/                   # Backend API Server
│   ├── main.py              # FastAPI endpoints
│   ├── analysis.py          # Audio analysis logic
│   └── requirements.txt     # Python dependencies
│
├── desktop_client/          # Desktop Application
│   ├── desktop_app.py       # Tkinter GUI with recording
│   ├── requirements.txt     # Python dependencies
│   └── README.md
│
├── android_client/          # Android Application
│   └── app/
│       └── src/main/
│           ├── java/.../    # Kotlin source
│           └── res/         # Resources
│
├── ios_client/              # iOS Application
│   └── VoiceAnalysis/
│       ├── Models/          # Data models
│       ├── Services/        # API service
│       ├── ViewModels/      # View models
│       └── Views/           # SwiftUI views
│
├── docs/                    # Documentation
├── create_test_audio.py     # Test file generator
└── README.md               # This file
```

---

## 🎨 Screenshots

### Desktop - Modern UI
- 🎤 Microphone recording với timer
- 📊 Table view với color coding
- 📈 Progress bars cho statistics
- 🎯 Clean, modern design

### Android - Material Design
- 📱 Material Design 3
- 🎨 Modern card-based layout
- ⚡ Fast and responsive

### iOS - Native Experience
- 🍎 Native iOS controls
- 🎨 SwiftUI interface
- 📄 Document picker integration

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Voice Unvoice System Team**
- Email: peaceful-fptu-k16@github.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Librosa](https://librosa.org/) - Audio analysis
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Desktop GUI
- [Retrofit](https://square.github.io/retrofit/) - Android HTTP
- [SwiftUI](https://developer.apple.com/xcode/swiftui/) - iOS UI

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/peaceful-fptu-k16">peaceful-fptu-k16</a>
</p>

<p align="center">
  ⭐ Star this repo if you find it helpful!
</p>
