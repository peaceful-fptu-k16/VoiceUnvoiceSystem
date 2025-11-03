import SwiftUI
import UniformTypeIdentifiers

/**
 * Màn hình chính của ứng dụng
 * Tuân thủ tất cả yêu cầu F-C1 đến F-C9
 */

struct ContentView: View {
    // MARK: - Properties
    
    @StateObject private var viewModel = ContentViewModel()
    @State private var showFilePicker = false
    @State private var showErrorAlert = false
    @State private var errorMessage = ""
    
    // MARK: - Body
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Header
                    headerView
                    
                    // File Selection - F-C1, F-C3
                    fileSelectionCard
                    
                    // Action Buttons - F-C4
                    actionButtons
                    
                    // Status - F-C6
                    statusView
                    
                    // Results - F-C8
                    resultsCard
                    
                    Spacer()
                }
                .padding()
            }
            .navigationTitle("Voice Analysis")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $showFilePicker) {
                DocumentPicker(onDocumentPicked: { url in
                    viewModel.setSelectedFile(url: url)
                })
            }
            .alert("Error", isPresented: $showErrorAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(errorMessage)
            }
            .onChange(of: viewModel.uiState) { state in
                // F-C9: Hiển thị lỗi
                if case .error(let message) = state {
                    errorMessage = message
                    showErrorAlert = true
                }
            }
        }
    }
    
    // MARK: - View Components
    
    private var headerView: some View {
        VStack {
            Image(systemName: "waveform.circle.fill")
                .font(.system(size: 60))
                .foregroundColor(.blue)
            
            Text("🎙️ Voice Analysis System")
                .font(.title2)
                .fontWeight(.bold)
        }
        .padding(.top)
    }
    
    private var fileSelectionCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("File Selection", systemImage: "folder")
                .font(.headline)
            
            Button(action: {
                showFilePicker = true
            }) {
                HStack {
                    Image(systemName: "doc.badge.plus")
                    Text("Choose Audio File")
                }
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
            
            // F-C3: Hiển thị tên file
            Text(viewModel.selectedFileName)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    private var actionButtons: some View {
        HStack(spacing: 16) {
            // F-C4: Nút Analyze
            Button(action: {
                viewModel.analyzeAudio()
            }) {
                HStack {
                    Image(systemName: "magnifyingglass")
                    Text("Analyze")
                }
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .disabled(!viewModel.isFileSelected || isLoading)
            
            Button(action: {
                viewModel.clearResults()
            }) {
                HStack {
                    Image(systemName: "trash")
                    Text("Clear")
                }
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
    }
    
    private var statusView: some View {
        HStack {
            switch viewModel.uiState {
            case .idle:
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.green)
                Text("Sẵn sàng")
                    .foregroundColor(.green)
                
            case .loading:
                // F-C6: Loading indicator
                ProgressView()
                Text("Đang phân tích...")
                    .foregroundColor(.orange)
                
            case .success:
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.green)
                Text("Phân tích hoàn tất!")
                    .foregroundColor(.green)
                
            case .error:
                Image(systemName: "xmark.circle.fill")
                    .foregroundColor(.red)
                Text("Lỗi")
                    .foregroundColor(.red)
            }
        }
        .font(.subheadline)
    }
    
    private var resultsCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Analysis Results", systemImage: "chart.bar")
                .font(.headline)
            
            ScrollView {
                switch viewModel.uiState {
                case .success(let response):
                    // F-C8: Hiển thị kết quả
                    ResultsView(response: response)
                    
                default:
                    Text("Chưa có kết quả")
                        .foregroundColor(.secondary)
                        .frame(maxWidth: .infinity, alignment: .center)
                        .padding()
                }
            }
            .frame(minHeight: 300)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    private var isLoading: Bool {
        if case .loading = viewModel.uiState {
            return true
        }
        return false
    }
}

// MARK: - Results View

struct ResultsView: View {
    let response: AnalysisResponse
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Summary
            VStack(alignment: .leading, spacing: 8) {
                Text("📄 File: \(response.filename)")
                    .font(.subheadline)
                Text("📊 Total Segments: \(response.totalSegments)")
                    .font(.subheadline)
            }
            .padding(.bottom, 8)
            
            Divider()
            
            // Statistics
            Text("📈 STATISTICS:")
                .font(.headline)
                .padding(.top, 8)
            
            let stats = response.getStatistics()
            let total = response.totalSegments
            
            ForEach(["VOICED", "UNVOICED", "SILENCE"], id: \.self) { type in
                let count = stats[type] ?? 0
                let percentage = total > 0 ? Double(count) / Double(total) * 100 : 0.0
                let emoji = type == "VOICED" ? "🔊" : (type == "UNVOICED" ? "💨" : "🔇")
                
                HStack {
                    Text("\(emoji) \(type):")
                        .frame(width: 120, alignment: .leading)
                    Text("\(count) frames")
                        .frame(width: 100, alignment: .leading)
                    Text(String(format: "(%.2f%%)", percentage))
                        .foregroundColor(.secondary)
                }
                .font(.system(.caption, design: .monospaced))
            }
            
            Divider()
            
            // Detailed segments
            Text("🔍 FIRST 20 SEGMENTS:")
                .font(.headline)
                .padding(.top, 8)
            
            VStack(alignment: .leading, spacing: 4) {
                ForEach(Array(response.segments.prefix(20).enumerated()), id: \.offset) { _, segment in
                    Text(formatSegment(segment))
                        .font(.system(.caption2, design: .monospaced))
                }
                
                if response.segments.count > 20 {
                    Text("\n... và \(response.segments.count - 20) segments nữa")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
    
    private func formatSegment(_ segment: Segment) -> String {
        return String(format: "%.3f | %-10s | F0: %6.2f Hz | E: %.4f",
                     segment.time, segment.type, segment.f0, segment.energy)
    }
}

// MARK: - Document Picker

struct DocumentPicker: UIViewControllerRepresentable {
    var onDocumentPicked: (URL) -> Void
    
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        // F-C1: Chọn file âm thanh
        let picker = UIDocumentPickerViewController(
            forOpeningContentTypes: [
                UTType.audio,
                UTType(filenameExtension: "wav")!,
                UTType(filenameExtension: "mp3")!,
                UTType(filenameExtension: "m4a")!
            ],
            asCopy: true
        )
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: DocumentPicker
        
        init(_ parent: DocumentPicker) {
            self.parent = parent
        }
        
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            parent.onDocumentPicked(url)
        }
    }
}

// MARK: - Preview

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
