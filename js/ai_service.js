class AIService {
    constructor() {
        this.models = [
            "gemini-3-flash-preview",
            "gemini-3-pro-preview",
            "gemini-2.5-flash"
        ];
    }

    getApiKey() {
        return localStorage.getItem('gemini_api_key') || '';
    }

    setApiKey(key) {
        localStorage.setItem('gemini_api_key', key);
    }

    async callGemini(prompt, systemInstruction = "") {
        const apiKey = this.getApiKey();
        if (!apiKey) {
            throw new Error("Chưa cấu hình API Key. Vui lòng nhập API Key để sử dụng tính năng này.");
        }

        let lastError = null;

        for (const model of this.models) {
            try {
                console.log(`Đang thử gọi model: ${model}`);
                return await this._executeRequest(model, apiKey, prompt, systemInstruction);
            } catch (error) {
                console.warn(`Model ${model} thất bại: ${error.message}`);
                lastError = error;
                // Nếu lỗi là 400 (Bad Request do sai API format) hoặc 403 (Invalid Key) thì không nên retry các model sau.
                // Ở đây mô phỏng Fallback nên cứ tiếp tục.
            }
        }

        throw new Error(`Tất cả model đều thất bại. Lỗi cuối: ${lastError.message}`);
    }

    async _executeRequest(model, apiKey, prompt, systemInstruction) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
        
        const payload = {
            contents: [{ parts: [{ text: prompt }] }]
        };

        if (systemInstruction) {
            payload.systemInstruction = {
                parts: [{ text: systemInstruction }]
            };
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        try {
            return data.candidates[0].content.parts[0].text;
        } catch (e) {
            throw new Error("Không thể đọc phản hồi từ Gemini API.");
        }
    }
}

// Global instance
window.aiService = new AIService();
