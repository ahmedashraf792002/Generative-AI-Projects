let statusTimer = null;
let isAnalyzing = false;
let isReady = false;
let isSending = false;

const els = {};

document.addEventListener("DOMContentLoaded", () => {
  [
    "playlistUrl",
    "resetChat",
    "analyzeBtn",
    "analyzeBtnText",
    "statusCard",
    "statusText",
    "progressBar",
    "suggestionsList",
    "clearChatBtn",
    "questionForm",
    "questionInput",
    "sendBtn",
    "chatWindow",
    "messages",
    "welcome",
    "readyPill",
    "headerSubtitle",
    "sidebar",
    "menuBtn",
  ].forEach((id) => {
    els[id] = document.getElementById(id);
  });

  els.analyzeBtn.addEventListener("click", analyzePlaylist);
  els.clearChatBtn.addEventListener("click", clearChat);
  els.questionForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendQuestion();
  });
  els.questionInput.addEventListener("input", () => autoResize(els.questionInput));
  els.questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendQuestion();
    }
  });
  els.menuBtn.addEventListener("click", () => els.sidebar.classList.toggle("open"));

  loadHistory();
  checkStatus();
});

async function analyzePlaylist() {
  const playlistUrl = els.playlistUrl.value.trim();
  if (!playlistUrl) {
    showStatus("Please enter a playlist URL.", 0, "error");
    return;
  }
  if (isAnalyzing) return;

  isAnalyzing = true;
  isReady = false;
  setAnalysisUi(true);
  setChatEnabled(false);
  renderSuggestions([]);
  showStatus("🔄 Analyzing playlist...", 3, "loading");
  setReadyState("Analyzing", "loading");

  if (els.resetChat.checked) {
    clearMessages();
  }

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        playlist_url: playlistUrl,
        reset_chat: els.resetChat.checked,
      }),
    });
    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Could not start analysis.");
    }

    clearInterval(statusTimer);
    statusTimer = setInterval(pollStatus, 1500);
    pollStatus();
  } catch (error) {
    isAnalyzing = false;
    setAnalysisUi(false);
    setReadyState("Not ready", "idle");
    showStatus(error.message, 0, "error");
  }
}

async function pollStatus() {
  try {
    const data = await fetchJson("/status");

    showStatus(data.progress_message || "Analyzing playlist...", data.progress_percent || 0, data.error ? "error" : "loading");

    if (data.is_loading) {
      setReadyState("Analyzing", "loading");
      return;
    }

    clearInterval(statusTimer);
    statusTimer = null;
    isAnalyzing = false;
    setAnalysisUi(false);

    if (data.error) {
      isReady = false;
      setChatEnabled(false);
      setReadyState("Not ready", "idle");
      showStatus(data.error, 0, "error");
      return;
    }

    if (data.is_ready) {
      isReady = true;
      setChatEnabled(true);
      setReadyState("Ready", "ready");
      showStatus("Playlist analyzed successfully.", 100, "success");
      renderSuggestions(data.suggested_questions || []);
      updateStats(data.stats || {});
      hideWelcomeIfNeeded();
    }
  } catch (_error) {
    // Keep polling through brief connection hiccups.
  }
}

async function checkStatus() {
  try {
    const data = await fetchJson("/status");
    if (data.is_loading) {
      isAnalyzing = true;
      setAnalysisUi(true);
      setChatEnabled(false);
      setReadyState("Analyzing", "loading");
      showStatus(data.progress_message || "🔄 Analyzing playlist...", data.progress_percent || 3, "loading");
      clearInterval(statusTimer);
      statusTimer = setInterval(pollStatus, 1500);
      return;
    }

    if (data.is_ready) {
      isReady = true;
      setChatEnabled(true);
      setReadyState("Ready", "ready");
      renderSuggestions(data.suggested_questions || []);
      updateStats(data.stats || {});
      showStatus("Playlist analyzed successfully.", 100, "success");
    }
  } catch (_error) {
    setChatEnabled(false);
  }
}

