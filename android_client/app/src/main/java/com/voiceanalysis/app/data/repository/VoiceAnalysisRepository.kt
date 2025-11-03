package com.voiceanalysis.app.data.repository

import android.net.Uri
import com.voiceanalysis.app.data.model.AnalysisResponse
import com.voiceanalysis.app.data.network.ApiClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

/**
 * Repository để xử lý logic gọi API
 * Tuân thủ S-A1: Tách biệt logic khỏi Activity/Fragment
 */
class VoiceAnalysisRepository {
    
    /**
     * Gửi file âm thanh lên server để phân tích
     * Tuân thủ S-A2: Sử dụng Coroutines với Dispatchers.IO
     * 
     * @param file File âm thanh cần phân tích
     * @return Result chứa AnalysisResponse hoặc Exception
     */
    suspend fun analyzeAudio(file: File): Result<AnalysisResponse> = 
        withContext(Dispatchers.IO) {
            try {
                // Tạo RequestBody từ file
                val requestBody = file.asRequestBody("audio/*".toMediaTypeOrNull())
                
                // Tạo MultipartBody.Part
                val filePart = MultipartBody.Part.createFormData(
                    "file",
                    file.name,
                    requestBody
                )
                
                // Gọi API
                val response = ApiClient.apiService.analyzeAudio(filePart)
                
                // Xử lý response - F-C9: Xử lý lỗi rõ ràng
                if (response.isSuccessful) {
                    val body = response.body()
                    if (body != null) {
                        Result.success(body)
                    } else {
                        Result.failure(Exception("Response body is null"))
                    }
                } else {
                    val errorMsg = when (response.code()) {
                        400 -> "File không hợp lệ hoặc định dạng không được hỗ trợ"
                        500 -> "Lỗi server khi xử lý file"
                        else -> "Lỗi không xác định (${response.code()})"
                    }
                    Result.failure(Exception(errorMsg))
                }
            } catch (e: Exception) {
                // S-2: Error handling
                val errorMsg = when {
                    e.message?.contains("Unable to resolve host") == true -> 
                        "Không thể kết nối đến server"
                    e.message?.contains("timeout") == true -> 
                        "Timeout - Server không phản hồi"
                    else -> 
                        "Lỗi: ${e.message}"
                }
                Result.failure(Exception(errorMsg))
            }
        }
}
