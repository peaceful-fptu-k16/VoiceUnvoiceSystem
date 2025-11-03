"""
API Server cho hệ thống phân tích Voiced/Unvoiced/Silence
Tuân thủ tiêu chuẩn S-P2: main.py chỉ chứa logic API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import Dict, Any
import logging

from analysis import analyze_audio_file

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo FastAPI app
app = FastAPI(
    title="Voice Analysis API",
    description="API phân tích âm thanh thành Voiced/Unvoiced/Silence",
    version="1.0.0"
)

# Cấu hình CORS để cho phép client từ các domain khác truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Danh sách định dạng file được hỗ trợ (F-S2)
SUPPORTED_FORMATS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}


@app.get("/")
async def root():
    """Endpoint kiểm tra server hoạt động"""
    return {
        "message": "Voice Analysis API is running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze/",
            "health": "/health/"
        }
    }


@app.get("/health/")
async def health_check():
    """Endpoint kiểm tra sức khỏe server (Health check)"""
    return {"status": "healthy"}


@app.post("/analyze/")
async def analyze_audio(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint chính để phân tích file âm thanh (F-S1)
    
    Args:
        file: File âm thanh được upload qua multipart/form-data
        
    Returns:
        JSONResponse chứa kết quả phân tích theo hợp đồng F-S5
        
    Raises:
        HTTPException: 400 nếu file không hợp lệ, 500 nếu lỗi xử lý
    """
    logger.info(f"Received file: {file.filename}")
    
    # Kiểm tra định dạng file (F-S2)
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in SUPPORTED_FORMATS:
        logger.warning(f"Unsupported format: {file_ext}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Unsupported file format",
                "message": f"File format {file_ext} is not supported. "
                          f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            }
        )
    
    # Sử dụng tempfile để xử lý file an toàn (F-S3, S-P1)
    temp_file = None
    try:
        # Tạo file tạm với suffix giống file gốc
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_ext
        )
        
        # Ghi nội dung file upload vào file tạm
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        logger.info(f"Processing file: {temp_file.name}")
        
        # Phân tích file âm thanh (F-S4)
        result = analyze_audio_file(temp_file.name)
        
        logger.info(
            f"Analysis completed: {result['total_segments']} segments"
        )
        
        # Trả về kết quả theo hợp đồng F-S5
        return JSONResponse(
            content=result,
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        
        # Trả về lỗi server (F-S6)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": f"Failed to process audio file: {str(e)}"
            }
        )
        
    finally:
        # Đảm bảo file tạm được xóa (S-P1)
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
                logger.info(f"Cleaned up temp file: {temp_file.name}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {str(e)}")


@app.get("/stats/")
async def get_stats():
    """Endpoint thống kê (tùy chọn)"""
    return {
        "supported_formats": list(SUPPORTED_FORMATS),
        "max_file_size": "100MB (configurable)",
        "frame_classification": ["VOICED", "UNVOICED", "SILENCE"]
    }


if __name__ == "__main__":
    import uvicorn
    
    # Chạy server với cấu hình phù hợp NF-4
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Tắt trong production
        workers=1  # Tăng lên 4-8 trong production (NF-4)
    )
