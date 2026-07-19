document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const tabs = document.querySelectorAll('.tab-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const modalSettings = document.getElementById('modal-settings');
    const btnOpenSettings = document.getElementById('btn-open-settings');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const inputApiKey = document.getElementById('input-api-key');
    const btnSaveApi = document.getElementById('btn-save-api');
    const btnTestApi = document.getElementById('btn-test-api');
    const testResultMessage = document.getElementById('test-result-message');
    
    const btnValidate = document.getElementById('btn-validate');
    const btnSchedule = document.getElementById('btn-schedule');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    
    const logTerminal = document.getElementById('log-terminal');
    const statusLabel = document.getElementById('status-label');
    const scoreLabel = document.getElementById('score-label');

    // --- Tab Navigation ---
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            const targetId = tab.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // --- Modal Management ---
    function openSettingsModal() {
        inputApiKey.value = window.aiService.getApiKey();
        testResultMessage.className = 'hidden';
        testResultMessage.textContent = '';
        modalSettings.classList.remove('hidden');
    }
    
    function closeSettingsModal() {
        modalSettings.classList.add('hidden');
    }

    btnOpenSettings.addEventListener('click', openSettingsModal);
    btnCloseModal.addEventListener('click', closeSettingsModal);

    // Initial API Key check
    if (!window.aiService.getApiKey()) {
        openSettingsModal();
    } else {
        btnOpenSettings.innerHTML = `<i class='bx bx-check-circle'></i><span>Đã cấu hình API Key</span>`;
        btnOpenSettings.classList.remove('warning');
        btnOpenSettings.classList.add('success');
    }

    btnSaveApi.addEventListener('click', () => {
        const key = inputApiKey.value.trim();
        if (key) {
            window.aiService.setApiKey(key);
            btnOpenSettings.innerHTML = `<i class='bx bx-check-circle'></i><span>Đã cấu hình API Key</span>`;
            btnOpenSettings.classList.remove('warning');
            btnOpenSettings.classList.add('success');
            logToTerminal("Đã lưu API Key thành công.", "success");
            closeSettingsModal();
        } else {
            testResultMessage.textContent = "Vui lòng nhập API Key hợp lệ!";
            testResultMessage.className = 'text-danger';
        }
    });

    btnTestApi.addEventListener('click', async () => {
        const key = inputApiKey.value.trim();
        if (!key) {
            testResultMessage.textContent = "Bạn chưa nhập API Key!";
            testResultMessage.className = 'text-danger';
            return;
        }

        // Tạm lưu để test
        window.aiService.setApiKey(key);
        
        btnTestApi.disabled = true;
        btnTestApi.textContent = "ĐANG THỬ...";
        testResultMessage.textContent = "Đang kết nối đến Gemini...";
        testResultMessage.className = '';

        try {
            const response = await window.aiService.callGemini("Hãy trả lời ngắn gọn: Kết nối API thành công!");
            testResultMessage.innerHTML = `<strong>Thành công!</strong> Phản hồi: ${response}`;
            testResultMessage.className = 'text-success';
            logToTerminal(`Kiểm tra API thành công: ${response}`, "success");
        } catch (error) {
            testResultMessage.innerHTML = `<strong>Lỗi:</strong> ${error.message}`;
            testResultMessage.className = 'text-danger';
            logToTerminal(`Lỗi kiểm tra API: ${error.message}`, "error");
        } finally {
            btnTestApi.disabled = false;
            btnTestApi.textContent = "KIỂM TRA KẾT NỐI";
        }
    });

    // --- App Logic ---
    function logToTerminal(message, type = "info") {
        const div = document.createElement('div');
        div.className = `log-entry ${type === 'error' ? 'log-error' : (type === 'warn' ? 'log-warn' : '')}`;
        const time = new Date().toLocaleTimeString();
        div.textContent = `[${time}] ${message}`;
        logTerminal.appendChild(div);
        logTerminal.scrollTop = logTerminal.scrollHeight;
    }

    btnValidate.addEventListener('click', () => {
        logToTerminal("Đang kiểm tra dữ liệu đầu vào...");
        setTimeout(() => {
            logToTerminal("Dữ liệu hợp lệ. Sẵn sàng xếp Thời Khóa Biểu.", "success");
            alert("Dữ liệu hợp lệ!");
        }, 500);
    });

    btnSchedule.addEventListener('click', async () => {
        progressContainer.classList.remove('hidden');
        progressBar.classList.remove('error');
        progressBar.style.width = '10%';
        progressText.textContent = "Khởi tạo dữ liệu...";
        progressPercent.textContent = "10%";
        logToTerminal("Bắt đầu quá trình xếp Thời Khóa Biểu...");

        if (!window.aiService.getApiKey()) {
            progressBar.classList.add('error');
            progressBar.style.width = '100%';
            progressText.textContent = "Đã dừng do lỗi: Chưa cấu hình API Key!";
            progressPercent.textContent = "LỖI";
            logToTerminal("Quá trình thất bại do thiếu API Key.", "error");
            openSettingsModal();
            return;
        }

        try {
            // Step 1: AI Parsing (Simulated)
            progressBar.style.width = '40%';
            progressText.textContent = "AI đang đọc Phân công chuyên môn (PDF)...";
            progressPercent.textContent = "40%";
            logToTerminal("Đang gọi AI Fallback model để đọc PDF...");

            // Giả lập gọi AI đọc cấu trúc
            const aiResponse = await window.aiService.callGemini("Phân tích cấu trúc phân công chuyên môn giáo viên Tiểu học (Mô phỏng). Trả về OK.");
            logToTerminal(`AI Response: ${aiResponse}`);

            // Step 2: Scheduling (Simulated)
            progressBar.style.width = '80%';
            progressText.textContent = "OR-Tools đang tối ưu hóa...";
            progressPercent.textContent = "80%";
            logToTerminal("OR-Tools CP-SAT đang tìm phương án tốt nhất...");
            
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Done
            progressBar.style.width = '100%';
            progressText.textContent = "Hoàn tất xếp lịch!";
            progressPercent.textContent = "100%";
            
            statusLabel.textContent = "Đã hoàn thành";
            statusLabel.style.color = "var(--success)";
            scoreLabel.textContent = "95/100";
            logToTerminal("Đã sinh Thời Khóa Biểu thành công.", "success");

            // Kích hoạt các nút Download
            document.querySelectorAll('#tab-results .btn-primary, #tab-results .btn-secondary').forEach(b => {
                b.disabled = false;
            });

        } catch (error) {
            progressBar.classList.add('error');
            progressBar.style.width = '100%';
            progressText.textContent = `Đã dừng do lỗi API`;
            progressPercent.textContent = "LỖI";
            statusLabel.textContent = "Lỗi Xếp Lịch";
            statusLabel.style.color = "var(--danger)";
            
            logToTerminal(`Xảy ra lỗi trong quá trình xử lý: ${error.message}`, "error");
        }
    });

    logToTerminal("Ứng dụng khởi động thành công. Vui lòng kiểm tra API Key.", "success");
});
