#!/usr/bin/env python3
"""
Claude Code Plugins Hub - Universal Installer (Cross-Platform: Linux, macOS, Windows)
Instalează toate plugin-urile oficiale din manifest în Claude Code și configurează puntea de skills.
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}\n  {text}\n{'='*60}")

def main():
    print_header("Claude Code Plugins Hub - Universal Installer")

    home = Path.home()
    is_windows = os.name == 'nt' or sys.platform.startswith('win')
    
    # 1. Verificare CLI claude
    claude_cmd = shutil.which("claude") or shutil.which("claude.cmd")
    if not claude_cmd:
        print("❌ Comanda 'claude' nu a fost găsită în PATH!")
        print("   Instalează Claude Code cu:")
        print("   npm install -g @anthropic-ai/claude-code")
        sys.exit(1)
    
    print(f"✔ Claude CLI detectat: {claude_cmd}")
    print(f"✔ Sistem de operare: {'Windows' if is_windows else 'Linux / macOS'}")

    # 2. Citire manifest
    manifest_path = Path(__file__).parent / "plugins_manifest.json"
    if not manifest_path.exists():
        print(f"❌ Nu s-a găsit manifestul la {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    plugins = manifest.get("plugins", {})
    total = len(plugins)
    print(f"📦 Manifest încărcat: {total} plugin-uri de instalat.\n")

    # 3. Instalare plugin-uri
    installed_count = 0
    failed = []

    for name, pinfo in plugins.items():
        plugin_id = pinfo.get("id", name)
        print(f"⏳ Instalare [{installed_count + 1}/{total}]: {name} ({plugin_id})...")
        
        # Rulare comanda claude plugin install <plugin_id>
        cmd = [claude_cmd, "plugin", "install", plugin_id]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 or "already installed" in res.stderr.lower() or "installed" in res.stdout.lower():
                print(f"   ✔ Instalat cu succes: {name}")
                installed_count += 1
            else:
                # Fallback încercare doar cu numele simplu dacă cu @ eșuează
                fallback_cmd = [claude_cmd, "plugin", "install", name]
                res2 = subprocess.run(fallback_cmd, capture_output=True, text=True)
                if res2.returncode == 0:
                    print(f"   ✔ Instalat cu succes (nume simplu): {name}")
                    installed_count += 1
                else:
                    print(f"   ⚠️ Avertisment la {name}: {res.stderr.strip()[:100]}")
                    failed.append(name)
        except Exception as e:
            print(f"   ❌ Eroare execuție: {e}")
            failed.append(name)

    # 4. Configurare punte Skills (~/.claude/skills)
    skills_dir = home / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📂 Director skills Claude Code configurat: {skills_dir}")

    # Punte opțională către skills existente în Antigravity dacă sunt prezente
    gemini_skills = home / ".gemini" / "config" / "skills"
    if gemini_skills.exists():
        for sdir in gemini_skills.iterdir():
            if sdir.is_dir() and (sdir / "SKILL.md").exists():
                dest = skills_dir / sdir.name
                if not dest.exists():
                    try:
                        if not is_windows:
                            dest.symlink_to(sdir, target_is_directory=True)
                        else:
                            shutil.copytree(sdir, dest)
                        print(f"   🔗 Punte skill activată: {sdir.name}")
                    except Exception as e:
                        pass

    # 5. Configurare scurtătură CLI index_plugin
    script_bin = Path(__file__).parent / "bin"
    if is_windows:
        user_bin = home / "bin"
        user_bin.mkdir(parents=True, exist_ok=True)
        for fn in ["index_plugin.cmd", "index_plugin.ps1", "index_plugin.py"]:
            src = script_bin / fn
            if src.exists():
                shutil.copy(src, user_bin / fn)
        print(f"✔ Wrapper-e Windows copiate în {user_bin}")
    else:
        user_bin = home / ".local" / "bin"
        user_bin.mkdir(parents=True, exist_ok=True)
        src = script_bin / "index_plugin"
        if src.exists():
            dest = user_bin / "index_plugin"
            shutil.copy(src, dest)
            dest.chmod(0o755)
            print(f"✔ Executabil index_plugin instalat în {dest}")

    print_header(f"Finalizat: {installed_count}/{total} plugin-uri Claude Code gata de utilizare!")
    if failed:
        print(f"Plugin-uri ce au necesitat intervenție: {', '.join(failed)}")

if __name__ == "__main__":
    main()
