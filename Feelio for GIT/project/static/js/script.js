let allImages = [
    "069783892c86935418e40b3975d243e1.jpg",
    "0acf22a2af34083164d14c8aaca764c1.jpg",
    "18fe47517cf7d89a4f636be4cbf7887d.jpg",
    "1af4827b82c1d4d775d3b29937dbca27.jpg",
    "20f8143395cbd94a17b13c2d74d76443.jpg",
    "223ca6eed2d26fc5a64703f9486b4dce.jpg",
    "3710051b520642a4bf073e2f1b308f30.jpg",
    "3e940dc2772e85944a378f087459c5b7.jpg",
    "4e86625bf5690d7a0d0f8de0bca6102f.jpg",
    "5b8a5c5c578077f39967dff2f23a604d.jpg",
    "5d19ecbcbbe041676b515304d8af3c9a.jpg",
    "62e89542ee3a9a22c3648585883baa78.jpg",
    "70e4d3e17574bd31ae77714f3f7caae1.jpg",
    "852269e66a29df4f5c36219a13063e3b.jpg",
    "8b2de90cb1c605e40823071ebd945101.jpg",
    "912750b850b7a994e567850d4cf03b27.jpg",
    "91cb34032c6caa1452bc39a5ab044636.jpg",
    "9505f46b22cb8621d7555bfe81860def.jpg",
    "9b7447105ba307bee473aa0d8516fe91.jpg",
    "9be956153ef3ec6e1c65a411a58b84bb.jpg",
    "bc075135976c4291b6817a5b80265e45.jpg",
    "cad5db42db0507061dc03a0eca4b9231.jpg",
    "calm1.jpg",
    "calm2.jpg",
    "da7c98808af7dce9c5f1f7ec1a040ecf.jpg",
    "default.jpg",
    "e16e41add89cb3f84afb831c88721abe.jpg",
    "eb15647c44bbd40bd5a90ae0f75370f2.jpg",
    "ed92a17dc807ccbf433655a0a532c0f0.jpg",
    "energy1.jpg",
    "energy2.jpg",
    "happy1.jpg",
    "happy2.jpg",
    "happy3.jpg",
    "sad1.jpg",
    "sad2.jpg"
];
let isRepeating = false;
let songHistory = [];
let lastImage = "";
let lastUserInput = {}; 
let audioCtx, analyser, source;
let animationId = null;
let isVisualizing = false;

function getRandomImage() {
    let randomImage;
    do {
        randomImage = allImages[Math.floor(Math.random() * allImages.length)];
    } while (randomImage === lastImage && allImages.length > 1);
    lastImage = randomImage;
    return randomImage;
}

async function predictMood(inputData = null) {
    const inputs = ["sleep", "energy", "stress", "social", "positivity"];
    let data = inputData;

    if (!data) {
        data = {};
        inputs.forEach(id => {
            data[id] = document.getElementById(id).value;
        });
        
        // If inputs are empty, try using last stored input
        const isEmpty = Object.values(data).every(v => v === "");
        if (isEmpty && Object.keys(lastUserInput).length > 0) {
            data = lastUserInput;
        } else {
            lastUserInput = { ...data }; 
        }
    }

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!res.ok) {
            const errData = await res.json();
            alert(errData.error || "Something went wrong on the server.");
            return;
        }

        const result = await res.json();
        if (result.song_path) {
            displaySong(result);
            document.body.classList.add("song-page");
            // Clear inputs
            inputs.forEach(id => document.getElementById(id).value = "");
        } else {
            alert("No song found for this mood. Please try again!");
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Failed to connect to the server.");
    }
}

function displaySong(data, addToHistory = true) {
    const audio = document.getElementById("audioPlayer");
    const playBtn = document.getElementById("playPauseBtn");
    const resultSection = document.getElementById("resultSection");
    const formSection = document.getElementById("formSection");

    // Store current song in history BEFORE changing
    if (addToHistory && audio.src && !audio.src.includes("null")) {
        const currentData = {
            song_path: audio.getAttribute("data-path"), // Store the relative path
            mood: document.getElementById("moodText").innerText.replace("Mood: ", ""),
            quote: document.getElementById("quote").innerText,
            bgClass: document.body.className
        };
        songHistory.push(currentData);
        if (songHistory.length > 20) songHistory.shift(); // Keep history manageable
    }

    // Update UI
    document.body.className = data.mood.toLowerCase();
    audio.src = data.song_path;
    audio.setAttribute("data-path", data.song_path);
    audio.load();

    document.getElementById("songName").innerText = data.song_path.split("/").pop().replace(".mp3", "");
    document.getElementById("songImage").src = "/static/images/" + getRandomImage();
    document.getElementById("moodText").innerText = "Mood: " + data.mood;
    
    const quoteEl = document.getElementById("quote");
    quoteEl.innerText = data.quote;
    quoteEl.style.opacity = 0;
    quoteEl.style.transform = "translateY(10px)";

    // Transitions
    if (resultSection.classList.contains("hidden")) {
        formSection.classList.add("slide-up-hide");
        setTimeout(() => {
            formSection.classList.add("hidden");
            resultSection.classList.remove("hidden");
            void resultSection.offsetWidth;
            resultSection.classList.add("slide-up-show");
            resultSection.classList.remove("initial-slide-down");
            const resultCard = resultSection.querySelector(".glass-card");
            resultCard.classList.add("result-card");
            setTimeout(() => resultCard.classList.add("active"), 100);
        }, 500);
    }

    setTimeout(() => {
        quoteEl.style.opacity = 1;
        quoteEl.style.transform = "translateY(0)";
    }, 600);

    // Setup Visualizer & Play
    const startAudio = () => {
        setupVisualizer(audio);
        if (audioCtx) audioCtx.resume();
        audio.play().then(() => {
            playBtn.innerText = "⏸️";
            drawVisualizer();
        }).catch(e => {
            console.log("Autoplay blocked:", e);
            playBtn.innerText = "▶️";
        });
    };

    if (resultSection.classList.contains("hidden")) {
        // Special case: Wait for animation if it was hidden
        setTimeout(startAudio, 600);
    } else {
        startAudio();
    }

    setupControls(audio);
}

