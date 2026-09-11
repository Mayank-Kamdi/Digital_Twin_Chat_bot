/**
 * LYRA Business Digital Twin - Client Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Generate or retrieve session ID
  let sessionId = localStorage.getItem("lyra_session_id");
  if (!sessionId) {
    sessionId = "session_" + Math.random().toString(36).substring(2, 9) + "_" + Date.now();
    localStorage.setItem("lyra_session_id", sessionId);
  }

  // DOM Elements
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const typingIndicator = document.getElementById("typing-indicator");
  const btnClearChat = document.getElementById("btn-clear-chat");
  const memoryBar = document.getElementById("memory-context-bar");
  const memoryTags = document.getElementById("memory-tags");
  const quickPrompts = document.querySelectorAll(".chip");

  // Admin Modal Elements
  const btnAdminToggle = document.getElementById("btn-admin-toggle");
  const btnCloseAdmin = document.getElementById("btn-close-admin");
  const adminModal = document.getElementById("admin-modal");
  const adminTabs = document.querySelectorAll(".admin-tab");
  const adminTabContents = document.querySelectorAll(".admin-tab-content");
  const adminStatusMsg = document.getElementById("admin-status-msg");

  // Admin Forms
  const formFaq = document.getElementById("form-faq");
  const formPolicy = document.getElementById("form-policy");
  const formProduct = document.getElementById("form-product");
  const formDocument = document.getElementById("form-document");

  // Scroll messages container to bottom
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Render a chat message bubble
  function appendMessage(sender, text, sources = [], isGuarded = false) {
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${sender === "user" ? "user-bubble" : "assistant-bubble"}`;

    const senderLabel = document.createElement("div");
    senderLabel.className = "sender-name";
    senderLabel.textContent = sender === "user" ? "You" : "LYRA Twin";
    bubble.appendChild(senderLabel);

    const messageText = document.createElement("div");
    messageText.className = "message-text";
    
    // Simple markdown formatting for bold and lists
    let formattedText = escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>");
    messageText.innerHTML = formattedText;
    bubble.appendChild(messageText);

    // Citations / Sources transparency
    if (sources && sources.length > 0 && sender !== "user") {
      const citationsDiv = document.createElement("div");
      citationsDiv.className = "source-citations";
      citationsDiv.innerHTML = "<strong>Verified Sources:</strong> ";
      sources.slice(0, 3).forEach(src => {
        const item = document.createElement("span");
        item.className = "source-item";
        item.textContent = `${src.title} (${Math.round(src.score * 100)}%)`;
        citationsDiv.appendChild(item);
      });
      bubble.appendChild(citationsDiv);
    }

    chatMessages.appendChild(bubble);
    scrollToBottom();
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // Update Memory Context Display
  function updateMemoryDisplay(requirements, mentionedProducts) {
    const tags = [];
    if (requirements && requirements.business_type) {
      tags.push(`Type: ${requirements.business_type}`);
    }
    if (requirements && requirements.needs && requirements.needs.length > 0) {
      tags.push(`Need: ${requirements.needs.join(", ")}`);
    }
    if (mentionedProducts && mentionedProducts.length > 0) {
      tags.push(`Discussed: ${mentionedProducts.join(", ")}`);
    }

    if (tags.length > 0) {
      memoryBar.classList.remove("hidden");
      memoryTags.innerHTML = tags.map(t => `<span class="memory-tag">${escapeHtml(t)}</span>`).join(" ");
    } else {
      memoryBar.classList.add("hidden");
      memoryTags.innerHTML = "";
    }
  }

  // Send message to API
  async function sendMessage(text) {
    if (!text.trim()) return;

    // Show user message
    appendMessage("user", text);
    chatInput.value = "";
    typingIndicator.classList.remove("hidden");
    scrollToBottom();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          message: text
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();
      typingIndicator.classList.add("hidden");

      // Show assistant response
      appendMessage("assistant", data.answer, data.sources, data.is_hallucination_guarded);

      // Update active memory bar
      updateMemoryDisplay(data.active_requirements, data.mentioned_products);

    } catch (err) {
      typingIndicator.classList.add("hidden");
      appendMessage("assistant", "I experienced a temporary communication issue. Please try again shortly.");
      console.error("Chat error:", err);
    }
  }

  // Form submit handler
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (query) {
      sendMessage(query);
    }
  });

  // Quick prompt chip handlers
  quickPrompts.forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-q");
      if (q) {
        sendMessage(q);
      }
    });
  });

  // Clear conversation handler
  btnClearChat.addEventListener("click", async () => {
    if (confirm("Clear conversation history and memory?")) {
      try {
        await fetch("/api/chat/clear", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId })
        });
        chatMessages.innerHTML = `
          <div class="message-bubble assistant-bubble">
            <div class="sender-name">LYRA Twin</div>
            <div class="message-text">
              Conversation memory has been cleared. How can I assist you with LYRA today?
            </div>
          </div>
        `;
        memoryBar.classList.add("hidden");
        memoryTags.innerHTML = "";
      } catch (err) {
        console.error("Failed to clear memory:", err);
      }
    }
  });

  // Admin Modal Logic
  btnAdminToggle.addEventListener("click", () => {
    adminModal.classList.remove("hidden");
    adminStatusMsg.textContent = "";
  });

  btnCloseAdmin.addEventListener("click", () => {
    adminModal.classList.add("hidden");
  });

  adminModal.addEventListener("click", (e) => {
    if (e.target === adminModal) {
      adminModal.classList.add("hidden");
    }
  });

  // Admin Tabs
  adminTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      adminTabs.forEach(t => t.classList.remove("active"));
      adminTabContents.forEach(c => c.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-target");
      document.getElementById(targetId).classList.add("active");
      adminStatusMsg.textContent = "";
    });
  });

  function showAdminStatus(msg, isError = false) {
    adminStatusMsg.textContent = msg;
    adminStatusMsg.className = `admin-status-msg ${isError ? "error" : "success"}`;
  }

  // Handle FAQ addition
  formFaq.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = document.getElementById("faq-question").value.trim();
    const a = document.getElementById("faq-answer").value.trim();
    try {
      const resp = await fetch("/api/admin/faq", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, answer: a })
      });
      if (resp.ok) {
        showAdminStatus("✓ FAQ successfully added and indexed in vector store!");
        formFaq.reset();
      } else {
        showAdminStatus("Failed to add FAQ.", true);
      }
    } catch (err) {
      showAdminStatus("Error adding FAQ.", true);
    }
  });

  // Handle Policy addition
  formPolicy.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("policy-title").value.trim();
    const summary = document.getElementById("policy-summary").value.trim();
    const details = document.getElementById("policy-details").value.trim();
    try {
      const resp = await fetch("/api/admin/policy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, summary, details, category: "custom_policy" })
      });
      if (resp.ok) {
        showAdminStatus("✓ Policy successfully added and indexed in vector store!");
        formPolicy.reset();
      } else {
        showAdminStatus("Failed to add policy.", true);
      }
    } catch (err) {
      showAdminStatus("Error adding policy.", true);
    }
  });

  // Handle Product addition
  formProduct.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("prod-name").value.trim();
    const category = document.getElementById("prod-category").value.trim();
    const summary = document.getElementById("prod-summary").value.trim();
    const best_for = document.getElementById("prod-bestfor").value.trim();
    const pricingStr = document.getElementById("prod-pricing").value.trim();
    try {
      const resp = await fetch("/api/admin/product", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          category,
          summary,
          best_for,
          pricing: { "Standard": pricingStr },
          features: ["Custom integration", "Standard SLA"]
        })
      });
      if (resp.ok) {
        showAdminStatus("✓ Product successfully added and indexed in vector store!");
        formProduct.reset();
      } else {
        showAdminStatus("Failed to add product.", true);
      }
    } catch (err) {
      showAdminStatus("Error adding product.", true);
    }
  });

  // Handle Document addition
  formDocument.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("doc-title").value.trim();
    const content = document.getElementById("doc-content").value.trim();
    try {
      const resp = await fetch("/api/admin/document", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content, category: "custom_doc" })
      });
      if (resp.ok) {
        showAdminStatus("✓ Document successfully added and indexed in vector store!");
        formDocument.reset();
      } else {
        showAdminStatus("Failed to add document.", true);
      }
    } catch (err) {
      showAdminStatus("Error adding document.", true);
    }
  });
});
