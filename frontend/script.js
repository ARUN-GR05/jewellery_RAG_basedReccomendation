// ⚠️ CHANGE THIS TO YOUR RENDER URL AFTER DEPLOYMENT
const API_BASE = "http://127.0.0.1:8000";

// --- TAB SWITCHING ---
function switchTab(mode) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

    document.querySelector(`button[onclick="switchTab('${mode}')"]`).classList.add('active');
    document.getElementById(`${mode}-panel`).classList.add('active');
}

// --- FILE UPLOAD HANDLING ---
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('image-preview').src = e.target.result;
            document.getElementById('drop-zone').classList.add('hidden');
            document.getElementById('preview-container').classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});



// --- ENTER KEY SUPPORT ---
const queryInput = document.getElementById('query-input');
queryInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        runTextSearch();
    }
});

// --- API CALLS ---

async function runTextSearch() {
    const query = document.getElementById('query-input').value;
    if (!query) return;

    showLoader(true, "Searching database...");

    try {
        const resultsCount = document.getElementById('results-count').value;
        const formData = new FormData();
        formData.append('query', query);
        formData.append('top_k', resultsCount);

        const response = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        renderResults(data.results);
        document.getElementById('ai-insight').classList.add('hidden'); // Hide AI box for text search
    } catch (error) {
        console.error(error);
        alert("Error connecting to server. Is the backend running?");
    }
    showLoader(false);
}

async function runImageSearch() {
    const file = fileInput.files[0];
    if (!file) return;

    showLoader(true, "Scanning image with AI (OCR + Vision)...");

    try {
        const resultsCount = document.getElementById('results-count').value;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('top_k', resultsCount);

        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        // Show AI Insights
        document.getElementById('ocr-result').innerText = data.ocr_text || "No text detected";
        document.getElementById('vision-result').innerText = data.analysis;
        document.getElementById('ai-insight').classList.remove('hidden');

        renderResults(data.results);
    } catch (error) {
        console.error(error);
        alert("Error analyzing image.");
    }
    showLoader(false);
}

// --- UTILS ---
function showLoader(show, text) {
    const loader = document.getElementById('loader');
    loader.classList.toggle('hidden', !show);
    if (text) document.getElementById('loading-text').innerText = text;
}

function renderResults(results) {
    const grid = document.getElementById('results-grid');
    grid.innerHTML = "";

    if (results.length === 0) {
        grid.innerHTML = "<p style='color:#777; grid-column: 1/-1; text-align:center;'>No results found.</p>";
        return;
    }

    results.forEach(item => {
        // Calculate score percentage and color
        const scorePercent = Math.round((item.score || 0) * 100);
        let scoreColor = '#4caf50'; // Green
        if (scorePercent < 80) scoreColor = '#ff9800'; // Orange
        if (scorePercent < 60) scoreColor = '#f44336'; // Red

        const card = `
            <div class="card">
                <div class="score-badge" style="background-color: ${scoreColor}">
                    ${scorePercent}% Match
                </div>
                <img src="/images/${item.image_name}" alt="${item.caption}" class="card-image">
                <div class="card-body">
                    <div class="card-category">${item.category}</div>
                    <div class="card-caption">${item.caption}</div>
                    <div class="card-meta">
                        <span>${item.material}</span>
                        <span>${item.style}</span>
                    </div>
                </div>
            </div>
        `;
        grid.innerHTML += card;
    });
}