package com.voiceanalysis.app.data.model

import com.google.gson.annotations.SerializedName

/**
 * Model dữ liệu cho API response
 * Tuân thủ S-4: Sử dụng Model để parse JSON
 * Hợp đồng F-S5: Cấu trúc JSON chuẩn
 */

data class AnalysisResponse(
    @SerializedName("filename")
    val filename: String,
    
    @SerializedName("total_segments")
    val totalSegments: Int,
    
    @SerializedName("segments")
    val segments: List<Segment>
) {
    /**
     * Tính thống kê các loại frame
     */
    fun getStatistics(): Map<String, Int> {
        val stats = mutableMapOf(
            "VOICED" to 0,
            "UNVOICED" to 0,
            "SILENCE" to 0
        )
        
        segments.forEach { segment ->
            stats[segment.type] = (stats[segment.type] ?: 0) + 1
        }
        
        return stats
    }
}

data class Segment(
    @SerializedName("time")
    val time: Double,
    
    @SerializedName("type")
    val type: String,
    
    @SerializedName("f0")
    val f0: Double,
    
    @SerializedName("energy")
    val energy: Double
)

/**
 * Wrapper cho trạng thái UI
 */
sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}
