import Foundation

/**
 * Service để gọi API
 * Tuân thủ S-I1: Sử dụng URLSession để gọi mạng (bất đồng bộ)
 * Tuân thủ S-5: Server URL trong config
 */

class VoiceAnalysisService {
    
    // MARK: - Configuration
    
    /**
     * Địa chỉ server - S-5: Config variable
     * Thay đổi địa chỉ này theo môi trường của bạn
     * 
     * - Simulator: Có thể dùng "http://127.0.0.1:8000" hoặc "http://localhost:8000"
     * - Thiết bị thật: Dùng IP nội bộ của máy chạy server (tìm bằng ipconfig trên Windows hoặc ifconfig trên Mac)
     */
    private let baseURL = "http://192.168.20.100:8000"  // IP của máy Windows chạy server
    
    // MARK: - Singleton
    static let shared = VoiceAnalysisService()
    
    private init() {}
    
    // MARK: - API Methods
    
    /**
     * Gửi file âm thanh lên server để phân tích
     * F-C5: Gửi file đến server
     * S-I1: Sử dụng URLSession (bất đồng bộ)
     *
     * - Parameters:
     *   - fileURL: URL của file âm thanh
     *   - completion: Closure được gọi khi hoàn thành (Result pattern)
     */
    func analyzeAudio(fileURL: URL, completion: @escaping (Result<AnalysisResponse, Error>) -> Void) {
        // Tạo URL cho endpoint
        guard let url = URL(string: "\(baseURL)/analyze/") else {
            completion(.failure(NetworkError.invalidURL))
            return
        }
        
        // Tạo multipart/form-data request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        // Đọc file data
        guard let fileData = try? Data(contentsOf: fileURL) else {
            completion(.failure(NetworkError.cannotReadFile))
            return
        }
        
        let fileName = fileURL.lastPathComponent
        let mimeType = getMimeType(for: fileURL.pathExtension)
        
        // Tạo body
        var body = Data()
        
        // Thêm file data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(fileData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        // Tạo URLSession task - S-I1
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            // S-2: Error handling
            if let error = error {
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.connectionError(error.localizedDescription)))
                }
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.invalidResponse))
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.noData))
                }
                return
            }
            
            // Kiểm tra status code
            switch httpResponse.statusCode {
            case 200:
                // Parse JSON - S-I2: Sử dụng Codable
                do {
                    let decoder = JSONDecoder()
                    let response = try decoder.decode(AnalysisResponse.self, from: data)
                    DispatchQueue.main.async {
                        completion(.success(response))
                    }
                } catch {
                    DispatchQueue.main.async {
                        completion(.failure(NetworkError.decodingError(error.localizedDescription)))
                    }
                }
                
            case 400:
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.badRequest("File không hợp lệ hoặc định dạng không được hỗ trợ")))
                }
                
            case 500:
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.serverError("Lỗi server khi xử lý file")))
                }
                
            default:
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.unknownError("Lỗi không xác định (\(httpResponse.statusCode))")))
                }
            }
        }
        
        task.resume()
    }
    
    // MARK: - Helper Methods
    
    private func getMimeType(for pathExtension: String) -> String {
        switch pathExtension.lowercased() {
        case "wav":
            return "audio/wav"
        case "mp3":
            return "audio/mpeg"
        case "m4a":
            return "audio/mp4"
        case "flac":
            return "audio/flac"
        case "ogg":
            return "audio/ogg"
        default:
            return "application/octet-stream"
        }
    }
}

// MARK: - Network Errors

enum NetworkError: LocalizedError {
    case invalidURL
    case cannotReadFile
    case connectionError(String)
    case invalidResponse
    case noData
    case badRequest(String)
    case serverError(String)
    case unknownError(String)
    case decodingError(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "URL không hợp lệ"
        case .cannotReadFile:
            return "Không thể đọc file"
        case .connectionError(let message):
            return "Lỗi kết nối: \(message)"
        case .invalidResponse:
            return "Response không hợp lệ"
        case .noData:
            return "Không có dữ liệu"
        case .badRequest(let message):
            return message
        case .serverError(let message):
            return message
        case .unknownError(let message):
            return message
        case .decodingError(let message):
            return "Lỗi parse JSON: \(message)"
        }
    }
}
