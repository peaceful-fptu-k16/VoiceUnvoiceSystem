import SwiftUI

/**
 * ViewModel cho ContentView
 * Tuân thủ S-I3: Sử dụng ObservableObject để truyền dữ liệu
 */

class ContentViewModel: ObservableObject {
    // MARK: - Published Properties
    
    @Published var selectedFileName: String = "No file selected"
    @Published var uiState: UIState<AnalysisResponse> = .idle
    @Published var isFileSelected: Bool = false
    
    // MARK: - Private Properties
    
    private let service = VoiceAnalysisService.shared
    private var selectedFileURL: URL?
    
    // MARK: - Methods
    
    /**
     * Cập nhật file đã chọn
     * F-C3: Hiển thị tên file
     */
    func setSelectedFile(url: URL) {
        self.selectedFileURL = url
        self.selectedFileName = url.lastPathComponent
        self.isFileSelected = true
    }
    
    /**
     * Phân tích file âm thanh
     * F-C5: Gửi file đến server
     * S-I1: Gọi mạng bất đồng bộ
     */
    func analyzeAudio() {
        guard let fileURL = selectedFileURL else {
            self.uiState = .error("Vui lòng chọn file trước")
            return
        }
        
        // F-C6: Hiển thị loading
        self.uiState = .loading
        
        // Gọi API - S-I3: Completion handler
        service.analyzeAudio(fileURL: fileURL) { [weak self] result in
            guard let self = self else { return }
            
            // F-C7: Parse JSON và cập nhật UI
            switch result {
            case .success(let response):
                // F-C8: Hiển thị kết quả
                self.uiState = .success(response)
                
            case .failure(let error):
                // F-C9: Hiển thị lỗi
                self.uiState = .error(error.localizedDescription)
            }
        }
    }
    
    /**
     * Reset state về idle
     */
    func resetState() {
        self.uiState = .idle
    }
    
    /**
     * Clear results
     */
    func clearResults() {
        self.selectedFileName = "No file selected"
        self.isFileSelected = false
        self.selectedFileURL = nil
        self.uiState = .idle
    }
}
