package com.voiceanalysis.app.data.network

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Singleton để quản lý Retrofit instance
 * Tuân thủ S-5: Server URL trong config
 */
object ApiClient {
    
    /**
     * Địa chỉ server - S-5: Config variable
     * S-A5: Sử dụng 10.0.2.2 cho emulator hoặc IP nội bộ cho thiết bị thật
     */
    private const val BASE_URL = "http://10.0.2.2:8000/"  // Emulator
    // private const val BASE_URL = "http://192.168.1.100:8000/"  // Thiết bị thật
    
    /**
     * OkHttpClient với logging và timeout
     */
    private val okHttpClient: OkHttpClient by lazy {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .build()
    }
    
    /**
     * Retrofit instance
     */
    private val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    /**
     * API service instance
     */
    val apiService: VoiceAnalysisApi by lazy {
        retrofit.create(VoiceAnalysisApi::class.java)
    }
}
