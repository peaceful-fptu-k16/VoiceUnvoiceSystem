"""
Script để tạo file âm thanh test
"""

import numpy as np
from scipy.io import wavfile

def create_test_audio(filename="test_audio.wav", duration=3, sample_rate=16000):
    """
    Tạo file âm thanh test với các đặc tính:
    - 1 giây silence (đầu)
    - 2 giây voiced (sin wave 440 Hz)
    - 1 giây unvoiced (white noise)
    - 1 giây silence (cuối)
    """
    print(f"🎵 Đang tạo file test: {filename}")
    
    # Silence (1 giây)
    silence1 = np.zeros(sample_rate * 1)
    
    # Voiced - Sin wave 440 Hz (2 giây)
    t = np.linspace(0, 2, sample_rate * 2)
    voiced = 0.3 * np.sin(2 * np.pi * 440 * t)
    
    # Unvoiced - White noise (1 giây)
    unvoiced = 0.1 * np.random.randn(sample_rate * 1)
    
    # Silence (1 giây)
    silence2 = np.zeros(sample_rate * 1)
    
    # Ghép tất cả
    audio = np.concatenate([silence1, voiced, unvoiced, silence2])
    
    # Normalize và convert sang int16
    audio = np.int16(audio * 32767)
    
    # Lưu file
    wavfile.write(filename, sample_rate, audio)
    
    print(f"✅ Đã tạo {filename}")
    print(f"   - Thời lượng: {len(audio) / sample_rate:.1f} giây")
    print(f"   - Sample rate: {sample_rate} Hz")
    print(f"   - Cấu trúc: 1s silence + 2s voiced + 1s unvoiced + 1s silence")

def create_long_test_audio(filename="test_60s.wav", duration=60, sample_rate=16000):
    """
    Tạo file âm thanh dài để test performance (NF-1)
    """
    print(f"🎵 Đang tạo file test dài: {filename}")
    
    # Tạo audio ngẫu nhiên
    audio = 0.3 * np.random.randn(sample_rate * duration)
    
    # Convert sang int16
    audio = np.int16(audio * 32767)
    
    # Lưu file
    wavfile.write(filename, sample_rate, audio)
    
    print(f"✅ Đã tạo {filename}")
    print(f"   - Thời lượng: {duration} giây")
    print(f"   - Sample rate: {sample_rate} Hz")

if __name__ == "__main__":
    # Kiểm tra scipy có sẵn không
    try:
        # Tạo file test ngắn
        create_test_audio("test_audio.wav", duration=5)
        
        # Tạo file test dài (cho performance test)
        create_long_test_audio("test_60s.wav", duration=60)
        
        print("\n✅ Hoàn thành! Sử dụng các file này để test hệ thống.")
        
    except ImportError:
        print("❌ Lỗi: Cần cài đặt scipy")
        print("   Chạy: pip install scipy")
