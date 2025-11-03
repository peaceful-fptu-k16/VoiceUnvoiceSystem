import Foundation

/**
 * Model dữ liệu cho API response
 * Tuân thủ S-I2: Sử dụng Codable để parse JSON tự động
 * Tuân thủ S-4: Sử dụng Model để parse JSON
 */

// MARK: - Analysis Response
struct AnalysisResponse: Codable {
    let filename: String
    let totalSegments: Int
    let segments: [Segment]
    
    enum CodingKeys: String, CodingKey {
        case filename
        case totalSegments = "total_segments"
        case segments
    }
    
    /// Tính thống kê các loại frame
    func getStatistics() -> [String: Int] {
        var stats: [String: Int] = [
            "VOICED": 0,
            "UNVOICED": 0,
            "SILENCE": 0
        ]
        
        for segment in segments {
            stats[segment.type, default: 0] += 1
        }
        
        return stats
    }
}

// MARK: - Segment
struct Segment: Codable {
    let time: Double
    let type: String
    let f0: Double
    let energy: Double
}

// MARK: - UI State
enum UIState<T> {
    case idle
    case loading
    case success(T)
    case error(String)
}
