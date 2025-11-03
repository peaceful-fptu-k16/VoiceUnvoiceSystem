# Voice Analysis Server

Backend API cho hệ thống phân tích Voiced/Unvoiced/Silence.

## Cài đặt

### 1. Cài đặt Python (3.8 trở lên)

### 2. Tạo môi trường ảo (khuyến nghị)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

## Chạy Server

### Development (với auto-reload)

```powershell
python main.py
```

Hoặc:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production (với nhiều workers - NF-4)

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Kiểm thử API

### 1. Kiểm tra server hoạt động

```powershell
curl http://localhost:8000/
```

### 2. Kiểm tra health

```powershell
curl http://localhost:8000/health/
```

### 3. Test phân tích file âm thanh

```powershell
curl -X POST "http://localhost:8000/analyze/" `
  -F "file=@test_audio.wav"
```

## API Documentation

Sau khi chạy server, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Cấu trúc Response (Hợp đồng F-S5)

```json
{
  "filename": "test.wav",
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
    }
  ]
}
```

## Định dạng File Hỗ trợ (F-S2)

- `.wav`
- `.mp3`
- `.m4a`
- `.flac`
- `.ogg`

## Mã Lỗi HTTP (F-S6)

- `200`: Thành công
- `400`: File không hợp lệ hoặc định dạng không được hỗ trợ
- `500`: Lỗi server khi xử lý

## Tuân thủ Tiêu chuẩn

- ✅ S-P1: Sử dụng `tempfile.NamedTemporaryFile`
- ✅ S-P2: Tách biệt logic (main.py vs analysis.py)
- ✅ S-P3: Quản lý thư viện bằng requirements.txt
- ✅ S-P4: Code tuân thủ PEP 8
- ✅ F-S1 đến F-S6: Tất cả yêu cầu chức năng server
- ✅ NF-4: Hỗ trợ đa workers
