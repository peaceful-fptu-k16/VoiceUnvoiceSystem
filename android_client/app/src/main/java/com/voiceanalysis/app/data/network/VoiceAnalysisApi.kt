package com.voiceanalysis.app.data.network

import com.voiceanalysis.app.data.model.AnalysisResponse
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

/**
 * API Interface cho Retrofit
 * Định nghĩa endpoint F-S1
 */
interface VoiceAnalysisApi {
    
    @Multipart
    @POST("analyze/")
    suspend fun analyzeAudio(
        @Part file: MultipartBody.Part
    ): Response<AnalysisResponse>
}