function setAnalysisUi(active) {
  els.analyzeBtn.disabled = active;
  els.analyzeBtn.classList.toggle("is-loading", active);
  els.analyzeBtnText.textContent = active ? "Analyzing..." : "Analyze Playlist";
  els.playlistUrl.disabled = active;
  els.resetChat.disabled = active;
}

function setChatEnabled(enabled) {
  els.questionInput.disabled = !enabled || isSending;
  els.sendBtn.disabled = !enabled || isSending;
  if (enabled && !isSending) els.questionInput.focus();
}

function setReadyState(text, state) {
  els.readyPill.textContent = text;
  els.readyPill.className = `ready-pill ${state}`;
}

function showStatus(message, percent, type) {
  els.statusCard.hidden = false;
  els.statusCard.className = `status-card ${type}`;
  els.statusText.textContent = message;
  els.progressBar.style.width = `${Math.max(0, Math.min(100, percent || 0))}%`;
}

function updateStats(stats) {
  if (!stats.video_count) return;
  els.headerSubtitle.textContent = `${stats.video_count} videos analyzed, ${stats.chunk_count || 0} transcript chunks indexed.`;
}

function renderSuggestions(questions) {
  els.suggestionsList.innerHTML = "";

  if (!questions.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = isAnalyzing ? "New suggested questions will appear after analysis." : "Analyze a playlist to generate study questions.";
    els.suggestionsList.appendChild(empty);
    return;
  }

  questions.slice(0, 5).forEach((question) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "suggestion-btn";
    button.textContent = question;
    button.addEventListener("click", () => askSuggestedQuestion(question));
    els.suggestionsList.appendChild(button);
  });
}

function askSuggestedQuestion(question) {
  if (!isReady || isSending || isAnalyzing) return;
  els.questionInput.value = question;
  autoResize(els.questionInput);
  sendQuestion();
}

async function sendQuestion() {
  const question = els.questionInput.value.trim();
  if (!question || !isReady || isSending || isAnalyzing) return;

  isSending = true;
  setChatEnabled(false);
  els.questionInput.value = "";
  autoResize(els.questionInput);
  hideWelcomeIfNeeded();

  const clientTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  appendMessage("user", question, clientTime);
  const typing = appendTyping();

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    typing.remove();

    if (!response.ok || !data.success) {
      appendMessage("assistant", data.error || "Something went wrong.", clientTime);
    } else {
      appendMessage("assistant", data.answer, data.timestamp || clientTime);
    }
  } catch (_error) {
    typing.remove();
    appendMessage("assistant", "Network error. Please try again.", clientTime);
  } finally {
    isSending = false;
    setChatEnabled(isReady && !isAnalyzing);
    scrollToBottom();
  }
}

function appendMessage(role, content, timestamp) {
  const row = document.createElement("article");
  row.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = `${role === "user" ? "You" : "Assistant"} • ${timestamp || ""}`;

  row.appendChild(bubble);
  row.appendChild(meta);
  els.messages.appendChild(row);
  scrollToBottom();
}

function appendTyping() {
  const row = document.createElement("article");
  row.className = "message assistant typing";
  row.innerHTML = '<div class="bubble typing-bubble"><span></span><span></span><span></span></div>';
  els.messages.appendChild(row);
  scrollToBottom();
  return row;
}

async function loadHistory() {
  try {
    const data = await fetchJson("/history");
    (data.history || []).forEach((message) => {
      appendMessage(message.role, message.content, message.timestamp || message.time || "");
    });
    if ((data.history || []).length) hideWelcomeIfNeeded();
  } catch (_error) {
    // History is a convenience, not a blocker.
  }
}

async function clearChat() {
  try {
    await fetch("/clear_chat", { method: "POST" });
  } finally {
    clearMessages();
  }
}

function clearMessages() {
  els.messages.innerHTML = "";
  els.welcome.hidden = false;
}

function hideWelcomeIfNeeded() {
  els.welcome.hidden = true;
}

function scrollToBottom() {
  els.chatWindow.scrollTo({ top: els.chatWindow.scrollHeight, behavior: "smooth" });
}

function autoResize(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
}

async function fetchJson(url) {
  const response = await fetch(url);
  return response.json();
}
