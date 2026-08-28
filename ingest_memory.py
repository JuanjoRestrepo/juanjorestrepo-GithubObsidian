"""
Módulo de Ingestión de Memoria para Obsidian.
Procesa exportaciones de Claude (chat_messages) y ChatGPT (mapping).
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def process_export(file_path: str, output_dir: str = "Context/AI_Memory/"):
    path_out = Path(output_dir)
    path_out.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(file_path):
        print(f"Error: No se encuentra el archivo {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list) and len(data) > 0 and "chat_messages" in data[0]:
        print(f"Procesando exportación de Claude ({len(data)} conversaciones)...")
        _parse_claude(data, path_out)
    elif isinstance(data, list) and len(data) > 0 and "mapping" in data[0]:
        print(f"Procesando exportación de ChatGPT ({len(data)} conversaciones)...")
        _parse_chatgpt(data, path_out)
    else:
        print("Formato no reconocido o archivo vacío.")


def _clean_filename(title: str) -> str:
    # Sanitizar caracteres no válidos para nombres de archivos en OS
    invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for char in invalid_chars:
        title = title.replace(char, "_")
    return title.strip() or "Memoria_Sin_Titulo"


def _generate_frontmatter(title: str, date_str: str, summary: str = "") -> str:
    summary_clean = summary.replace("\n", " ") if summary else ""
    return (
        f"---\n"
        f'title: "{title}"\n'
        f"date: {date_str}\n"
        f"tags: [ai_memory, claude_context]\n"
        f'summary: "{summary_clean}"\n'
        f"---\n\n"
    )


def _parse_claude(data: List[Dict[str, Any]], path_out: Path):
    count = 0
    for convo in data:
        title = _clean_filename(convo.get("name") or "Conversacion_Claude")
        date_str = convo.get("created_at", datetime.now().isoformat())
        summary = convo.get("summary", "")

        md_content = _generate_frontmatter(title, date_str, summary)
        messages = convo.get("chat_messages", [])

        if not messages:
            continue

        for msg in messages:
            sender = msg.get("sender", "unknown")
            text = msg.get("text", "")

            role_label = "Human" if sender == "human" else "Assistant"
            md_content += f"### {role_label}\n{text}\n\n"

        file_dest = path_out / f"Claude_{title}_{convo.get('uuid', '')[:8]}.md"
        with open(file_dest, "w", encoding="utf-8") as out:
            out.write(md_content)
        count += 1

    print(f"¡Éxito! Se generaron {count} archivos de memoria en '{path_out}'.")


def _parse_chatgpt(data: List[Dict[str, Any]], path_out: Path):
    count = 0
    for convo in data:
        title = _clean_filename(convo.get("title") or "Conversacion_ChatGPT")
        date_str = convo.get("create_time", datetime.now().isoformat())
        md_content = _generate_frontmatter(title, str(date_str))

        mapping = convo.get("mapping", {})
        for msg_node in mapping.values():
            msg = msg_node.get("message")
            if msg and msg.get("content") and msg["content"].get("parts"):
                role = msg["author"]["role"]
                text = str(msg["content"]["parts"][0])
                role_label = "Human" if role == "user" else "Assistant"
                md_content += f"### {role_label}\n{text}\n\n"

        file_dest = path_out / f"ChatGPT_{title}.md"
        with open(file_dest, "w", encoding="utf-8") as out:
            out.write(md_content)
        count += 1

    print(f"¡Éxito! Se generaron {count} archivos de memoria en '{path_out}'.")


if __name__ == "__main__":
    process_export("chatgpt_chats_real.json")
