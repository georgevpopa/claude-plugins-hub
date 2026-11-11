# ⚡ Claude Code Plugins Hub & Semantic Matcher

Hub portabil, cross-platform (**Linux & Windows**), conținând suita oficială de **18 plugin-uri esențiale**, puntea integrată de **Skills** și motorul de căutare semantică `index_plugin` pentru **Claude Code** (inclusiv instanța noastră Free Claude Code conectată la Evo-X3).

---

## 📦 Instalare Rapidă (1-Click) pe Orice Dispozitiv

### Pe Linux / macOS:
```bash
git clone https://github.com/georgevpopa/claude-plugins-hub.git
cd claude-plugins-hub
./setup.sh
# sau direct:
python3 install.py
```

### Pe Windows:
- Deschide **PowerShell** sau **CMD**:
  ```powershell
  git clone https://github.com/georgevpopa/claude-plugins-hub.git
  cd claude-plugins-hub
  ```
- Rulare în **PowerShell**:
  ```powershell
  python install.py
  # sau
  .\setup.ps1
  ```
- Rulare în **Command Prompt (CMD)**:
  ```cmd
  setup.bat
  # sau
  python install.py
  ```

> [!NOTE]
> Scriptul Python `install.py` detectează automat sistemul de operare, instalează toate plugin-urile prin CLI-ul `claude plugin install`, creează puntea de skills în `~/.claude/skills` (sau `%USERPROFILE%\.claude\skills` pe Windows) și adaugă utilitarul `index_plugin` în PATH.

---

## 🔍 Cum se folosește `index_plugin` pentru Claude Code

Utilitarul suportă căutare semantică dedicată pentru ecosistemul Claude Code prin flag-ul `--claude`:

### 1. Catalogul Plugin-urilor Claude Code:
```bash
index_plugin --claude -l
```

### 2. Căutare Semantică cu Prag de Relevanță (implicit $\ge 70\%$):
```bash
# Code review automat & analiză PR:
index_plugin --claude "review cod si verificare"

# Scanare securitate & vulnerabilități:
index_plugin --claude "vulnerabilitati si securitate"

# Simplificare și curățare cod:
index_plugin --claude "simplifica cod si clean code"

# Creare și benchmark de skills:
index_plugin --claude "creare skills noi"

# Automatizări și hook-uri:
index_plugin --claude "hook-uri si preventie erori"
```

### 3. Detalii Complete despre un Plugin:
```bash
index_plugin --info code-review
index_plugin --info claude-security
index_plugin --info skill-creator
```

---

## 🛠️ Suita de Plugin-uri Incluse (18 Plugin-uri Oficiale)

| Categorie | Plugin-uri Incluse | Rol & Utilitate |
| :--- | :--- | :--- |
| **Dezvoltare & Arhitectură** | `feature-dev`, `code-simplifier`, `code-modernization`, `playground`, `skill-creator` | Dezvoltare module, clean code, modernizare legacy, sandbox HTML și crearea de skills. |
| **Review & Git Automation** | `code-review`, `pr-review-toolkit`, `commit-commands`, `hookify`, `claude-md-management` | Multi-agent PR review, diff-uri, generare automată de commit-uri și hook-uri de siguranță. |
| **Securitate & Ghidaj** | `claude-security`, `security-guidance` | Audit de vulnerabilități (SAST), verificare tipare riscante și ghidaj securitate cod. |
| **Language Servers (LSP)** | `typescript-lsp`, `pyright-lsp`, `rust-analyzer-lsp`, `gopls-lsp` | Navigare tipuri, erori de sintaxă și semantică pentru TypeScript, Python, Rust și Go. |
| **Design & UI** | `frontend-design` | Implementare și arhitectură UI/UX, styling și componente frontend. |
| **Backend & Protocoale** | `mcp-server-dev` | Proiectare și testare servere Model Context Protocol (MCP). |

---

## 🧠 Puntea de Skills & Crearea de Proceduri Noi (`skill-creator`)

1. **Puntea Automată**: Toate procedurile din `~/.gemini/config/skills` (cum ar fi `context-guard`, `evo-muscle`, `reverse-engineer-anything`) sunt automat legate în `~/.claude/skills/`, fiind disponibile nativ în sesiunile Claude Code.
2. **Dezvoltare de Skills Noi**:
   - `skill-creator` permite rularea evaluărilor automate:
     ```bash
     python3 ~/.claude/plugins/cache/anthropic-plugin-directory/skill-creator/*/skills/skill-creator/scripts/quick_validate.py ~/.claude/skills/<nume-skill>
     ```

---

## 🌐 Sincronizare pe Orice Calculator

Repository GitHub oficial:
👉 **`https://github.com/georgevpopa/claude-plugins-hub`**

Pe orice mașină nouă:
```bash
git clone https://github.com/georgevpopa/claude-plugins-hub.git
cd claude-plugins-hub
python install.py
```
Toate plugin-urile, utilitarele și puntea de skills se instalează și se configurează automat!
