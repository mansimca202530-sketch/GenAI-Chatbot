// ============================================================
// GLOBAL VARIABLES
// ============================================================

let selectedModel = "llama";

let uploadedPDF = null;


// ============================================================
// MODEL SELECTION
// ============================================================

function selectModel(model) {

    selectedModel = model;


    // Remove active state

    document
        .querySelectorAll(".model-card")
        .forEach(card => {

            card.classList.remove("active");

        });


    // Add active state

    const selectedCard =
        document.querySelector(
            `.model-card[data-model="${model}"]`
        );


    if (selectedCard) {

        selectedCard.classList.add("active");

    }


    const title =
        document.getElementById("chatTitle");

    const currentModel =
        document.getElementById("currentModel");


    // LLaMA

    if (model === "llama") {

        title.textContent =
            "LLaMA 3.2 Assistant";

        currentModel.textContent =
            "LLaMA 3.2";

    }


    // DeepSeek

    else if (model === "deepseek") {

        title.textContent =
            "DeepSeek V3 Assistant";

        currentModel.textContent =
            "DeepSeek V3";

    }


    // PDF

    else if (model === "pdf") {

        title.textContent =
            "PDF Assistant";

        currentModel.textContent =
            "PDF RAG";

    }


    // Show PDF panel

    const pdfPanel =
        document.getElementById("pdfPanel");


    if (model === "pdf") {

        pdfPanel.classList.add("show");

    }

    else {

        pdfPanel.classList.remove("show");

    }

}


// ============================================================
// OPEN PDF SELECTOR
// ============================================================

function openPDFSelector() {

    // Automatically switch to PDF mode

    selectModel("pdf");


    document
        .getElementById("pdfFile")
        .click();

}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const input =
        document.getElementById("messageInput");


    const message =
        input.value.trim();


    if (!message) {

        return;

    }


    // PDF mode requires uploaded PDF

    if (
        selectedModel === "pdf" &&
        !uploadedPDF
    ) {

        addMessage(
            "Please upload a PDF first.",
            "ai"
        );

        return;

    }


    // Hide welcome screen

    hideWelcome();


    // Add user message

    addMessage(
        message,
        "user"
    );


    // Clear input

    input.value = "";

    autoResize(input);


    // Disable send button

    const sendButton =
        document.getElementById(
            "sendButton"
        );


    sendButton.disabled = true;


    // Show typing

    const typingID =
        showTyping();


    try {


        // ==================================================
        // SEND REQUEST TO MAIN.PY
        // ==================================================

        const response =
            await fetch(
                "/chat",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        message: message,

                        model: selectedModel,

                        pdf_path: uploadedPDF

                    })

                }
            );


        // Convert response to JSON

        const data =
            await response.json();


        // Remove typing

        removeTyping(
            typingID
        );


        // ==================================================
        // SUCCESS
        // ==================================================

        if (data.success) {

            addMessage(
                data.answer,
                "ai"
            );

        }


        // ==================================================
        // BACKEND ERROR
        // ==================================================

        else {

            addMessage(
                "⚠️ " + data.error,
                "ai"
            );

        }


    }


    catch (error) {


        removeTyping(
            typingID
        );


        addMessage(
            "⚠️ Unable to connect to the backend.",
            "ai"
        );


        console.error(
            "Backend error:",
            error
        );

    }


    sendButton.disabled = false;

}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    text,
    sender
) {

    const container =
        document.getElementById(
            "chatMessages"
        );


    const row =
        document.createElement(
            "div"
        );


    row.className =
        `message-row ${sender}`;


    const avatar =
        document.createElement(
            "div"
        );


    avatar.className =
        `avatar ${sender}-avatar`;


    avatar.textContent =
        sender === "ai"
            ? "✦"
            : "👤";


    const content =
        document.createElement(
            "div"
        );


    content.className =
        "message-content";


    const name =
        document.createElement(
            "div"
        );


    name.className =
        "message-name";


    name.textContent =
        sender === "ai"
            ? getModelName()
            : "You";


    const bubble =
        document.createElement(
            "div"
        );


    bubble.className =
        "message-bubble";


    bubble.textContent =
        text;


    content.appendChild(
        name
    );


    content.appendChild(
        bubble
    );


    if (sender === "ai") {

        row.appendChild(
            avatar
        );

        row.appendChild(
            content
        );

    }

    else {

        row.appendChild(
            content
        );

        row.appendChild(
            avatar
        );

    }


    container.appendChild(
        row
    );


    scrollToBottom();

}


// ============================================================
// MODEL NAME
// ============================================================

function getModelName() {

    if (selectedModel === "llama") {

        return "LLaMA 3.2";

    }


    if (selectedModel === "deepseek") {

        return "DeepSeek V3";

    }


    return "PDF Assistant";

}


// ============================================================
// TYPING INDICATOR
// ============================================================

function showTyping() {

    const container =
        document.getElementById(
            "chatMessages"
        );


    const id =
        "typing-" + Date.now();


    const row =
        document.createElement(
            "div"
        );


    row.className =
        "message-row ai";


    row.id = id;


    row.innerHTML = `

        <div class="avatar ai-avatar">
            ✦
        </div>

        <div class="message-content">

            <div class="message-name">
                ${getModelName()}
            </div>

            <div class="message-bubble">

                <div class="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        </div>

    `;


    container.appendChild(
        row
    );


    scrollToBottom();


    return id;

}


