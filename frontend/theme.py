import shinyswatch

UAI_THEME = shinyswatch.theme.flatly \
  .add_defaults(
    primary="#FB8FE6",
    secondary="#585657",
    success="#4D736F",
    info="#9DA6C9",
    warning="#ffc900",
    danger="#090909",
    light="#FFFFFF",
    dark="#090909",
    font_family='"Bricolage Grotesque", sans-serif',
    font_size="16px",
    body_bg="#F2F2EF",
    body_color="#585657"
  ) \
  .add_rules("""
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&display=swap');
    :root {
      --bg-canvas: #F2F2EF;
      --bg-card:   #FFFFFF;
      --ink-900:   #090909;
      --ink-700:   #585657;
      --line-200:  #E4E3E2;
      --acc-pink:  #FB8FE6;
      --acc-teal:  #4D736F;
      --acc-coral: #ffc900;
      --acc-lilac: #9DA6C9;
      --radius-xl: 24px;
      --radius-md: 14px;
      --shadow-soft: 0 6px 18px rgba(0,0,0,0.06);
      --shadow-sticker: 0 6px 0 rgba(0,0,0,1);
      --border-strong: 2px solid var(--ink-900);
      --border-light: 1px solid var(--line-200);
    }

    html, body {
      font-family: "Bricolage Grotesque", sans-serif !important;
      font-optical-sizing: auto !important;
      font-weight: 400 !important;
      font-style: normal !important;
      font-variation-settings: "wdth" 100 !important;
      font-size: 14px !important;
      line-height: 1.5;
      background: var(--bg-canvas) !important;
      color: var(--ink-700) !important;
    }

    * {
      font-family: "Bricolage Grotesque", sans-serif !important;
      font-optical-sizing: auto !important;
      font-variation-settings: "wdth" 100 !important;
    }

    body > div {
      padding: clamp(24px, 4vw, 48px) !important;
      background: var(--bg-canvas) !important;
    }

    .container-fluid {
      background: var(--bg-card) !important;
      border-radius: var(--radius-xl) !important;
      border: var(--border-light) !important;
      box-shadow: var(--shadow-soft) !important;
      padding: clamp(20px, 3vw, 32px) !important;
      max-width: 1200px !important;
      margin: 0 auto !important;
    }

    h1 {
      font-family: "Bricolage Grotesque", sans-serif !important;
      font-optical-sizing: auto !important;
      font-weight: 800 !important;
      font-style: normal !important;
      font-variation-settings: "wdth" 100 !important;
      letter-spacing: -0.02em !important;
      font-size: clamp(28px, 4vw, 44px) !important;
      line-height: 1.1 !important;
      color: var(--ink-900) !important;
      margin-bottom: 16px !important;
    }

    h2, h3 {
      font-family: "Bricolage Grotesque", sans-serif !important;
      font-optical-sizing: auto !important;
      font-weight: 700 !important;
      font-style: normal !important;
      font-variation-settings: "wdth" 100 !important;
      color: var(--ink-900) !important;
      margin-bottom: 16px !important;
    }

    p, .text-muted {
      font-size: clamp(14px, 1.4vw, 18px) !important;
      line-height: 1.5 !important;
      color: var(--ink-700);
      margin-bottom: 16px !important;
    }

    .shiny-chat-container {
      background: var(--bg-card) !important;
      border-radius: var(--radius-xl) !important;
      border: var(--border-light) !important;
      box-shadow: var(--shadow-soft) !important;
      margin-top: 24px !important;
      overflow: hidden !important;
    }

    .shiny-chat-messages {
      padding: clamp(16px, 2vw, 24px) !important;
      max-height: 500px !important;
      overflow-y: auto !important;
      background: var(--bg-card) !important;
    }

    .shiny-chat-input-container {
      border-top: var(--border-light) !important;
      padding: 16px clamp(16px, 2vw, 24px) !important;
      background: var(--bg-canvas) !important;
    }

    .shiny-chat-input {
      background: var(--bg-card) !important;
      border: var(--border-strong) !important;
      border-radius: 10px !important;
      padding: 12px 14px !important;
      font-size: 14px !important;
      color: var(--ink-900) !important;
      font-weight: 500 !important;
      transition: all 0.2s ease !important;
      min-height: 60px !important;
      resize: vertical !important;
      font-family: "Bricolage Grotesque", sans-serif !important;
    }

    .shiny-chat-input:focus {
      outline: none !important;
      box-shadow: 0 0 0 3px rgba(251, 143, 230, 0.2) !important;
      transform: translateY(-1px) !important;
    }

    shiny-chat-message {
      background: white !important;
      margin-bottom: 16px !important;
      padding: 16px 20px !important;
      border-radius: var(--radius-md) !important;
      line-height: 1.6 !important;
      font-size: 14px !important;
      border: var(--border-strong) !important;
      box-shadow: var(--shadow-sticker) !important;
    }

    shiny-chat-message[data-role="user"] {
      background: var(--acc-pink) !important;
      color: var(--ink-900) !important;
      margin-left: 20% !important;
      font-weight: 600 !important;
    }

    shiny-chat-message[data-role="user"] p {
      color: var(--ink-900) !important;
    }

    shiny-chat-message[data-role="assistant"] {
      background: var(--bg-card) !important;
      color: var(--ink-700) !important;
      margin-right: 20% !important;
    }

    shiny-chat-message .message-icon {
      background: var(--acc-pink) !important;
      border: var(--border-strong) !important;
      box-shadow: none !important;
      border-radius: 50% !important;
    }
      
    shiny-chat-message[data-role="user"] .message-icon {
      display: none !important;
    }
    
    .fa {
      fill: black #important;
    }

    .suggestion {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: var(--acc-coral) !important;
      color: var(--ink-900) !important;
      padding: 12px 18px !important;
      border-radius: 10px !important;
      margin: 4px 8px 4px 0 !important;
      font-size: 14px !important;
      font-weight: 700 !important;
      border: var(--border-strong) !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      text-decoration: none !important;
      box-shadow: 0 4px 0 rgba(0,0,0,1) !important;
    }

    .suggestion:hover {
      background: var(--acc-teal) !important;
      color: white !important;
      transform: translateY(-2px) !important;
      box-shadow: 0 8px 0 rgba(0,0,0,1) !important;
    }

    .suggestion:active {
      transform: translateY(1px) !important;
      box-shadow: 0 2px 0 rgba(0,0,0,1) !important;
    }

    .btn {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 12px 18px !important;
      gap: 10px !important;
      background: var(--acc-coral) !important;
      border: var(--border-strong) !important;
      border-radius: 10px !important;
      font-weight: 700 !important;
      color: var(--ink-900) !important;
      font-size: 14px !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      text-decoration: none !important;
      box-shadow: 0 4px 0 rgba(0,0,0,1) !important;
    }

    .btn:hover {
      background: var(--acc-teal) !important;
      color: white !important;
      transform: translateY(-1px) !important;
      box-shadow: 0 6px 0 rgba(0,0,0,1) !important;
    }

    .btn:active {
      transform: translateY(1px) !important;
      box-shadow: 0 1px 0 rgba(0,0,0,1) !important;
    }

    .btn-primary {
      background: var(--acc-pink) !important;
      color: var(--ink-900) !important;
      border: var(--border-strong) !important;
    }

    .btn-primary:hover {
      background: var(--acc-teal) !important;
      color: white !important;
    }

    .form-control {
      background: var(--bg-card) !important;
      border: var(--border-strong) !important;
      border-radius: 10px !important;
      padding: 12px 14px !important;
      font-size: 14px !important;
      color: var(--ink-900) !important;
      font-weight: 500 !important;
      transition: all 0.2s ease !important;
      height: auto !important;
      min-height: 84px !important;
      max-height: 200px !important;
      overflow-y: auto !important;
      resize: none !important;
    }

    .form-control:focus {
      outline: none !important;
      box-shadow: 0 0 0 3px rgba(251, 143, 230, 0.2) !important;
      transform: translateY(-1px) !important;
    }

    @media (max-width: 768px) {
      body > div {
        padding: 16px !important;
      }

      .container-fluid {
        padding: 16px !important;
        border-radius: 16px !important;
      }

      h1 {
        font-size: 24px !important;
      }

      shiny-chat-message[data-role="user"] {
        margin-left: 10% !important;
      }

      shiny-chat-message[data-role="assistant"] {
        margin-right: 10% !important;
      }
    }
  """)