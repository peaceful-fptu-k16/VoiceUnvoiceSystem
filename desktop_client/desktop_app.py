"""
Desktop Application cho hệ thống phân tích Voiced/Unvoiced/Silence
Tuân thủ các tiêu chuẩn S-D1, S-D2 và tất cả yêu cầu Client
Bao gồm tính năng ghi âm từ microphone (F-C2)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import requests
import threading
import json
from typing import Optional, Dict, Any
import os
import wave
import pyaudio
import tempfile
from datetime import datetime


class Config:
    """Lớp cấu hình - Tuân thủ S-5: Không hard-code địa chỉ server"""
    API_BASE_URL = "http://127.0.0.1:8000"
    ANALYZE_ENDPOINT = f"{API_BASE_URL}/analyze/"
    SUPPORTED_FORMATS = [
        ("Audio Files", "*.wav *.mp3 *.m4a *.flac *.ogg"),
        ("WAV Files", "*.wav"),
        ("MP3 Files", "*.mp3"),
        ("M4A Files", "*.m4a"),
        ("All Files", "*.*")
    ]
    
    # Cấu hình ghi âm
    RECORD_SAMPLE_RATE = 16000  # Hz
    RECORD_CHANNELS = 1  # Mono
    RECORD_CHUNK = 1024  # Buffer size
    RECORD_FORMAT = pyaudio.paInt16  # 16-bit audio


class AnalysisResponse:
    """
    Model cho response từ API - Tuân thủ S-4: Sử dụng Model để parse JSON
    """
    def __init__(self, data: Dict[str, Any]):
        self.filename = data.get("filename", "")
        self.total_segments = data.get("total_segments", 0)
        self.segments = data.get("segments", [])
    
    def get_statistics(self) -> Dict[str, int]:
        """Tính thống kê các loại frame"""
        stats = {"VOICED": 0, "UNVOICED": 0, "SILENCE": 0}
        for segment in self.segments:
            frame_type = segment.get("type", "")
            if frame_type in stats:
                stats[frame_type] += 1
        return stats


class VoiceAnalysisApp:
    """
    Ứng dụng Desktop chính
    Tuân thủ tất cả yêu cầu F-C1 đến F-C9
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Voice Analysis System - Desktop Client")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        
        # Biến trạng thái
        self.selected_file: Optional[str] = None
        self.is_analyzing: bool = False
        self.is_recording: bool = False
        
        # PyAudio instance cho ghi âm
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        
        # Tạo giao diện
        self._create_ui()
        
        # Cleanup khi đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _create_ui(self):
        """Tạo giao diện người dùng - Tuân thủ NF-3: Đơn giản, trực quan"""
        
        # Background màu cho root
        self.root.configure(bg='#ecf0f1')
        
        # Frame chính với background
        main_frame = tk.Frame(self.root, bg='#ecf0f1', padx=25, pady=25)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # ========== HEADER ==========
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=90)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.grid_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="🎙️ Voice Analysis System",
            font=("Segoe UI", 26, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        header_label.pack(expand=True)
        
        # ========== RECORDING CARD ==========
        record_card = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        record_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        record_card.columnconfigure(0, weight=1)
        
        # Recording title bar
        record_title_bar = tk.Frame(record_card, bg='#e74c3c', height=40)
        record_title_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        record_title_bar.grid_propagate(False)
        
        record_title = tk.Label(
            record_title_bar,
            text="🎤  MICROPHONE RECORDING",
            font=("Segoe UI", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            anchor='w',
            padx=15
        )
        record_title.pack(fill=tk.BOTH, expand=True)
        
        # Recording controls frame
        record_controls = tk.Frame(record_card, bg='white', pady=20, padx=20)
        record_controls.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Record button với màu sắc và width cố định
        self.record_button = tk.Button(
            record_controls,
            text="⚫ START RECORDING",
            command=self._toggle_recording,
            font=("Segoe UI", 11, "bold"),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            relief=tk.FLAT,
            width=25,
            pady=12,
            cursor='hand2',
            borderwidth=0
        )
        self.record_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Recording time với style
        self.recording_time_label = tk.Label(
            record_controls,
            text="⏱️ 00:00",
            font=("Segoe UI", 14, "bold"),
            bg='white',
            fg='#95a5a6'
        )
        self.recording_time_label.pack(side=tk.LEFT)
        
        # ========== FILE SELECTION CARD ==========
        file_card = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        file_card.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_card.columnconfigure(0, weight=1)
        
        # File selection title bar
        file_title_bar = tk.Frame(file_card, bg='#3498db', height=40)
        file_title_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        file_title_bar.grid_propagate(False)
        
        file_title = tk.Label(
            file_title_bar,
            text="📁  FILE SELECTION",
            font=("Segoe UI", 12, "bold"),
            bg='#3498db',
            fg='white',
            anchor='w',
            padx=15
        )
        file_title.pack(fill=tk.BOTH, expand=True)
        
        # File controls frame
        file_controls = tk.Frame(file_card, bg='white', pady=20, padx=20)
        file_controls.grid(row=1, column=0, sticky=(tk.W, tk.E))
        file_controls.columnconfigure(1, weight=1)
        
        # Select button với màu xanh và width cố định
        select_button = tk.Button(
            file_controls,
            text="📂  BROWSE FILES",
            command=self._select_file,
            font=("Segoe UI", 11, "bold"),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief=tk.FLAT,
            width=25,
            pady=12,
            cursor='hand2',
            borderwidth=0
        )
        select_button.grid(row=0, column=0, padx=(0, 15))
        
        # File path label với background
        self.file_label = tk.Label(
            file_controls,
            text="No file selected",
            font=("Segoe UI", 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            anchor='w',
            padx=15,
            pady=10,
            relief=tk.FLAT
        )
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # ========== ACTION BUTTONS ==========
        action_frame = tk.Frame(main_frame, bg='#ecf0f1')
        action_frame.grid(row=3, column=0, pady=(0, 15))
        
        # Analyze button với màu xanh lá và width cố định
        self.analyze_button = tk.Button(
            action_frame,
            text="🔍  ANALYZE AUDIO",
            command=self._start_analysis,
            font=("Segoe UI", 12, "bold"),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            relief=tk.FLAT,
            width=22,
            pady=15,
            cursor='hand2',
            borderwidth=0,
            state=tk.DISABLED
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button với width cố định
        self.clear_button = tk.Button(
            action_frame,
            text="🗑️  CLEAR",
            command=self._clear_results,
            font=("Segoe UI", 12, "bold"),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            relief=tk.FLAT,
            width=15,
            pady=15,
            cursor='hand2',
            borderwidth=0
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status label với icon
        self.status_label = tk.Label(
            main_frame,
            text="✅  Ready to analyze",
            font=("Segoe UI", 10, "bold"),
            bg='#ecf0f1',
            fg='#27ae60'
        )
        self.status_label.grid(row=3, column=0, pady=(0, 10), sticky=tk.E)
        
        # ========== RESULTS CARD ==========
        results_card = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        results_card.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_card.columnconfigure(0, weight=1)
        results_card.rowconfigure(1, weight=1)
        
        # Results title bar
        results_title_bar = tk.Frame(results_card, bg='#16a085', height=40)
        results_title_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        results_title_bar.grid_propagate(False)
        
        results_title = tk.Label(
            results_title_bar,
            text="📊  ANALYSIS RESULTS",
            font=("Segoe UI", 12, "bold"),
            bg='#16a085',
            fg='white',
            anchor='w',
            padx=15
        )
        results_title.pack(fill=tk.BOTH, expand=True)
        
        # Results text với scrollbar
        results_container = tk.Frame(results_card, bg='white', padx=0, pady=0)
        results_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_container.columnconfigure(0, weight=1)
        results_container.rowconfigure(1, weight=1)
        
        # Statistics Frame
        stats_frame = tk.Frame(results_container, bg='#fdfefe', padx=15, pady=10)
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="No analysis results yet",
            font=("Segoe UI", 10),
            bg='#fdfefe',
            fg='#7f8c8d',
            justify=tk.LEFT,
            anchor='w'
        )
        self.stats_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Separator
        separator = tk.Frame(results_container, bg='#bdc3c7', height=1)
        separator.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Table Frame với Treeview
        table_frame = tk.Frame(results_container, bg='white', padx=15, pady=15)
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview với scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Style cho Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview",
                       background="#fdfefe",
                       foreground="#2c3e50",
                       fieldbackground="#fdfefe",
                       font=("Consolas", 9),
                       rowheight=25)
        style.configure("Custom.Treeview.Heading",
                       background="#3498db",
                       foreground="white",
                       font=("Segoe UI", 10, "bold"),
                       relief=tk.FLAT)
        style.map("Custom.Treeview.Heading",
                 background=[('active', '#2980b9')])
        style.map("Custom.Treeview",
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
        self.results_table = ttk.Treeview(
            table_frame,
            columns=("no", "time", "type", "f0", "energy"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            style="Custom.Treeview",
            height=20
        )
        
        # Configure columns
        self.results_table.heading("no", text="No.")
        self.results_table.heading("time", text="Time (s)")
        self.results_table.heading("type", text="Type")
        self.results_table.heading("f0", text="F0 (Hz)")
        self.results_table.heading("energy", text="Energy")
        
        self.results_table.column("no", width=60, anchor=tk.CENTER)
        self.results_table.column("time", width=100, anchor=tk.E)
        self.results_table.column("type", width=150, anchor=tk.CENTER)
        self.results_table.column("f0", width=120, anchor=tk.E)
        self.results_table.column("energy", width=120, anchor=tk.E)
        
        # Configure scrollbars
        tree_scroll_y.config(command=self.results_table.yview)
        tree_scroll_x.config(command=self.results_table.xview)
        
        # Grid layout
        self.results_table.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#34495e', height=35)
        footer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        footer_frame.grid_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text=f"🌐 Server: {Config.API_BASE_URL}  |  © 2025 Voice Analysis System",
            font=("Segoe UI", 9),
            bg='#34495e',
            fg='#bdc3c7'
        )
        footer_label.pack(expand=True)
    
    def _select_file(self):
        """Xử lý chọn file - F-C1, F-C3"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=Config.SUPPORTED_FORMATS
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(
                text=os.path.basename(filename),
                foreground="#2c3e50",
                font=("Segoe UI", 10, "bold")
            )
            self.analyze_button.config(state=tk.NORMAL, bg='#27ae60')
            self._log_message(f"✅ Selected file: {os.path.basename(filename)}")
    
    def _toggle_recording(self):
        """Bật/tắt ghi âm - F-C2"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Bắt đầu ghi âm từ microphone - F-C2"""
        try:
            self.is_recording = True
            self.frames = []
            
            # Mở stream
            self.stream = self.audio.open(
                format=Config.RECORD_FORMAT,
                channels=Config.RECORD_CHANNELS,
                rate=Config.RECORD_SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.RECORD_CHUNK
            )
            
            # Cập nhật UI
            self.record_button.config(
                text="⏹️  STOP RECORDING",
                bg='#c0392b'
            )
            self.recording_time_label.config(fg='#e74c3c')
            self.analyze_button.config(state=tk.DISABLED, bg='#95a5a6')
            self._update_status("🎤 Recording...", "#e74c3c")
            
            # Bắt đầu thread ghi âm
            self.recording_start_time = datetime.now()
            recording_thread = threading.Thread(target=self._record_audio)
            recording_thread.daemon = True
            recording_thread.start()
            
            # Cập nhật thời gian ghi âm
            self._update_recording_time()
            
        except Exception as e:
            self.is_recording = False
            messagebox.showerror("Recording Error", f"Không thể ghi âm: {str(e)}\n\nKiểm tra microphone đã được kết nối!")
            self._update_status("✅  Ready to analyze", "#27ae60")
    
    def _record_audio(self):
        """Thread ghi âm - đọc dữ liệu từ stream"""
        try:
            while self.is_recording:
                data = self.stream.read(Config.RECORD_CHUNK, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            print(f"Recording error: {e}")
    
    def _update_recording_time(self):
        """Cập nhật thời gian ghi âm"""
        if self.is_recording:
            elapsed = (datetime.now() - self.recording_start_time).total_seconds()
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            self.recording_time_label.config(text=f"⏱️ {mins:02d}:{secs:02d}")
            self.root.after(100, self._update_recording_time)
        else:
            self.recording_time_label.config(text="⏱️ 00:00", fg='#95a5a6')
    
    def _stop_recording(self):
        """Dừng ghi âm và lưu file - F-C2"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        # Dừng stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Lưu file WAV
        try:
            # Tạo file tạm
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav",
                prefix="recording_"
            )
            temp_filename = temp_file.name
            temp_file.close()
            
            # Ghi dữ liệu
            wf = wave.open(temp_filename, 'wb')
            wf.setnchannels(Config.RECORD_CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(Config.RECORD_FORMAT))
            wf.setframerate(Config.RECORD_SAMPLE_RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            
            # Cập nhật file đã chọn
            self.selected_file = temp_filename
            duration = len(self.frames) * Config.RECORD_CHUNK / Config.RECORD_SAMPLE_RATE
            
            self.file_label.config(
                text=f"🎤 Recorded audio ({duration:.1f}s)",
                foreground="#e74c3c",
                font=("Segoe UI", 10, "bold")
            )
            
            # Kích hoạt nút analyze
            self.analyze_button.config(state=tk.NORMAL, bg='#27ae60')
            self.record_button.config(
                text="⚫  START RECORDING",
                bg='#e74c3c'
            )
            
            self._update_status(f"✅ Recording completed: {duration:.1f}s", "#27ae60")
            self._log_message(f"✅ Recorded {duration:.1f} seconds of audio")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Không thể lưu file: {str(e)}")
            self._update_status("Error saving recording", "red")
    
    def _start_analysis(self):
        """
        Bắt đầu phân tích - F-C4, F-C5
        Tuân thủ S-1: Chạy trên background thread
        """
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        if self.is_analyzing:
            return
        
        # Vô hiệu hóa nút để tránh gửi nhiều lần - F-C6
        self.is_analyzing = True
        self.analyze_button.config(state=tk.DISABLED, bg='#95a5a6')
        self._update_status("⏳ Analyzing...", "#f39c12")
        
        # Chạy trên background thread - S-D1
        thread = threading.Thread(target=self._perform_analysis)
        thread.daemon = True
        thread.start()
    
    def _perform_analysis(self):
        """
        Thực hiện gọi API - Chạy trên background thread
        Tuân thủ S-2: Error handling với try-catch
        """
        try:
            # Chuẩn bị file để upload - F-C5
            with open(self.selected_file, 'rb') as f:
                files = {'file': (os.path.basename(self.selected_file), f)}
                
                # Gọi API - F-C5
                response = requests.post(
                    Config.ANALYZE_ENDPOINT,
                    files=files,
                    timeout=60  # Timeout 60 giây
                )
            
            # Kiểm tra response
            if response.status_code == 200:
                # Parse JSON theo hợp đồng - F-C7, S-4
                data = response.json()
                analysis_result = AnalysisResponse(data)
                
                # Cập nhật UI - S-D2: Sử dụng root.after để an toàn với Tkinter
                self.root.after(0, self._display_results, analysis_result)
            else:
                # Xử lý lỗi - F-C9
                error_msg = f"Server error ({response.status_code})"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', {}).get('message', '')}"
                except:
                    pass
                
                self.root.after(0, self._show_error, error_msg)
        
        except requests.exceptions.ConnectionError:
            # Lỗi kết nối - F-C9
            self.root.after(
                0,
                self._show_error,
                f"Cannot connect to server at {Config.API_BASE_URL}"
            )
        
        except requests.exceptions.Timeout:
            # Timeout
            self.root.after(0, self._show_error, "Request timeout (>60s)")
        
        except Exception as e:
            # Lỗi khác - S-2
            self.root.after(0, self._show_error, f"Error: {str(e)}")
        
        finally:
            # Kích hoạt lại nút - F-C6
            self.root.after(0, self._enable_analyze_button)
    
    def _display_results(self, result: AnalysisResponse):
        """Hiển thị kết quả - F-C8 - Hiển thị toàn bộ trong table"""
        # Clear existing data
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        
        # Thống kê tổng quan
        stats = result.get_statistics()
        total = result.total_segments
        
        # Update statistics label
        stats_text = f"📄 File: {result.filename}  |  📊 Total Segments: {total}\n\n"
        
        for frame_type, count in stats.items():
            percentage = (count / total * 100) if total > 0 else 0
            emoji = "🔊" if frame_type == "VOICED" else "💨" if frame_type == "UNVOICED" else "🔇"
            bar_length = int(percentage / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            stats_text += f"{emoji} {frame_type:12s}: {count:6d} frames ({percentage:6.2f}%)  [{bar}]\n"
        
        self.stats_label.config(text=stats_text)
        
        # Populate table với TẤT CẢ segments
        for i, segment in enumerate(result.segments, 1):
            time_val = segment.get('time', 0)
            seg_type = segment.get('type', '')
            f0 = segment.get('f0', 0)
            energy = segment.get('energy', 0)
            
            # Icon cho type
            if seg_type == "VOICED":
                type_display = f"🔊 {seg_type}"
            elif seg_type == "UNVOICED":
                type_display = f"💨 {seg_type}"
            else:
                type_display = f"🔇 {seg_type}"
            
            # Thêm màu cho từng loại
            tag = seg_type.lower()
            self.results_table.insert(
                "",
                tk.END,
                values=(i, f"{time_val:.3f}", type_display, f"{f0:.2f}", f"{energy:.6f}"),
                tags=(tag,)
            )
        
        # Configure row colors
        self.results_table.tag_configure('voiced', background='#d5f4e6')
        self.results_table.tag_configure('unvoiced', background='#fdebd0')
        self.results_table.tag_configure('silence', background='#f0f0f0')
        
        self._update_status("✅  Analysis completed successfully!", "#27ae60")
    
    def _show_error(self, error_message: str):
        """Hiển thị lỗi - F-C9"""
        self._update_status(f"❌ Error: {error_message}", "#e74c3c")
        messagebox.showerror("Analysis Error", error_message)
    
    def _enable_analyze_button(self):
        """Kích hoạt lại nút Analyze"""
        self.is_analyzing = False
        if self.selected_file:
            self.analyze_button.config(state=tk.NORMAL, bg='#27ae60')
    
    def _clear_results(self):
        """Xóa kết quả hiển thị"""
        # Clear table
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        # Clear stats
        self.stats_label.config(text="No analysis results yet")
        self._update_status("✅  Ready to analyze", "#27ae60")
    
    def _update_status(self, message: str, color: str):
        """Cập nhật trạng thái - S-3: UI Feedback"""
        self.status_label.config(text=message, foreground=color)
    
    def _log_message(self, message: str):
        """Ghi log vào stats label"""
        current = self.stats_label.cget("text")
        if "No analysis results yet" in current:
            self.stats_label.config(text=message)
        else:
            self.stats_label.config(text=current + "\n" + message)
    
    def _on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        # Dừng ghi âm nếu đang ghi
        if self.is_recording:
            self._stop_recording()
        
        # Đóng PyAudio
        if hasattr(self, 'audio'):
            self.audio.terminate()
        
        # Xóa file tạm nếu có
        if self.selected_file and self.selected_file.startswith(tempfile.gettempdir()):
            try:
                os.unlink(self.selected_file)
            except:
                pass
        
        self.root.destroy()


def main():
    """Entry point của ứng dụng"""
    root = tk.Tk()
    app = VoiceAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