// ============================================================
// REMOVE TYPING
// ============================================================

function removeTyping(id) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.remove();

    }

}


// ============================================================
// PDF UPLOAD
// ============================================================

async function uploadPDF() {

    const fileInput =
        document.getElementById(
            "pdfFile"
        );


    const file =
        fileInput.files[0];


    if (!file) {

        return;

    }


    // Make sure it is PDF

    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        document.getElementById(
            "fileStatus"
        ).textContent =
            "⚠️ Please select a PDF file.";

        return;

    }


    const status =
        document.getElementById(
            "fileStatus"
        );


    status.textContent =
        "Uploading PDF...";


    status.style.color =
        "#6366f1";


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {


        // ==================================================
        // SEND PDF TO FLASK
        // ==================================================

        const response =
            await fetch(
                "/upload",
                {

                    method: "POST",

                    body: formData

                }
            );


        const data =
            await response.json();


        // ==================================================
        // SUCCESS
        // ==================================================

        if (data.success) {

            uploadedPDF =
                data.path;


            status.textContent =
                "✓ " + data.filename;


            status.style.color =
                "#22a06b";


            // Automatically switch to PDF assistant

            selectModel("pdf");

        }


        // ==================================================
        // ERROR
        // ==================================================

        else {

            uploadedPDF = null;


            status.textContent =
                "⚠️ " + data.error;


            status.style.color =
                "#e45b63";

        }


    }


    catch (error) {

        uploadedPDF = null;


        status.textContent =
            "⚠️ Upload failed.";


        status.style.color =
            "#e45b63";


        console.error(
            "Upload error:",
            error
        );

    }

}


// ============================================================
// SUGGESTION BUTTON
// ============================================================

function useSuggestion(text) {

    const input =
        document.getElementById(
            "messageInput"
        );


    input.value =
        text;


    autoResize(
        input
    );


    input.focus();

}


// ============================================================
// NEW CHAT
// ============================================================

function newChat() {

    const container =
        document.getElementById(
            "chatMessages"
        );


    container.innerHTML = `

        <div
            class="welcome-message"
            id="welcomeMessage">

            <div class="welcome-icon">
                ✨
            </div>

            <h2>
                How can I help you today?
            </h2>

            <p>
                Ask a question, explore an idea,
                or upload a PDF to get started.
            </p>

            <div class="suggestion-grid">

                <button
                    onclick="useSuggestion(
                        'Explain what RAG is in simple words'
                    )">

                    <span>💡</span>

                    <div>

                        <strong>
                            Learn something
                        </strong>

                        <small>
                            Explain RAG in simple words
                        </small>

                    </div>

                </button>


                <button
                    onclick="useSuggestion(
                        'What are the main features of an AI chatbot?'
                    )">

                    <span>🤖</span>

                    <div>

                        <strong>
                            AI concepts
                        </strong>

                        <small>
                            Explore AI chatbot features
                        </small>

                    </div>

                </button>


                <button
                    onclick="useSuggestion(
                        'Give me 5 ideas for a college project'
                    )">

                    <span>🚀</span>

                    <div>

                        <strong>
                            Get ideas
                        </strong>

                        <small>
                            Find project ideas
                        </small>

                    </div>

                </button>


                <button
                    onclick="selectModel('pdf')">

                    <span>📄</span>

                    <div>

                        <strong>
                            Ask my PDF
                        </strong>

                        <small>
                            Upload and analyze a document
                        </small>

                    </div>

                </button>

            </div>

        </div>

    `;


    // Clear current input

    document.getElementById(
        "messageInput"
    ).value = "";


    // Reset uploaded PDF

    uploadedPDF = null;


    document.getElementById(
        "fileStatus"
    ).textContent = "";


    // Return to LLaMA

    selectModel("llama");

}


// ============================================================
// CLEAR CHAT
// ============================================================

function clearChat() {

    newChat();

}


// ============================================================
// HIDE WELCOME
// ============================================================

function hideWelcome() {

    const welcome =
        document.getElementById(
            "welcomeMessage"
        );


    if (welcome) {

        welcome.remove();

    }

}


// ============================================================
// AUTO RESIZE
// ============================================================

function autoResize(textarea) {

    textarea.style.height =
        "auto";


    textarea.style.height =
        Math.min(
            textarea.scrollHeight,
            120
        ) + "px";

}


// ============================================================
// ENTER KEY
// ============================================================

function handleKeyDown(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


// ============================================================
// SCROLL
// ============================================================

function scrollToBottom() {

    const container =
        document.getElementById(
            "chatMessages"
        );


    setTimeout(
        function() {

            container.scrollTop =
                container.scrollHeight;

        },
        50
    );

}


// ============================================================
// MOBILE SIDEBAR
// ============================================================

function toggleSidebar() {

    const sidebar =
        document.querySelector(
            ".sidebar"
        );


    sidebar.classList.toggle(
        "open"
    );

}