# Kiến trúc Hệ thống - Chi tiết

## 1. Tổng quan Luồng dữ liệu

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER DEVICES                             │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │   Desktop   │    │   Android   │    │     iOS     │       │
│  │  (Tkinter)  │    │  (Kotlin)   │    │   (Swift)   │       │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘       │
│         │                  │                   │               │
└─────────┼──────────────────┼───────────────────┼───────────────┘
          │                  │                   │
          │   1. Upload      │                   │
          │   audio file     │                   │
          │   (multipart)    │                   │
          │                  │                   │
          └──────────────────┴───────────────────┘
                             │
                             ▼
          ┌──────────────────────────────────────┐
          │         NETWORK LAYER                │
          │   HTTP POST /analyze/                │
          │   Content-Type: multipart/form-data  │
          └──────────────────┬───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVER (Backend)                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Application                   │  │
│  │                                                          │  │
│  │  main.py                                                │  │
│  │  ┌────────────────────────────────────────────────┐    │  │
│  │  │  POST /analyze/                                │    │  │
│  │  │  1. Receive multipart file                     │    │  │
│  │  │  2. Save to tempfile                           │    │  │
│  │  │  3. Call analysis.py                           │    │  │
│  │  │  4. Return JSON response                       │    │  │
│  │  └───────────────────┬────────────────────────────┘    │  │
│  │                      │                                  │  │
│  │                      ▼                                  │  │
│  │  analysis.py                                           │  │
│  │  ┌────────────────────────────────────────────────┐    │  │
│  │  │  AudioAnalyzer                                 │    │  │
│  │  │  ├─ Load audio (librosa.load)                  │    │  │
│  │  │  ├─ Extract F0 (librosa.pyin)                  │    │  │
│  │  │  ├─ Extract Energy (librosa.feature.rms)       │    │  │
│  │  │  └─ Classify frames:                           │    │  │
│  │  │     • F0 > 0          → VOICED                 │    │  │
│  │  │     • F0 = 0, E > T   → UNVOICED               │    │  │
│  │  │     • F0 = 0, E ≤ T   → SILENCE                │    │  │
│  │  └────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 2. Return JSON
                             │
                             ▼
          ┌──────────────────────────────────────┐
          │         JSON RESPONSE                │
          │  {                                   │
          │    "filename": "...",                │
          │    "total_segments": 1234,           │
          │    "segments": [                     │
          │      {                               │
          │        "time": 0.01,                 │
          │        "type": "VOICED",             │
          │        "f0": 150.5,                  │
          │        "energy": 0.15                │
          │      }, ...                          │
          │    ]                                 │
          │  }                                   │
          └──────────────────┬───────────────────┘
                             │
          ┌──────────────────┴───────────────────┐
          │                  │                   │
          ▼                  ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │ Desktop  │       │ Android  │       │   iOS    │
    │ Parse &  │       │ Parse &  │       │ Parse &  │
    │ Display  │       │ Display  │       │ Display  │
    └──────────┘       └──────────┘       └──────────┘
```

## 2. Cấu trúc Code Chi tiết

### Server (Python/FastAPI)

```
server/
├── main.py                 # Entry point, API routes
│   ├── FastAPI()
│   ├── CORS middleware
│   ├── POST /analyze/     # Nhận file, gọi analysis
│   └── Error handling
│
├── analysis.py            # Core business logic
│   ├── AudioAnalyzer
│   │   ├── __init__()
│   │   ├── analyze()         # Main analysis function
│   │   ├── _extract_f0()     # Pitch extraction
│   │   ├── _extract_energy() # RMS calculation
│   │   └── _classify_frames() # Classification logic
│   └── analyze_audio_file()  # Utility function
│
└── requirements.txt
    ├── fastapi
    ├── uvicorn
    ├── librosa
    └── python-multipart
