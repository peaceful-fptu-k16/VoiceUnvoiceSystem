package com.voiceanalysis.app.ui

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.voiceanalysis.app.data.model.AnalysisResponse
import com.voiceanalysis.app.data.model.UiState
import com.voiceanalysis.app.data.repository.VoiceAnalysisRepository
import kotlinx.coroutines.launch
import java.io.File

/**
 * ViewModel cho MainActivity
 * Tuân thủ S-A1: Sử dụng ViewModel để chứa logic, tách biệt khỏi Activity
 */
class MainViewModel : ViewModel() {
    
    private val repository = VoiceAnalysisRepository()
    
    // LiveData cho UI state
    private val _uiState = MutableLiveData<UiState<AnalysisResponse>>(UiState.Idle)
    val uiState: LiveData<UiState<AnalysisResponse>> = _uiState
    
    // LiveData cho tên file đã chọn
    private val _selectedFileName = MutableLiveData<String>()
    val selectedFileName: LiveData<String> = _selectedFileName
    
    /**
     * Cập nhật tên file đã chọn
     */
    fun setSelectedFile(fileName: String) {
        _selectedFileName.value = fileName
    }
    
    /**
     * Phân tích file âm thanh
     * Tuân thủ S-A2: Sử dụng Coroutines (viewModelScope)
     * F-C5: Gửi file đến server
     */
    fun analyzeAudio(file: File) {
        // F-C6: Hiển thị loading
        _uiState.value = UiState.Loading
        
        // Chạy trong coroutine với Dispatchers.IO (S-A2)
        viewModelScope.launch {
            val result = repository.analyzeAudio(file)
            
            // F-C7: Parse JSON và cập nhật UI
            _uiState.value = result.fold(
                onSuccess = { response ->
                    UiState.Success(response)
                },
                onFailure = { exception ->
                    // F-C9: Hiển thị lỗi rõ ràng
                    UiState.Error(exception.message ?: "Unknown error")
                }
            )
        }
    }
    
    /**
     * Reset UI state về Idle
     */
    fun resetState() {
        _uiState.value = UiState.Idle
    }
}
