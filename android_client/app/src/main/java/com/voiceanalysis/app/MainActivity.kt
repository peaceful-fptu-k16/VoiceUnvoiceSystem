package com.voiceanalysis.app

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.view.View
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.android.material.snackbar.Snackbar
import com.voiceanalysis.app.data.model.UiState
import com.voiceanalysis.app.databinding.ActivityMainBinding
import com.voiceanalysis.app.ui.MainViewModel
import java.io.File
import java.io.FileOutputStream

/**
 * MainActivity - Màn hình chính của ứng dụng
 * Tuân thủ tất cả yêu cầu F-C1 đến F-C9
 */
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()
    
    private var selectedFileUri: Uri? = null
    
    // Launcher để chọn file - F-C1
    private val filePickerLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            result.data?.data?.let { uri ->
                handleSelectedFile(uri)
            }
        }
    }
    
    // Launcher để xin quyền storage
    private val storagePermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            openFilePicker()
        } else {
            showError("Cần quyền truy cập bộ nhớ để chọn file")
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        observeViewModel()
    }
    
    private fun setupUI() {
        // F-C1: Nút chọn file
        binding.btnSelectFile.setOnClickListener {
            checkPermissionAndOpenFilePicker()
        }
        
        // F-C4: Nút phân tích
        binding.btnAnalyze.setOnClickListener {
            selectedFileUri?.let { uri ->
                analyzeFile(uri)
            }
        }
        
        // Nút xóa kết quả
        binding.btnClear.setOnClickListener {
            clearResults()
        }
    }
    
    private fun observeViewModel() {
        // Observe tên file - F-C3
        viewModel.selectedFileName.observe(this) { fileName ->
            binding.tvSelectedFile.text = fileName
        }
        
        // Observe UI state
        viewModel.uiState.observe(this) { state ->
            when (state) {
                is UiState.Idle -> {
                    showIdle()
                }
                is UiState.Loading -> {
                    showLoading()  // F-C6
                }
                is UiState.Success -> {
                    showSuccess(state.data)  // F-C8
                }
                is UiState.Error -> {
                    showError(state.message)  // F-C9
                }
            }
        }
    }
    
    private fun checkPermissionAndOpenFilePicker() {
        // Kiểm tra quyền READ_EXTERNAL_STORAGE
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            // Android 13+ không cần quyền cho file picker
            openFilePicker()
        } else {
            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.READ_EXTERNAL_STORAGE
                ) == PackageManager.PERMISSION_GRANTED
            ) {
                openFilePicker()
            } else {
                storagePermissionLauncher.launch(Manifest.permission.READ_EXTERNAL_STORAGE)
            }
        }
    }
    
    private fun openFilePicker() {
        val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
            type = "audio/*"
            addCategory(Intent.CATEGORY_OPENABLE)
        }
        filePickerLauncher.launch(intent)
    }
    
    private fun handleSelectedFile(uri: Uri) {
        selectedFileUri = uri
        
        // Lấy tên file - F-C3
        val fileName = getFileName(uri)
        viewModel.setSelectedFile(fileName)
        
        // Kích hoạt nút Analyze
        binding.btnAnalyze.isEnabled = true
        
        Snackbar.make(binding.root, "✅ Đã chọn: $fileName", Snackbar.LENGTH_SHORT).show()
    }
    
    private fun getFileName(uri: Uri): String {
        var name = "unknown"
        val cursor = contentResolver.query(uri, null, null, null, null)
        cursor?.use {
            if (it.moveToFirst()) {
                val nameIndex = it.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (nameIndex >= 0) {
                    name = it.getString(nameIndex)
                }
            }
        }
        return name
    }
    
    private fun analyzeFile(uri: Uri) {
        try {
            // Copy file từ Uri sang file tạm
            val tempFile = createTempFileFromUri(uri)
            
            // F-C5: Gửi file đến server
            viewModel.analyzeAudio(tempFile)
            
        } catch (e: Exception) {
            showError("Không thể đọc file: ${e.message}")
        }
    }
    
    private fun createTempFileFromUri(uri: Uri): File {
        val inputStream = contentResolver.openInputStream(uri)
            ?: throw Exception("Cannot open input stream")
        
        val tempFile = File.createTempFile("audio_", ".tmp", cacheDir)
        
        inputStream.use { input ->
            FileOutputStream(tempFile).use { output ->
                input.copyTo(output)
            }
        }
        
        return tempFile
    }
    
    private fun showIdle() {
        binding.progressBar.visibility = View.GONE
        binding.tvStatus.text = "Sẵn sàng"
        binding.tvStatus.setTextColor(getColor(android.R.color.holo_green_dark))
        binding.btnAnalyze.isEnabled = selectedFileUri != null
    }
    
    private fun showLoading() {
        // F-C6: Hiển thị "Đang xử lý..." và vô hiệu hóa nút
        binding.progressBar.visibility = View.VISIBLE
        binding.tvStatus.text = "⏳ Đang phân tích..."
        binding.tvStatus.setTextColor(getColor(android.R.color.holo_orange_dark))
        binding.btnAnalyze.isEnabled = false
        binding.tvResults.text = ""
    }
    
    private fun showSuccess(response: com.voiceanalysis.app.data.model.AnalysisResponse) {
        // F-C8: Hiển thị kết quả
        binding.progressBar.visibility = View.GONE
        binding.tvStatus.text = "✅ Phân tích hoàn tất!"
        binding.tvStatus.setTextColor(getColor(android.R.color.holo_green_dark))
        binding.btnAnalyze.isEnabled = true
        
        // Format kết quả
        val stats = response.getStatistics()
        val total = response.totalSegments
        
        val resultText = buildString {
            appendLine("═".repeat(50))
            appendLine("📄 File: ${response.filename}")
            appendLine("📊 Total Segments: $total")
            appendLine("═".repeat(50))
            appendLine()
            appendLine("📈 STATISTICS:")
            appendLine("─".repeat(50))
            
            stats.forEach { (type, count) ->
                val percentage = if (total > 0) (count.toFloat() / total * 100) else 0f
                val emoji = when (type) {
                    "VOICED" -> "🔊"
                    "UNVOICED" -> "💨"
                    else -> "🔇"
                }
                appendLine("$emoji $type: $count frames (${String.format("%.2f", percentage)}%)")
            }
            
            appendLine()
            appendLine("═".repeat(50))
            appendLine("🔍 FIRST 20 SEGMENTS:")
            appendLine("─".repeat(50))
            
            response.segments.take(20).forEach { segment ->
                appendLine(
                    String.format(
                        "%.3f | %-10s | F0: %6.2f Hz | Energy: %.4f",
                        segment.time,
                        segment.type,
                        segment.f0,
                        segment.energy
                    )
                )
            }
            
            if (response.segments.size > 20) {
                appendLine("\n... và ${response.segments.size - 20} segments nữa")
            }
        }
        
        binding.tvResults.text = resultText
    }
    
    private fun showError(message: String) {
        // F-C9: Hiển thị lỗi rõ ràng
        binding.progressBar.visibility = View.GONE
        binding.tvStatus.text = "❌ Lỗi"
        binding.tvStatus.setTextColor(getColor(android.R.color.holo_red_dark))
        binding.btnAnalyze.isEnabled = true
        
        AlertDialog.Builder(this)
            .setTitle("Lỗi phân tích")
            .setMessage(message)
            .setPositiveButton("OK", null)
            .show()
    }
    
    private fun clearResults() {
        binding.tvResults.text = ""
        viewModel.resetState()
    }
}
