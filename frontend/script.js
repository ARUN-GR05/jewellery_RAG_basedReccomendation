// ⚠️ CHANGE THIS TO YOUR RENDER URL AFTER DEPLOYMENT
const API_BASE = "http://127.0.0.1:8000";

// --- TAB SWITCHING ---
function switchTab(mode) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

    // Updated selector for new structure
    const activeBtn = document.querySelector(`.tab-btn[onclick="switchTab('${mode}')"]`);
    if (activeBtn) activeBtn.classList.add('active');

    const activePanel = document.getElementById(`${mode}-panel`);
    if (activePanel) activePanel.classList.add('active');
}

// --- FILE UPLOAD HANDLING ---
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

if (dropZone) {
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag & Drop Support
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--gold)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = '#444';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#444';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect(file);
        }
    });
}

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileSelect(file);
});

function handleFileSelect(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('image-preview').src = e.target.result;
        document.getElementById('drop-zone').classList.add('hidden');
        document.getElementById('preview-container').classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

function resetUpload() {
    fileInput.value = "";
    document.getElementById('image-preview').src = "";
    document.getElementById('drop-zone').classList.remove('hidden');
    document.getElementById('preview-container').classList.add('hidden');
    document.getElementById('ai-insight').classList.add('hidden');
}

// --- ENTER KEY SUPPORT ---
const queryInput = document.getElementById('query-input');
if (queryInput) {
    queryInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            runTextSearch();
        }
    });
}

// --- API CALLS ---

async function runTextSearch() {
    const query = document.getElementById('query-input').value;
    if (!query) return;

    showLoader(true, "Consulting our collection...");

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
        document.getElementById('ai-insight').classList.add('hidden');
    } catch (error) {
        console.error(error);
        alert("Connectivity issue. Please ensure the vault is accessible (backend running).");
    }
    showLoader(false);
}

async function runImageSearch() {
    const file = fileInput.files[0];
    if (!file) return;

    showLoader(true, "Synthesizing visual and textual data...");

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
        document.getElementById('ocr-result').innerText = data.ocr_text || "Undetected";
        document.getElementById('vision-result').innerText = data.analysis;
        document.getElementById('ai-insight').classList.remove('hidden');

        renderResults(data.results);
    } catch (error) {
        console.error(error);
        alert("Neural synthesis failed. Please try another image.");
    }
    showLoader(false);
}

// --- UTILS ---
function showLoader(show, text) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.toggle('hidden', !show);
        if (text) document.getElementById('loading-text').innerText = text;
    }
}

function renderResults(results) {
    const grid = document.getElementById('results-grid');
    if (!grid) return;

    grid.innerHTML = "";

    if (!results || results.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align:center; padding: 60px; color: var(--text-muted);">
                <p style="font-size: 1.2rem; font-family: 'Playfair Display', serif;">The collection does not currently contain a match for your request.</p>
                <p style="font-size: 0.8rem; margin-top: 10px; letter-spacing: 1px; text-transform: uppercase;">Try adjusting your description</p>
            </div>
        `;
        return;
    }

    results.forEach(item => {
        const scorePercent = Math.round((item.score || 0) * 100);

        const card = `
            <div class="card" style="animation: fadeInUp 0.6s ease-out forwards;">
                <div class="card-image-wrapper">
                    <img src="/images/${item.image_name}" alt="${item.caption}" class="card-image" onerror="this.src='https://via.placeholder.com/400x400?text=Jewellery+Item'">
                    <div class="score-badge">
                        ${scorePercent}% Match
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-category">${item.category}</div>
                    <h3 class="card-caption">${item.caption}</h3>
                    <div class="card-meta">
                        <span>${item.material}</span>
                        <span>${item.style}</span>
                    </div>
                </div>
            </div>
        `;
        grid.insertAdjacentHTML('beforeend', card);
    });
}
