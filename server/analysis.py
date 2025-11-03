"""
Mô-đun phân tích âm thanh - Chứa toàn bộ logic nghiệp vụ
Tuân thủ tiêu chuẩn S-P2: Tách biệt nghiệp vụ khỏi API logic
"""

import librosa
import numpy as np
from typing import List, Dict, Any


class AudioAnalyzer:
    """
    Lớp phân tích âm thanh theo tiêu chuẩn Voiced/Unvoiced/Silence
    
    Attributes:
        energy_threshold: Ngưỡng năng lượng để phân biệt SILENCE vs UNVOICED
        frame_length: Độ dài khung (samples)
        hop_length: Bước nhảy giữa các khung (samples)
    """
    
    def __init__(
        self,
        energy_threshold: float = 0.02,
        frame_length: int = 2048,
        hop_length: int = 512
    ):
        self.energy_threshold = energy_threshold
        self.frame_length = frame_length
        self.hop_length = hop_length
    
    def analyze(self, audio_path: str) -> Dict[str, Any]:
        """
        Phân tích file âm thanh và trả về kết quả theo hợp đồng F-S5
        
        Args:
            audio_path: Đường dẫn đến file âm thanh
            
        Returns:
            Dict chứa kết quả phân tích theo chuẩn JSON contract
            
        Raises:
            Exception: Nếu có lỗi trong quá trình phân tích
        """
        # Load file âm thanh
        y, sr = librosa.load(audio_path, sr=None)
        
        # Tính toán Pitch (F0) - Tần số cơ bản
        f0 = self._extract_f0(y, sr)
        
        # Tính toán Energy (RMS)
        energy = self._extract_energy(y)
        
        # Phân loại từng frame
        segments = self._classify_frames(f0, energy, sr)
        
        # Tạo response theo hợp đồng F-S5
        return {
            "filename": audio_path.split('/')[-1].split('\\')[-1],
            "total_segments": len(segments),
            "segments": segments
        }
    
    def _extract_f0(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Trích xuất tần số cơ bản (F0/Pitch) sử dụng librosa
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Array chứa giá trị F0 cho từng frame
        """
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz('C2'),  # ~65 Hz
            fmax=librosa.note_to_hz('C7'),  # ~2093 Hz
            sr=sr,
            frame_length=self.frame_length,
            hop_length=self.hop_length
        )
        
        # Thay thế NaN bằng 0
        f0 = np.nan_to_num(f0, nan=0.0)
        
        return f0
    
    def _extract_energy(self, y: np.ndarray) -> np.ndarray:
        """
        Trích xuất năng lượng (RMS - Root Mean Square)
        
        Args:
            y: Audio time series
            
        Returns:
            Array chứa giá trị năng lượng cho từng frame
        """
        rms = librosa.feature.rms(
            y=y,
            frame_length=self.frame_length,
            hop_length=self.hop_length
        )[0]
        
        return rms
    
    def _classify_frames(
        self,
        f0: np.ndarray,
        energy: np.ndarray,
        sr: int
    ) -> List[Dict[str, Any]]:
        """
        Phân loại từng frame theo quy tắc F-S4:
        - VOICED: Có F0 (dây thanh âm rung)
        - UNVOICED: Không có F0 NHƯNG có năng lượng > ngưỡng
        - SILENCE: Không có F0 và năng lượng thấp
        
        Args:
            f0: Array tần số cơ bản
            energy: Array năng lượng
            sr: Sample rate
            
        Returns:
            List các segment theo hợp đồng F-S5
        """
        segments = []
        
        # Đảm bảo cả hai array có cùng độ dài
        min_length = min(len(f0), len(energy))
        
        for i in range(min_length):
            # Tính thời gian của frame (giây)
            time = librosa.frames_to_time(
                i,
                sr=sr,
                hop_length=self.hop_length
            )
            
            current_f0 = float(f0[i])
            current_energy = float(energy[i])
            
            # Phân loại theo quy tắc F-S4
            if current_f0 > 0:
                frame_type = "VOICED"
            elif current_energy > self.energy_threshold:
                frame_type = "UNVOICED"
            else:
                frame_type = "SILENCE"
            
            segments.append({
                "time": round(time, 3),
                "type": frame_type,
                "f0": round(current_f0, 2),
                "energy": round(current_energy, 4)
            })
        
        return segments


def analyze_audio_file(file_path: str) -> Dict[str, Any]:
    """
    Hàm tiện ích để phân tích file âm thanh
    
    Args:
        file_path: Đường dẫn đến file âm thanh
        
    Returns:
        Dict kết quả phân tích
    """
    analyzer = AudioAnalyzer()
    return analyzer.analyze(file_path)