```

### Desktop Client (Python/Tkinter)

```
desktop_client/
└── desktop_app.py
    ├── Config                    # Server URL config
    ├── AnalysisResponse          # Data model
    │   ├── __init__()
    │   └── get_statistics()
    │
    ├── VoiceAnalysisApp          # Main app
    │   ├── __init__()            # Setup UI
    │   ├── _create_ui()          # Build interface
    │   ├── _select_file()        # File picker
    │   ├── _start_analysis()     # Button handler
    │   ├── _perform_analysis()   # Network call (threaded)
    │   ├── _display_results()    # Show results
    │   └── _show_error()         # Error display
    │
    └── main()                    # Entry point
```

### Android Client (Kotlin)

```
android_client/app/src/main/java/com/voiceanalysis/app/
├── MainActivity.kt                     # UI Controller
│   ├── onCreate()
│   ├── setupUI()
│   ├── observeViewModel()             # LiveData observers
│   ├── checkPermissionAndOpenFilePicker()
│   └── analyzeFile()
│
├── data/
│   ├── model/
│   │   └── AnalysisResponse.kt        # Data classes
│   │       ├── AnalysisResponse
│   │       ├── Segment
│   │       └── UiState<T>
│   │
│   ├── network/
│   │   ├── VoiceAnalysisApi.kt        # Retrofit interface
│   │   └── ApiClient.kt               # Retrofit setup
│   │
│   └── repository/
│       └── VoiceAnalysisRepository.kt # API calls
│           └── analyzeAudio()
│
└── ui/
    └── MainViewModel.kt               # ViewModel
        ├── _uiState: LiveData
        ├── _selectedFileName: LiveData
        ├── setSelectedFile()
        ├── analyzeAudio()             # Network call (coroutine)
        └── resetState()
```

### iOS Client (Swift/SwiftUI)

```
ios_client/VoiceAnalysis/
├── VoiceAnalysisApp.swift             # App entry
│
├── Models/
│   └── AnalysisResponse.swift         # Data models
│       ├── AnalysisResponse: Codable
│       ├── Segment: Codable
│       └── UIState<T>
│
├── Services/
│   └── VoiceAnalysisService.swift     # API service
│       ├── shared: Singleton
│       ├── baseURL: String
│       └── analyzeAudio()             # URLSession call
│
├── ViewModels/
│   └── ContentViewModel.swift         # ObservableObject
│       ├── @Published uiState
│       ├── @Published selectedFileName
│       ├── setSelectedFile()
│       ├── analyzeAudio()             # Network call
│       └── resetState()
│
└── Views/
    └── ContentView.swift              # SwiftUI view
        ├── body: View
        ├── headerView
        ├── fileSelectionCard
        ├── actionButtons
        ├── statusView
        ├── resultsCard
        └── DocumentPicker
```

## 3. Phân loại Frame - Thuật toán

```
For each frame in audio:
    
    1. Calculate F0 (Pitch)
       ├─ Use librosa.pyin()
       ├─ fmin = 65 Hz (C2)
       └─ fmax = 2093 Hz (C7)
    
    2. Calculate Energy (RMS)
       └─ Use librosa.feature.rms()
    
    3. Classify:
       
       IF F0 > 0:
           ├─ type = "VOICED"
           └─ (Dây thanh âm rung)
       
       ELSE IF Energy > threshold (default 0.02):
           ├─ type = "UNVOICED"
           └─ (Âm ma sát, không rung dây thanh)
       
       ELSE:
           ├─ type = "SILENCE"
           └─ (Im lặng)
    
    4. Save segment:
       {
           "time": frame_time,
           "type": classification,
           "f0": f0_value,
           "energy": energy_value
       }
```

## 4. Threading Model

### Desktop (Python/Tkinter)

```
Main Thread (UI)
    │
    ├─ User clicks "Analyze"
    │
    ├─ Start background thread ───────────────┐
    │                                          │
    │                                    Worker Thread
    ├─ Disable button                          │
    │                                          ├─ Open file
    ├─ Show "Loading..."                       ├─ POST to server
    │                                          ├─ Wait response
    │                                          └─ Return result
    │                                                    │
    ├─ root.after(0, update_ui) ◄────────────────────────┘
    │       │
    │       └─ Display results
    │       └─ Enable button
    └─ Continue UI loop
