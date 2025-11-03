# Voice Analysis iOS Client

Ứng dụng iOS (Swift/SwiftUI) cho hệ thống phân tích Voiced/Unvoiced/Silence.

## Yêu cầu

- macOS (để chạy Xcode)
- Xcode 14+ 
- iOS 15.0+
- Swift 5.7+

## Cài đặt

### 1. Mở project trong Xcode

```bash
open ios_client/VoiceAnalysis.xcodeproj
```

### 2. Cấu hình Server URL (S-5)

Mở file `Services/VoiceAnalysisService.swift`:

```swift
private let baseURL = "http://127.0.0.1:8000"
```

**Lưu ý cho thiết bị thật**:
- Simulator có thể dùng `127.0.0.1` hoặc `localhost`
- Thiết bị thật cần sử dụng IP nội bộ của máy Mac (tìm bằng `ifconfig`)
- Ví dụ: `http://192.168.1.100:8000`

### 3. Cấu hình Info.plist (S-I4, S-I5)

File `Info.plist` đã được cấu hình:
- ✅ `NSAppTransportSecurity` - Cho phép HTTP (development)
- ✅ `NSMicrophoneUsageDescription` - Quyền ghi âm (nếu cần)

## Chạy Ứng dụng

### 1. Chạy Server trước

```bash
cd ../server
python main.py
```

### 2. Chạy ứng dụng iOS

- Chọn target device (Simulator hoặc thiết bị thật)
- Click nút Run (▶️) hoặc nhấn `Cmd + R`

## Kiến trúc & Tech Stack

### Tech Stack (Theo S-I)

- **Swift**: Ngôn ngữ chính
- **SwiftUI**: UI framework
- **URLSession**: Networking (native)
- **Codable**: JSON parsing
- **ObservableObject**: State management

### Cấu trúc Code

```
VoiceAnalysis/
├── Models/
│   └── AnalysisResponse.swift      # Data models (S-I2)
├── Services/
│   └── VoiceAnalysisService.swift  # API service (S-I1)
├── ViewModels/
│   └── ContentViewModel.swift      # ViewModel (S-I3)
├── Views/
│   └── ContentView.swift           # UI layer
├── VoiceAnalysisApp.swift          # App entry point
└── Info.plist                      # Configuration (S-I4, S-I5)
```

## Tuân thủ Tiêu chuẩn

### General (S-1 đến S-5)
- ✅ S-1: URLSession tự động bất đồng bộ
- ✅ S-2: Result type cho error handling
- ✅ S-3: UI feedback rõ ràng
- ✅ S-4: Codable struct cho JSON parsing
- ✅ S-5: Server URL trong config

### iOS Specific (S-I1 đến S-I5)
- ✅ S-I1: URLSession.shared.dataTask (bất đồng bộ)
- ✅ S-I2: Codable protocol cho AnalysisResponse
- ✅ S-I3: ObservableObject cho ViewModel
- ✅ S-I4: NSAppTransportSecurity trong Info.plist
- ✅ S-I5: NSMicrophoneUsageDescription trong Info.plist

### Functional Requirements (F-C1 đến F-C9)
- ✅ F-C1: UIDocumentPicker để chọn file
- ✅ F-C3: Hiển thị tên file
- ✅ F-C4: Nút Analyze
- ✅ F-C5: Gửi file đến API
- ✅ F-C6: Loading state và disable button
- ✅ F-C7: Parse JSON với Codable
- ✅ F-C8: Hiển thị kết quả
- ✅ F-C9: Error alert rõ ràng

## Hướng dẫn Sử dụng (NF-3)

1. **Chọn file**: Nhấn "Choose Audio File"
2. **Phân tích**: Nhấn "Analyze"
3. **Xem kết quả**: Kết quả hiển thị trong card "Analysis Results"

## Troubleshooting

### Lỗi kết nối server

**Trên Simulator**:
- Kiểm tra server đang chạy
- Có thể dùng `localhost` hoặc `127.0.0.1`

**Trên thiết bị thật**:
1. Mac và iPhone phải cùng mạng WiFi
2. Tìm IP của Mac:
   ```bash
   ifconfig | grep "inet "
   ```
3. Cập nhật `baseURL` trong `VoiceAnalysisService.swift`:
   ```swift
   private let baseURL = "http://192.168.1.100:8000"  // Thay bằng IP của bạn
   ```
4. Kiểm tra firewall không chặn port 8000

### Lỗi "App Transport Security"

Nếu không thể kết nối qua HTTP:
- Kiểm tra `Info.plist` có `NSAppTransportSecurity` chưa
- Trong production nên dùng HTTPS thay vì tắt ATS

### Build cho thiết bị thật

1. Kết nối iPhone với Mac
2. Trust developer certificate trong Settings > General > Device Management
3. Select iPhone làm target
4. Run (Cmd + R)

## Production Deployment

### App Store

1. Tắt `NSAllowsArbitraryLoads` trong Info.plist
2. Sử dụng HTTPS cho server
3. Configure proper bundle identifier
4. Code signing & provisioning profile
5. Archive & upload to App Store Connect

### TestFlight

Tương tự App Store nhưng không cần review để test nội bộ.

## Native Alternative: Alamofire

Nếu muốn sử dụng Alamofire thay vì URLSession:

```swift
// Trong Package Dependencies, thêm:
// https://github.com/Alamofire/Alamofire

import Alamofire

AF.upload(multipartFormData: { multipartFormData in
    multipartFormData.append(fileURL, withName: "file")
}, to: "\(baseURL)/analyze/")
.responseDecodable(of: AnalysisResponse.self) { response in
    // Handle response
}
```
