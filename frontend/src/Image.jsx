import React, { useState } from "react";
import {
    Wand2,
    Copy,
    RefreshCw,
    X,
    Sparkles,
    Image as ImageIcon,
    Palette,
    Sun,
    Moon,
    Camera,
    Save,
} from "lucide-react";


const PromptGenieApp = () => {
    const [currentPage, setCurrentPage] = useState("home");
    const [darkMode, setDarkMode] = useState(true);
    const [formData, setFormData] = useState({
        subject: "",
        style: "",
        mood: "",
        lighting: "",
        composition: "",
        detailLevel: "",
        artistReference: "",
    });
    const [generatedPrompt, setGeneratedPrompt] = useState("");
    const [toastMessage, setToastMessage] = useState("");
    const [showToast, setShowToast] = useState(false);

    const showToastMsg = (msg) => {
        setToastMessage(msg);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 2500);
    };

    const generatePrompt = async () => {
        if (!formData.subject.trim()) {
            showToastMsg("⚠️ Please describe your scene first!");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/prompt/build", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    subject: formData.subject,
                    style: formData.style,
                    mood: formData.mood,
                    lighting: formData.lighting,
                    composition: formData.composition,
                    detail_level: formData.detailLevel,
                    artist_reference: formData.artistReference,
                }),
            });

            const data = await response.json();
            setGeneratedPrompt(data.prompt);
            showToastMsg("✨ Prompt generated successfully!");
        } catch (err) {
            setGeneratedPrompt(
                `${formData.subject}, ${formData.style}, ${formData.mood}.`
            );
            showToastMsg("✨ Local prompt created!");
        }
    };

    const copyPrompt = () => {
        navigator.clipboard.writeText(generatedPrompt);
        showToastMsg("📋 Copied to clipboard!");
    };

    return (
        <div className={`app-container ${darkMode ? "dark" : "light"}`}>
            <header className="header">
                <div className="logo" onClick={() => setCurrentPage("home")}>
                    <ImageIcon className="logo-icon" />
                    <span>PromptGenie</span>
                </div>
                <nav className="nav-links">
                    <button onClick={() => setCurrentPage("home")}>Home</button>
                    <button onClick={() => setCurrentPage("generator")}>Generate</button>
                    <button onClick={() => setDarkMode(!darkMode)} className="theme-btn">
                        {darkMode ? <Sun /> : <Moon />}
                    </button>
                </nav>
            </header>

            <main className="main-content">
                {currentPage === "home" && (
                    <div className="hero-section">
                        <Sparkles className="hero-icon" />
                        <h1>Turn ideas into perfect AI prompts</h1>
                        <p>Choose a style, describe your idea, and get studio-quality prompts.</p>
                        <button
                            className="button-primary"
                            onClick={() => setCurrentPage("generator")}
                        >
                            <Wand2 /> Start Generating
                        </button>
                    </div>
                )}

                {currentPage === "generator" && (
                    <div className="generator">
                        <div className="generator-left">
                            <h2>
                                <Palette /> Create Your Prompt
                            </h2>
                            <label>Scene Description *</label>
                            <textarea
                                value={formData.subject}
                                onChange={(e) =>
                                    setFormData({ ...formData, subject: e.target.value })
                                }
                                placeholder="A woman reading a book near a window"
                            />
                            <label>Style</label>
                            <input
                                type="text"
                                value={formData.style}
                                onChange={(e) =>
                                    setFormData({ ...formData, style: e.target.value })
                                }
                                placeholder="Cinematic, Realistic..."
                            />
                            <label>Mood</label>
                            <input
                                type="text"
                                value={formData.mood}
                                onChange={(e) =>
                                    setFormData({ ...formData, mood: e.target.value })
                                }
                                placeholder="Serene, Dramatic..."
                            />
                            <label>Lighting</label>
                            <input
                                type="text"
                                value={formData.lighting}
                                onChange={(e) =>
                                    setFormData({ ...formData, lighting: e.target.value })
                                }
                                placeholder="Golden hour, soft light..."
                            />
                            <button className="button-primary" onClick={generatePrompt}>
                                <Wand2 /> Generate
                            </button>
                        </div>

                        <div className="generator-right">
                            <h2>
                                <Sparkles /> Your Generated Prompt
                            </h2>
                            <div className="output-box">
                                {generatedPrompt || "Your generated prompt will appear here..."}
                            </div>
                            <button
                                className="button-secondary"
                                onClick={copyPrompt}
                                disabled={!generatedPrompt}
                            >
                                <Copy /> Copy
                            </button>
                            <div className="preview-box">
                                <Camera className="preview-icon" />
                                <p>Preview area - use this prompt in your AI generator</p>
                            </div>
                        </div>
                    </div>
                )}
            </main>

            <footer className="footer">
                <p>© 2025 PromptGenie AI Tools</p>
            </footer>

            {showToast && <div className="toast">{toastMessage}</div>}
        </div>
    );
};

export default PromptGenieApp;
