# 📱 HƯỚNG DẪN TEST ỨNG DỤNG iOS

## ✅ Yêu Cầu

### Phần Cứng & Phần Mềm:
- ✅ **Mac** với macOS 12.0+ (Monterey hoặc mới hơn)
- ✅ **Xcode 14+** (download từ App Store)
- ✅ **iPhone** với iOS 15.0+ HOẶC **iOS Simulator**
- ✅ **Cable Lightning/USB-C** (nếu test trên thiết bị thật)

### Network:
- ✅ iPhone và máy chạy server phải **cùng mạng WiFi**
- ✅ IP máy Windows: **192.168.20.100** (đã được cập nhật trong code)
- ✅ Server đang chạy trên port **8000**

---

## 🚀 BƯỚC 1: Khởi Động Server

### Trên máy Windows (E:\VoiceUnvoiceSystem):

```powershell
# Di chuyển vào thư mục server
cd server

# Chạy server
python main.py
```

**Kiểm tra server đã chạy:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

⚠️ **Lưu ý:** Server phải dùng `0.0.0.0` thay vì `127.0.0.1` để iPhone có thể kết nối!

Nếu server hiện tại chạy `127.0.0.1`, cần sửa file `server/main.py`:
```python
# Dòng cuối cùng, thay đổi:
uvicorn.run(app, host="0.0.0.0", port=8000)  # Thay "127.0.0.1" thành "0.0.0.0"
```

---

## 🍎 BƯỚC 2: Mở Project trong Xcode

### 2.1. Copy project sang Mac

Nếu bạn đang trên Windows, cần chuyển thư mục `ios_client` sang Mac:

**Cách 1: USB Drive**
- Copy thư mục `E:\VoiceUnvoiceSystem\ios_client` vào USB
- Chép sang Mac vào thư mục `~/VoiceAnalysis`

**Cách 2: AirDrop (nếu có Mac gần)**
- Nén thư mục `ios_client` thành zip
- AirDrop sang Mac

**Cách 3: Git**
```bash
# Nếu đã init git repo
git add .
git commit -m "iOS app ready"
git push

# Trên Mac
git clone <repo-url>
```

### 2.2. Tạo Xcode Project

Hiện tại chưa có file `.xcodeproj`. Trên Mac, mở Terminal và chạy:

```bash
cd ~/VoiceAnalysis/ios_client

# Tạo Xcode project
xcodebuild -project VoiceAnalysis.xcodeproj
```

**HOẶC** tạo project mới trong Xcode:

1. Mở Xcode
2. File → New → Project
3. Chọn **iOS** → **App**
4. Điền thông tin:
   - Product Name: `VoiceAnalysis`
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Organization Identifier: `com.yourcompany` (tùy ý)
5. Lưu vào thư mục `ios_client`
6. **Copy tất cả file** từ thư mục hiện tại vào project:
   - Kéo thả folder `Models/`, `Services/`, `ViewModels/`, `Views/` vào project
   - Thay thế file `VoiceAnalysisApp.swift`
   - Copy nội dung `Info.plist` vào Info của project

---

## 🏃 BƯỚC 3: Chạy Ứng Dụng

### 3.1. Chọn Target Device

**Cách 1: iPhone Simulator (Dễ nhất)**
1. Trong Xcode, góc trên bên trái, click vào dropdown target
2. Chọn **iPhone 15 Pro** (hoặc model khác)
3. Click nút **Run** (▶️) hoặc nhấn `Cmd + R`
4. Đợi Simulator khởi động và app được cài đặt

⚠️ **Lưu ý:** Simulator vẫn cần server chạy trên `192.168.20.100:8000`

**Cách 2: iPhone Thật (Nên dùng để test thực tế)**
1. Kết nối iPhone với Mac bằng cable
2. Mở nút **Trust This Computer** trên iPhone
3. Trong Xcode Settings → Accounts, thêm Apple ID của bạn
4. Trong project navigator, chọn target **VoiceAnalysis**
5. Tab **Signing & Capabilities**:
   - Team: Chọn Personal Team (Apple ID của bạn)
   - Bundle Identifier: Đổi thành unique name (vd: `com.yourname.voiceanalysis`)
6. Chọn iPhone trong target dropdown
7. Click **Run** (▶️)

**Lần đầu chạy trên iPhone:**
- iPhone sẽ hiện cảnh báo "Untrusted Developer"
- Vào Settings → General → VPN & Device Management
- Trust developer certificate của bạn

### 3.2. Kiểm Tra Kết Nối

**Test server có hoạt động không:**

Trên iPhone, mở Safari và truy cập:
```
http://192.168.20.100:8000/docs
```

✅ Nếu hiện trang FastAPI docs → Server OK!
❌ Nếu không kết nối được → Xem phần Troubleshooting

---

## 🧪 BƯỚC 4: Test Các Tính Năng

### 4.1. Chuẩn Bị File Test

Copy các file test audio vào iPhone:
1. **Qua AirDrop:** Gửi `test_60s.wav` từ Windows sang iPhone
2. **Qua iTunes/Finder:** Sync file vào iPhone
3. **Qua iCloud Drive:** Upload file lên iCloud, tải về iPhone

### 4.2. Test Flow

