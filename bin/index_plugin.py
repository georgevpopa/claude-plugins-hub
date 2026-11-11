#!/usr/bin/env python3
"""
Antigravity & Claude Code Plugin Index & Semantic Matcher (Universal Cross-Platform)
Indexează toate plugin-urile instalate (Antigravity & Claude Code), oferă căutare semantică
cu prag de relevanță (>= 70%) și afișează componentele (skills, reguli, servere MCP).
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path

HOME = Path.home()
ANTIGRAVITY_PLUGINS_DIR = HOME / ".gemini" / "config" / "plugins"
CLAUDE_DIR = HOME / ".claude"
CLAUDE_INSTALLED_FILE = CLAUDE_DIR / "plugins" / "installed_plugins.json"

STOPWORDS = {
    "si", "de", "cu", "la", "in", "pentru", "un", "o", "am", "nevoie", "ce", "care", 
    "ar", "fi", "mai", "bun", "folosit", "the", "a", "an", "and", "or", "for", "to", 
    "is", "are", "sa", "pe", "din", "plugin", "pluginuri", "pluginurile", "noastre", 
    "cel", "vreau", "caut", "as", "vrea", "cum", "sa-mi", "imi", "iti", "cumva", "fac",
    "faci", "avem", "putem", "folosi", "foloseste", "folosesc", "help", "ajuta", "trebuie",
    "claude", "antigravity"
}

DOMAIN_EXPERTS = {
    # Antigravity & General
    "context7": ["prisma", "react", "nextjs", "vue", "tailwind", "fastapi", "django", "library", "librarie", "pachet", "documentatie", "docs", "lookup", "manual", "sdk"],
    "android-cli-plugin": ["apk", "smali", "dex", "android", "adb", "aapt2", "emulator", "decompile", "decompilare", "mobile", "app", "aplicatie"],
    "virustotal": ["virus", "malware", "securitate", "security", "threat", "hash", "sha256", "suspicios", "fisier", "url", "ip", "analiza"],
    "superpowers": ["tdd", "debugging", "plan", "workflow", "inginerie", "best-practices", "arhitectura", "refactoring", "superpowers", "calitate", "teste"],
    "skill-creator": ["skill", "skills", "creare", "creator", "creeaza", "evals", "benchmark", "nou", "noi", "dezvoltare"],
    "postman": ["postman", "api", "rest", "endpoints", "mock", "http", "swagger", "openapi", "colectii", "testare"],
    "browse": ["browser", "click", "screenshot", "scrape", "scraping", "navigare", "web", "browserbase"],
    "parallel": ["cautare", "search", "web", "live", "internet", "google", "stiri", "articole", "actual"],
    "chrome-devtools-plugin": ["chrome", "devtools", "puppeteer", "consola", "network", "dom", "inspectare", "performanta"],
    "supabase": ["supabase", "postgres", "sql", "baza de date", "database", "auth", "storage", "backend"],
    "mongodb-atlas": ["mongodb", "mongo", "nosql", "document", "colectii", "atlas", "database", "baza"],
    "neo4j": ["neo4j", "graf", "graph", "cypher", "graphrag", "relatii", "noduri"],
    "coderabbit": ["code review", "review", "pr", "pull request", "refactor", "calitate cod", "verificare cod"],
    "qodo": ["qodo", "git", "istoric", "modificari", "local", "review"],
    "firebase": ["firebase", "firestore", "auth", "realtime", "cloud functions", "google backend"],
    "flutter": ["flutter", "dart", "mobile", "cross-platform", "widget", "multiplatform"],
    "unity": ["unity", "joc", "jocuri", "game", "gamedev", "c#", "3d", "2d"],
    "vercel-plugin": ["vercel", "nextjs", "deploy", "serverless", "edge", "frontend"],
    "netlify": ["netlify", "deploy", "edge functions", "blobs", "frontend"],
    "railway": ["railway", "hosting", "deploy", "containere", "infrastructura"],
    "auth0": ["auth0", "autentificare", "login", "sso", "mfa", "rbac", "user"],
    "sentry": ["sentry", "erori", "exceptions", "crash", "monitoring", "stacktrace"],
    "datadog": ["datadog", "apm", "metrici", "loguri", "observabilitate", "dashboard"],
    "stripe": ["stripe", "plati", "card", "bani", "abonament", "facturi", "checkout"],
    "figma": ["figma", "design", "ui", "ux", "componente", "css", "styling"],
    "notion": ["notion", "note", "workspace", "documentare", "wiki", "pagini"],
    "trello": ["trello", "kanban", "board", "liste", "carduri", "task-uri"],
    "linear": ["linear", "issue tracker", "sprint", "bug", "taskuri", "proiect"],
    
    # Claude Code Specific
    "feature-dev": ["feature", "functie", "functionalitate", "dezvoltare", "modul", "implementare", "arhitectura feature"],
    "code-review": ["code review", "review", "audit", "verificare cod", "analiza cod", "defecte", "pr review"],
    "code-simplifier": ["simplifica", "refactor", "curatare", "clean code", "lizibilitate", "optimizare"],
    "pr-review-toolkit": ["pr", "pull request", "git", "diff", "comentarii pr", "teste pr"],
    "commit-commands": ["commit", "git commit", "push", "mesaj commit", "git push"],
    "claude-security": ["securitate", "vulnerabilitati", "cve", "sast", "audit securitate", "deep scan"],
    "security-guidance": ["ghid securitate", "securitate cod", "safe coding", "best practices security"],
    "frontend-design": ["frontend", "ui", "ux", "interfata", "styling", "design sistem"],
    "hookify": ["hook", "hook-uri", "automatizare", "reguli", "event", "preventie erori"],
    "mcp-server-dev": ["mcp server", "creare mcp", "server mcp", "protocol mcp", "tool mcp"],
    "playground": ["playground", "html", "prototip", "demo", "interactiv", "canvas"],
    "claude-md-management": ["claude.md", "management claude", "instructiuni", "audit claude"],
    "code-modernization": ["legacy", "modernizare", "upgrade cod", "refactorizare masiva", "migrare"],
    "typescript-lsp": ["typescript", "ts", "types", "lsp typescript", "javascript", "js"],
    "pyright-lsp": ["python", "pyright", "type checking python", "lsp python"],
    "rust-analyzer-lsp": ["rust", "cargo", "lsp rust", "rust-analyzer"],
    "gopls-lsp": ["go", "golang", "lsp go", "gopls"]
}

CATEGORIES = {
    "Dezvoltare & Superpowers": ["superpowers", "skill-creator", "context7", "coderabbit", "qodo", "postman", "google-antigravity-sdk", "modern-web-guidance-plugin", "spacefast", "google-developer-knowledge", "feature-dev", "code-simplifier", "code-modernization", "playground"],
    "Securitate & Reverse Engineering": ["virustotal", "crowdstrike", "sentinelone-purple-mcp", "endor-labs-agent-kit", "soc", "claude-security", "security-guidance"],
    "Review Cod & Git Automation": ["code-review", "pr-review-toolkit", "commit-commands", "hookify", "claude-md-management"],
    "Language Servers (LSP)": ["typescript-lsp", "pyright-lsp", "rust-analyzer-lsp", "gopls-lsp"],
    "Browser & Scraping Web": ["browse", "parallel", "chrome-devtools-plugin", "keenable", "keenable-select"],
    "Mobile & Game Dev": ["android-cli-plugin", "flutter", "unity"],
    "Baze de Date, Backend & Cloud": ["supabase", "mongodb-atlas", "neo4j", "firebase", "vercel-plugin", "netlify", "railway", "databricks", "data-agent-kit-plugin", "google-cloud-developer", "gemini-api", "looker", "base44", "mcp-server-dev"],
    "Observabilitate & Erori": ["sentry", "datadog", "dynatrace", "arize-skills", "leapwork-play"],
    "Productivitate, Workspace & Task-uri": ["atlassian-twg-cli", "notion", "trello", "linear", "monday", "zapier", "dropbox", "wispr-flow", "pandadoc", "figma", "mobbin", "canva", "invideo", "frontend-design"],
    "Google Workspace": ["gdrive", "gdocs", "gsheets", "gmail", "gcalendar", "gslides", "google_maps_platform"],
    "Business, CRM & Altele": ["stripe", "auth0", "semrush", "wordpress", "wix", "intercom", "harness-antigravity", "ping-identity-pingone", "zoho-crm-plugin", "zoho-projects", "zoho-desk-antigravity", "zohobooks-antigravity", "zoho-bigin", "science", "egm"]
}

def clean_query(text):
    tokens = re.findall(r'[a-zA-Z0-9_\-]+', text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def scan_antigravity_plugins():
    plugins = {}
    if not ANTIGRAVITY_PLUGINS_DIR.exists():
        return plugins

    for p in sorted(ANTIGRAVITY_PLUGINS_DIR.iterdir()):
        if not p.is_dir():
            continue
        
        manifest = p / "plugin.json"
        if not manifest.exists():
            for alt in [p / ".claude-plugin" / "plugin.json", p / ".antigravity-plugin" / "plugin.json"]:
                if alt.exists():
                    manifest = alt
                    break

        meta = {}
        if manifest.exists():
            try:
                with open(manifest, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass

        name = meta.get("name") or p.name
        display_name = meta.get("displayName") or name
        version = meta.get("version", "1.0.0")
        desc = meta.get("description", "Fără descriere disponibilă.")
        keywords = meta.get("keywords", [])
        
        skills = []
        skills_dir = p / "skills"
        if skills_dir.exists():
            for s in skills_dir.glob("*/SKILL.md"):
                skills.append(s.parent.name)

        has_mcp = (p / "mcp_config.json").exists() or (p / ".mcp.json").exists()
        has_hooks = (p / "hooks.json").exists() or (p / "hooks" / "hooks.json").exists()
        has_rules = (p / "rules").exists()

        category = "Altele"
        for cat, names in CATEGORIES.items():
            if name in names:
                category = cat
                break

        plugins[name] = {
            "name": name,
            "display_name": display_name,
            "version": version,
            "dir": p.name,
            "path": str(p),
            "description": desc,
            "category": category,
            "keywords": keywords,
            "skills": skills,
            "skills_count": len(skills),
            "has_mcp": has_mcp,
            "has_hooks": has_hooks,
            "has_rules": has_rules,
            "ecosystem": "Antigravity"
        }

    return plugins

def scan_claude_plugins():
    plugins = {}
    if not CLAUDE_INSTALLED_FILE.exists():
        return plugins

    try:
        with open(CLAUDE_INSTALLED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return plugins

    for plugin_key, items in data.get("plugins", {}).items():
        name = plugin_key.split("@")[0]
        meta_info = items[0] if items else {}
        install_path = meta_info.get("installPath")
        version = meta_info.get("version", "1.0.0")
        desc = "Plugin oficial Claude Code."
        skills = []

        if install_path:
            ipath = Path(install_path)
            for pjson in [ipath / "plugin.json", ipath / ".claude-plugin" / "plugin.json"]:
                if pjson.exists():
                    try:
                        with open(pjson, "r", encoding="utf-8") as pf:
                            pj = json.load(pf)
                            desc = pj.get("description", desc)
                    except Exception:
                        pass
            
            sdir = ipath / "skills"
            if sdir.exists():
                for s in sdir.glob("*/SKILL.md"):
                    skills.append(s.parent.name)

        category = "Altele"
        for cat, names in CATEGORIES.items():
            if name in names:
                category = cat
                break

        plugins[name] = {
            "name": name,
            "display_name": name,
            "version": version,
            "dir": name,
            "path": install_path or "",
            "description": desc,
            "category": category,
            "keywords": [name],
            "skills": skills,
            "skills_count": len(skills),
            "has_mcp": False,
            "has_hooks": False,
            "has_rules": False,
            "ecosystem": "Claude Code"
        }

    return plugins

def score_plugin(plugin, query_tokens, full_query):
    score = 0.0
    matched_reasons = []

    name = plugin["name"].lower()
    desc = plugin["description"].lower()
    keywords = [k.lower() for k in plugin.get("keywords", [])]
    skills = [s.lower() for s in plugin.get("skills", [])]
    all_text = name + " " + desc + " " + " ".join(keywords) + " " + " ".join(skills)

    # 1. Verificare Expertiză de Domeniu (Domain Knowledge Map)
    domain_terms = DOMAIN_EXPERTS.get(plugin["name"], [])
    domain_hits = []
    for dt in domain_terms:
        if dt in full_query or any(dt in qt for qt in query_tokens):
            domain_hits.append(dt)

    if domain_hits:
        score += 75.0
        matched_reasons.append(f"domeniu cheie: {', '.join(domain_hits)}")

    # 2. Match exact pe numele plugin-ului sau skill-urilor
    for q in query_tokens:
        if q == name or q in name:
            score += 35.0
            matched_reasons.append(f"nume plugin ('{name}')")
            break

    # 3. Match pe skills conținute
    matched_skills = [s for s in skills if any(q in s for q in query_tokens)]
    if matched_skills:
        score += 25.0
        matched_reasons.append(f"skills: {', '.join(matched_skills[:3])}")

    # 4. Potrivire în descriere & cuvinte cheie
    token_hits = [q for q in query_tokens if q in all_text]
    if token_hits:
        score += min(len(token_hits) * 12.0, 30.0)
        matched_reasons.append(f"termeni găsiți: {', '.join(token_hits)}")

    final_score = min(score, 100.0)
    return final_score, matched_reasons

def main():
    parser = argparse.ArgumentParser(
        description="Antigravity & Claude Code Plugin Index & Semantic Matcher",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("query", nargs="*", help="Căutare după intenție/nevoie (ex: 'analiza apk', 'documentatie prisma', 'tdd')")
    parser.add_argument("-l", "--list", action="store_true", help="Listează toate plugin-urile instalate grupate pe categorii")
    parser.add_argument("-i", "--info", metavar="PLUGIN", help="Afișează detaliile complete ale unui plugin specific")
    parser.add_argument("-j", "--json", action="store_true", help="Returnează rezultatele în format JSON brut")
    parser.add_argument("-t", "--threshold", type=float, default=70.0, help="Pragul minim de potrivire procentuală (implicit: 70%%)")
    parser.add_argument("--claude", action="store_true", help="Filtrează exclusiv plugin-urile din Claude Code")
    parser.add_argument("--antigravity", action="store_true", help="Filtrează exclusiv plugin-urile din Antigravity")

    args = parser.parse_args()

    antigravity_plugins = scan_antigravity_plugins() if not args.claude else {}
    claude_plugins = scan_claude_plugins() if not args.antigravity else {}
    
    all_plugins = {}
    for k, v in antigravity_plugins.items():
        all_plugins[k] = v
    for k, v in claude_plugins.items():
        if k in all_plugins:
            all_plugins[k]["ecosystem"] = "Ambele (Antigravity & Claude Code)"
        else:
            all_plugins[k] = v

    if args.json and not args.query and not args.info:
        print(json.dumps(all_plugins, indent=2, ensure_ascii=False))
        return

    if args.info:
        target = args.info.strip()
        found = all_plugins.get(target)
        if not found:
            matches = [k for k in all_plugins if target.lower() in k.lower()]
            if matches:
                found = all_plugins[matches[0]]

        if not found:
            print(f"❌ Plugin-ul '{target}' nu a fost găsit.")
            sys.exit(1)

        print(f"\n{'='*70}")
        print(f"📦 Plugin: {found['name']}  (v{found['version']})")
        print(f"🏷️  Ecosistem: {found['ecosystem']}")
        print(f"📁 Director: {found['path']}")
        print(f"📂 Categorie: {found['category']}")
        print(f"{'='*70}")
        print(f"📝 Descriere:\n   {found['description']}\n")
        
        if found.get("skills"):
            print(f"⚡ Skills incluse ({found['skills_count']}):")
            for s in found["skills"]:
                print(f"   • {s}")
        else:
            print("⚡ Skills: Niciunul definit explicit.")
            
        print(f"🔌 Server MCP: {'DA' if found['has_mcp'] else 'NU'}")
        print(f"🪝 Hook-uri active: {'DA' if found['has_hooks'] else 'NU'}")
        print(f"📜 Reguli incluse: {'DA' if found['has_rules'] else 'NU'}\n")
        return

    if args.query:
        query_str = " ".join(args.query).strip()
        tokens = clean_query(query_str)
        if not tokens:
            tokens = [query_str.lower()]

        results = []
        for p in all_plugins.values():
            score, reasons = score_plugin(p, tokens, query_str.lower())
            if score >= args.threshold:
                results.append((score, p, reasons))

        results.sort(key=lambda x: x[0], reverse=True)

        if args.json:
            json_out = [
                {
                    "score": round(s, 1),
                    "name": p["name"],
                    "ecosystem": p["ecosystem"],
                    "category": p["category"],
                    "description": p["description"],
                    "skills_count": p["skills_count"],
                    "reasons": r
                }
                for s, p, r in results
            ]
            print(json.dumps(json_out, indent=2, ensure_ascii=False))
            return

        print(f"\n🔍 Căutare semantică: \"{query_str}\" (Prag relevanță: >={args.threshold:.0f}%)")
        print(f"{'='*70}")

        if not results:
            print("❌ Niciun plugin nu a atins pragul de relevanță de 70%.")
            print("💡 Sugestie: Încearcă termeni mai generali sau rulează `index_plugin` pentru lista completă.")
            return

        print(f"S-au găsit {len(results)} plugin-uri recomandate:\n")
        for score, p, reasons in results:
            badge = "🟢 PERFECT MATCH" if score >= 90 else "🟡 RELEVANT"
            eco_badge = f"[{p['ecosystem']}]"
            print(f"▶ {p['name']} ({score:.0f}% potrivire) {badge} {eco_badge}")
            print(f"   📂 Categorie: {p['category']}")
            print(f"   💬 Descriere: {p['description']}")
            if p.get("skills"):
                sample_skills = ", ".join(p["skills"][:4])
                if len(p["skills"]) > 4:
                    sample_skills += f" (+ încă {len(p['skills'])-4})"
                print(f"   ⚡ Skills: {sample_skills}")
            print(f"   🎯 Relevanță bazată pe: {', '.join(reasons)}")
            print("-" * 70)
        return

    total_antigravity = len(antigravity_plugins)
    total_claude = len(claude_plugins)
    total_combined = len(all_plugins)
    
    print(f"\n{'='*75}")
    print(f"🚀 CATALOG PLUGIN-URI INSTALATE ({total_combined} total: {total_antigravity} Antigravity, {total_claude} Claude Code)")
    print(f"{'='*75}")

    by_category = {}
    for p in all_plugins.values():
        cat = p["category"]
        by_category.setdefault(cat, []).append(p)

    for cat in sorted(by_category.keys()):
        items = by_category[cat]
        print(f"\n📁 {cat.upper()} ({len(items)} plugin-uri):")
        for p in sorted(items, key=lambda x: x["name"]):
            badges = []
            if p["skills_count"] > 0:
                badges.append(f"{p['skills_count']} skills")
            if p["has_mcp"]:
                badges.append("MCP")
            badge_str = f" [{', '.join(badges)}]" if badges else ""
            eco = f"({p['ecosystem']})"
            desc_short = (p['description'][:65] + '...') if len(p['description']) > 65 else p['description']
            print(f"   • {p['name']:<26} {eco:<24} {badge_str:<12} -> {desc_short}")

    print(f"\n{'='*75}")
    print("💡 Utilizare rapidă:")
    print("   • Căutare generală:    index_plugin \"caut documentatie react\"")
    print("   • Căutare Claude Code: index_plugin --claude \"review cod\"")
    print("   • Detalii complete:    index_plugin --info <nume-plugin>")
    print("   • Export JSON:         index_plugin --json\n")

if __name__ == "__main__":
    main()
