# 🚀 QUICK START - Test iOS App

## TÓM TẮT NHANH

### Bước 1: Khởi động Server (Windows)
```powershell
cd E:\VoiceUnvoiceSystem\server
python main.py
```

✅ Server đang chạy: `http://192.168.20.100:8000`

### Bước 2: Trên Mac
1. Copy thư mục `ios_client` từ Windows sang Mac
2. Mở Xcode, tạo project mới (iOS App, SwiftUI)
3. Copy tất cả file code vào project
4. Chạy (Cmd + R)

### Bước 3: Test
1. Click "Choose Audio File"
2. Chọn file `test_60s.wav`
3. Click "Analyze"
4. Xem kết quả!

---

## THÔNG TIN QUAN TRỌNG

| Thông Tin | Giá Trị |
|-----------|---------|
| Server URL | `http://192.168.20.100:8000` |
| Windows IP | `192.168.20.100` |
| Port | `8000` |
| File đã cập nhật | `VoiceAnalysisService.swift` |

---

## YÊU CẦU

- ✅ Mac với Xcode 14+
- ✅ iPhone/Simulator với iOS 15+
- ✅ iPhone và Windows **cùng mạng WiFi**
- ✅ Server chạy trên Windows

---

## TEST NHANH SERVER

Từ iPhone Safari, mở:
```
http://192.168.20.100:8000/docs
```

Nếu thấy FastAPI docs → OK! 🎉

---

## TROUBLESHOOTING NHANH

### Không kết nối được server?

1. **Check WiFi:** iPhone và Windows cùng mạng
2. **Check Firewall:** 
   ```powershell
   netsh advfirewall firewall add rule name="Python Server" dir=in action=allow protocol=TCP localport=8000
   ```
3. **Restart server:** Ctrl+C rồi chạy lại

### Build error trong Xcode?

1. Xcode → Settings → Accounts → Thêm Apple ID
2. Project → Signing → Chọn Team
3. Đổi Bundle Identifier

---

Xem file `HUONG_DAN_TEST.md` để có hướng dẫn chi tiết đầy đủ!