1. **Mở App** → Hiện header "🎙️ Voice Analysis System"
2. **Click "Choose Audio File"** → Document picker mở ra
3. **Chọn file** `test_60s.wav` → Tên file hiển thị
4. **Click "Analyze"** → Button disabled, hiện "Đang phân tích..."
5. **Đợi kết quả** (5-10 giây)
6. **Xem kết quả**:
   - 📄 File info
   - 📊 Statistics với emoji
   - 🔍 First 20 segments
7. **Click "Clear"** → Xóa kết quả

### 4.3. Checklist Tính Năng

- [ ] F-C1: Document picker mở được
- [ ] F-C3: Tên file hiển thị sau khi chọn
- [ ] F-C4: Button "Analyze" kích hoạt khi có file
- [ ] F-C5: Upload file lên server thành công
- [ ] F-C6: Loading state hiển thị khi analyzing
- [ ] F-C7: Parse JSON response thành công
- [ ] F-C8: Kết quả hiển thị đầy đủ (stats + segments)
- [ ] F-C9: Error alert hiện khi có lỗi (test bằng cách tắt server)

---

## 🐛 TROUBLESHOOTING

### ❌ Lỗi "Cannot connect to server"

**Nguyên nhân & Giải pháp:**

1. **Server không chạy hoặc sai địa chỉ**
   ```bash
   # Kiểm tra server đang chạy
   curl http://192.168.20.100:8000/docs
   ```

2. **iPhone và Windows không cùng WiFi**
   - Kiểm tra iPhone: Settings → WiFi → Network name
   - Kiểm tra Windows: Control Panel → Network → WiFi name
   - Phải giống nhau!

3. **Windows Firewall chặn port 8000**
   ```powershell
   # Cho phép port 8000 qua firewall
   netsh advfirewall firewall add rule name="Python Server" dir=in action=allow protocol=TCP localport=8000
   ```

4. **Server chạy 127.0.0.1 thay vì 0.0.0.0**
   - Sửa `server/main.py`:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

### ❌ Lỗi "App Transport Security blocked"

Nếu iOS chặn HTTP connection:

1. Mở `Info.plist` trong Xcode
2. Thêm key:
   ```xml
   <key>NSAppTransportSecurity</key>
   <dict>
       <key>NSAllowsArbitraryLoads</key>
       <true/>
   </dict>
   ```

⚠️ Trong production nên dùng HTTPS!

### ❌ Lỗi Build "Code signing required"

1. Xcode → Settings → Accounts
2. Thêm Apple ID (free account cũng được)
3. Project → Signing & Capabilities
4. Chọn Team = Personal Team
5. Thay đổi Bundle Identifier thành unique name

### ❌ Lỗi "No devices found"

- Simulator: Install iOS Simulator trong Xcode → Settings → Components
- iPhone thật: 
  - Unlock iPhone
  - Trust computer khi popup hiện
  - Xcode → Window → Devices and Simulators → Check iPhone

### ❌ App crash khi chọn file

Kiểm tra `Info.plist` có quyền:
```xml
<key>NSMicrophoneUsageDescription</key>
<string>Để ghi âm và phân tích giọng nói</string>
```

---

## 📊 Kết Quả Mong Đợi

### Màn Hình Chính:
```
🎙️ Voice Analysis System

┌─────────────────────────┐
│ File Selection          │
│ [Choose Audio File]     │
│ test_60s.wav           │
└─────────────────────────┘

[Analyze]  [Clear]

✅ Sẵn sàng
```

### Sau Khi Analyze:
```
📄 File: test_60s.wav
📊 Total Segments: 1178

📈 STATISTICS:
🔊 VOICED    : 589 frames (50.00%)
💨 UNVOICED  : 294 frames (25.00%)
🔇 SILENCE   : 295 frames (25.00%)

🔍 FIRST 20 SEGMENTS:
0.000 | UNVOICED   | F0:   0.00 Hz | E: 0.2141
0.032 | UNVOICED   | F0:   0.00 Hz | E: 0.2609
...
```

---

## 🎯 Next Steps

### Thêm Tính Năng Recording (Tương tự Desktop):

1. Thêm AVFoundation framework
2. Request microphone permission
3. Implement AVAudioRecorder
4. Lưu file tạm và upload

### Deploy Lên App Store:

1. Tạo App Store Connect account
2. Configure provisioning profile
3. Archive build
4. Upload lên TestFlight
5. Submit for review

---

## 📞 Hỗ Trợ

### Log Debug trong Xcode:

```swift
// Thêm vào VoiceAnalysisService để debug
print("🌐 Request URL: \(url)")
print("📤 Sending file: \(fileName)")
print("📥 Response: \(httpResponse.statusCode)")
```

### Check Console trong Xcode:
- View → Debug Area → Activate Console (Cmd + Shift + Y)
- Xem log khi app chạy

### Test API bằng Terminal:

```bash
# Test từ Mac/iPhone network
curl -X POST http://192.168.20.100:8000/analyze/ \
  -F "file=@test_60s.wav"
```

---

## ✅ Checklist Hoàn Thành

- [ ] Server chạy trên Windows (0.0.0.0:8000)
- [ ] IP address đã cập nhật trong code (192.168.20.100)
- [ ] Project mở được trong Xcode
- [ ] App build thành công
- [ ] App chạy trên Simulator/iPhone
- [ ] Chọn file audio thành công
- [ ] Analyze và nhận kết quả đúng
- [ ] Error handling hoạt động

---

**Chúc bạn test thành công! 🎉**

Nếu gặp vấn đề, hãy check log trong Xcode Console và server log.