function setupControls(audio) {
    const playBtn = document.getElementById("playPauseBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const repeatBtn = document.getElementById("repeatBtn");
    const progressBar = document.getElementById("progressBar");
    const currentTimeEl = document.getElementById("currentTime");
    const durationEl = document.getElementById("duration");

    playBtn.onclick = () => {
        if (audio.paused) {
            setupVisualizer(audio);
            if (audioCtx) audioCtx.resume();
            audio.play();
            playBtn.innerText = "⏸️";
            drawVisualizer();
        } else {
            audio.pause();
            playBtn.innerText = "▶️";
        }
    };

    nextBtn.onclick = () => {
        predictMood(); // Simplest way to get a new random song for the same mood logic
    };

    prevBtn.onclick = () => {
        if (songHistory.length > 0) {
            const prevSong = songHistory.pop();
            displaySong(prevSong, false);
        } else {
            audio.currentTime = 0;
            audio.play();
        }
    };

    repeatBtn.onclick = () => {
        isRepeating = !isRepeating;
        repeatBtn.classList.toggle("active-control", isRepeating);
    };

    audio.onended = () => {
        if (isRepeating) {
            audio.currentTime = 0;
            audio.play();
        } else {
            nextBtn.onclick();
        }
    };

    audio.ontimeupdate = () => {
        if (isNaN(audio.duration)) return;
        const progress = (audio.currentTime / audio.duration) * 100;
        progressBar.value = progress || 0;
        const minutes = Math.floor(audio.currentTime / 60);
        const seconds = Math.floor(audio.currentTime % 60).toString().padStart(2, "0");
        currentTimeEl.innerText = `${minutes}:${seconds}`;
    };

    audio.onloadedmetadata = () => {
        const minutes = Math.floor(audio.duration / 60);
        const seconds = Math.floor(audio.duration % 60).toString().padStart(2, "0");
        durationEl.innerText = `${minutes}:${seconds}`;
    };

    progressBar.oninput = () => {
        if (audio.duration) {
            audio.currentTime = (progressBar.value / 100) * audio.duration;
        }
    };
}

async function sendFeedback(isCorrect) {
    const moodText = document.getElementById("moodText").innerText;
    const mood = moodText.replace("Mood: ", "");
    const res = await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood: mood, correct: isCorrect })
    });
    const result = await res.json();
    document.getElementById("feedbackMsg").innerText = result.message;
}

// 3. INITIALIZE VISUALIZER ONLY ONCE
function setupVisualizer(audio) {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        try {
            source = audioCtx.createMediaElementSource(audio);
            source.connect(analyser);
            analyser.connect(audioCtx.destination);
        } catch (e) {
            console.log("Visualizer connection already exists or failed:", e);
        }
        analyser.fftSize = 256;
    }

    // Always ensure canvas is sized correctly
    const canvas = document.getElementById("visualizer");
    if (canvas) {
        const resizeCanvas = () => {
            if (canvas.offsetWidth > 0) {
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;
            }
        };
        // Ensure we handle future resizing
        if (!window.visualizerResizeAttached) {
            window.addEventListener("resize", resizeCanvas);
            window.visualizerResizeAttached = true;
        }
        resizeCanvas();
    }
}

function drawVisualizer() {
    const canvas = document.getElementById("visualizer");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    const audio = document.getElementById("audioPlayer");

    // Cancel any existing animation frame to prevent overlapping loops
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }

    function renderFrame() {
        if (audio.paused) {
            isVisualizing = false;
            // Optionally clear canvas when paused or keep the last frame
            // ctx.clearRect(0, 0, canvas.width, canvas.height); 
            return;
        }
        
        isVisualizing = true;
        animationId = requestAnimationFrame(renderFrame);
        analyser.getByteFrequencyData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const barWidth = (canvas.width / bufferLength) * 2;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const barHeight = dataArray[i] / 2;
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, "#22c55e");
            gradient.addColorStop(1, "#4ade80");

            ctx.fillStyle = gradient;
            ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
            x += barWidth + 1;
        }
    }

    renderFrame();
}