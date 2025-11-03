# Voice Analysis Android Client

Ứng dụng Android (Kotlin) cho hệ thống phân tích Voiced/Unvoiced/Silence.

## Yêu cầu

- Android Studio (phiên bản mới nhất)
- Android SDK 24+ (Android 7.0)
- Kotlin 1.9+

## Cài đặt

### 1. Mở project trong Android Studio

```
File -> Open -> Chọn thư mục android_client
```

### 2. Sync Gradle

Android Studio sẽ tự động sync dependencies.

### 3. Cấu hình Server URL (S-5, S-A5)

Mở file `app/src/main/java/com/voiceanalysis/app/data/network/ApiClient.kt`:

```kotlin
// Cho Emulator (S-A5)
private const val BASE_URL = "http://10.0.2.2:8000/"

// Cho thiết bị thật (S-A5)
// private const val BASE_URL = "http://192.168.1.100:8000/"
```

**Lưu ý**: 
- Emulator sử dụng IP `10.0.2.2` để truy cập localhost của máy host
- Thiết bị thật cần sử dụng IP nội bộ của máy tính (tìm bằng `ipconfig`)

## Chạy Ứng dụng

### 1. Chạy Server trước

```powershell
cd ../server
python main.py
```

### 2. Chạy ứng dụng Android

- Click nút "Run" (▶️) trong Android Studio
- Hoặc: `Run -> Run 'app'`

## Kiến trúc & Tech Stack

### Tech Stack (Theo S-A)

- **Kotlin**: Ngôn ngữ chính
- **Retrofit + OkHttp**: Networking
- **Gson**: JSON parsing
- **Coroutines**: Asynchronous programming
- **ViewModel + LiveData**: MVVM architecture
- **Material Design 3**: UI components

### Cấu trúc Code

```
app/
├── data/
│   ├── model/              # Data models (S-4)
│   ├── network/            # API interface & client
│   └── repository/         # Business logic
├── ui/
│   ├── MainActivity.kt     # UI layer
│   └── MainViewModel.kt    # ViewModel (S-A1)
└── res/
    └── layout/             # UI layouts
```

## Quyền (Permissions)

### Đã khai báo trong AndroidManifest.xml:

- ✅ `INTERNET` (S-A3) - Bắt buộc
- ✅ `READ_EXTERNAL_STORAGE` - Đọc file
- ✅ `READ_MEDIA_AUDIO` (Android 13+)
- ✅ `RECORD_AUDIO` (S-A4) - Nếu có ghi âm

### Runtime Permissions

App tự động xin quyền khi cần thiết.

## Tuân thủ Tiêu chuẩn

### General (S-1 đến S-5)
- ✅ S-1: API calls trên background (Coroutines)
- ✅ S-2: Try-catch error handling
- ✅ S-3: UI feedback rõ ràng
- ✅ S-4: Model classes để parse JSON
- ✅ S-5: Server URL trong config

### Android Specific (S-A1 đến S-A5)
- ✅ S-A1: ViewModel pattern
- ✅ S-A2: Coroutines với Dispatchers.IO
- ✅ S-A3: INTERNET permission
- ✅ S-A4: RECORD_AUDIO permission
- ✅ S-A5: IP 10.0.2.2 cho emulator

### Functional Requirements (F-C1 đến F-C9)
- ✅ F-C1: Chọn file từ storage
- ✅ F-C3: Hiển thị tên file
- ✅ F-C4: Nút Analyze
- ✅ F-C5: Gửi file đến API
- ✅ F-C6: Loading state và disable button
- ✅ F-C7: Parse JSON response
- ✅ F-C8: Hiển thị kết quả
- ✅ F-C9: Error handling rõ ràng

## Troubleshooting

### Lỗi kết nối server

1. Kiểm tra server đang chạy
2. Kiểm tra IP trong `ApiClient.kt`:
   - Emulator: `10.0.2.2:8000`
   - Thiết bị thật: IP nội bộ máy tính
3. Kiểm tra firewall không chặn port 8000

### Lấy IP nội bộ máy tính (Windows)

```powershell
ipconfig
```

Tìm "IPv4 Address" trong phần WiFi/Ethernet adapter.

### Build APK

```
Build -> Build Bundle(s) / APK(s) -> Build APK(s)
```

APK sẽ nằm trong `app/build/outputs/apk/debug/`.