```

### Android (Kotlin/Coroutines)

```
Main Thread (UI)
    │
    ├─ User clicks "Analyze"
    │
    ├─ ViewModel.analyzeAudio() ──────────────┐
    │                                          │
    │                                    viewModelScope.launch
    │                                          │
    ├─ _uiState = Loading                      ├─ withContext(IO)
    │                                          ├─ repository.analyzeAudio()
    │                                          │    ├─ Create RequestBody
    │                                          │    ├─ API call (suspend)
    │                                          │    └─ Return Result
    │                                          └─ Back to Main
    │                                                    │
    ├─ Observer triggers ◄───────────────────────────────┘
    │       │
    │       └─ Update UI (Success/Error)
    └─ Continue event loop
```

### iOS (Swift/URLSession)

```
Main Thread (UI)
    │
    ├─ User clicks "Analyze"
    │
    ├─ viewModel.analyzeAudio() ──────────────┐
    │                                          │
    │                                    Background Queue
    │                                          │
    ├─ uiState = .loading                      ├─ Read file
    │                                          ├─ Create URLRequest
    │                                          ├─ URLSession.dataTask
    │                                          └─ Completion handler
    │                                                    │
    ├─ DispatchQueue.main.async ◄────────────────────────┘
    │       │
    │       └─ Update @Published properties
    │       └─ SwiftUI auto-updates view
    └─ Continue RunLoop
```

## 5. Error Handling Flow

```
┌──────────────────────────────────────────────────────┐
│                    Client                            │
│                                                      │
│  Try:                                                │
│    ├─ Open file                                      │
│    ├─ Create request                                 │
│    └─ Send to server                                 │
│                   │                                  │
│  Catch:           │                                  │
│    ├─ FileNotFound    → "Cannot read file"           │
│    ├─ ConnectionError → "Cannot connect to server"   │
│    ├─ Timeout         → "Request timeout"            │
│    └─ Other           → "Error: {message}"           │
└──────────────────────┼───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                    Server                            │
│                                                      │
│  Try:                                                │
│    ├─ Validate file format                           │
│    │    └─ If invalid → 400 Bad Request              │
│    ├─ Save to tempfile                               │
│    ├─ Analyze with librosa                           │
│    └─ Return JSON                                    │
│                                                      │
│  Catch:                                              │
│    ├─ Librosa error  → 500 Internal Server Error     │
│    └─ Other          → 500 with error message        │
│                                                      │
│  Finally:                                            │
│    └─ Delete tempfile                                │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│              Client (Error Display)                  │
│                                                      │
│  Switch status_code:                                 │
│    ├─ 200 → Parse JSON, show results                 │
│    ├─ 400 → "Invalid file format"                    │
│    ├─ 500 → "Server processing error"                │
│    └─ Other → "Unknown error (code)"                 │
└──────────────────────────────────────────────────────┘
```

## 6. Data Flow - JSON Contract

```
Server Response (F-S5 Contract):
{
  "filename": String,          # Tên file gốc
  "total_segments": Integer,   # Tổng số frames
  "segments": [                # Mảng các segments
    {
      "time": Float,           # Thời gian (giây)
      "type": String,          # "VOICED" | "UNVOICED" | "SILENCE"
      "f0": Float,             # Tần số cơ bản (Hz), 0 nếu không có
      "energy": Float          # Năng lượng (RMS)
    },
    ...
  ]
}

Client Processing:
1. Parse JSON to Model/Class
2. Calculate statistics (count by type)
3. Format for display:
   ├─ Summary (filename, total)
   ├─ Statistics (percentages)
   └─ Detailed list (first N segments)
```

---

**Ghi chú**: Sơ đồ này mô tả kiến trúc ở mức cao. Chi tiết implementation xem trong code của từng component.
