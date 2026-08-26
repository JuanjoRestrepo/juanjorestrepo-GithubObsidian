"""
Módulo de Ingestión Multi-Modelo para AI Second Brain.
Soporta exportaciones de ChatGPT, Claude y Gemini.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def process_export(file_path: str, output_dir: str):
    path_out = Path(output_dir)
    path_out.mkdir(parents=True, exist_ok=True)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Detección del esquema (ChatGPT vs Claude vs Gemini)
    if isinstance(data, list) and len(data) > 0 and "mapping" in data[0]:
        print("Detectado esquema: ChatGPT")
        _parse_chatgpt(data, path_out)
    elif isinstance(data, list) and len(data) > 0 and "chat_messages" in data[0]:
        print("Detectado esquema: Claude")
        _parse_claude(data, path_out)
    else:
        # Fallback genérico para Gemini u otros
        print("Detectado esquema: Genérico/Gemini")
        _parse_generic(data, path_out)


def _generate_frontmatter(title: str, date_str: str) -> str:
    return f"---\ntitle: {title}\ndate: {date_str}\ntags: [ai_memory, context]\n---\n\n"


def _parse_chatgpt(data, path_out):
    for convo in data:
        title = convo.get("title", "Memoria_GPT").replace("/", "_")
        date_str = convo.get("create_time", datetime.now().isoformat())
        md_content = _generate_frontmatter(title, date_str)

        for msg_node in convo.get("mapping", {}).values():
            msg = msg_node.get("message")
            if msg and msg.get("content") and msg["content"].get("parts"):
                role = msg["author"]["role"]
                text = str(msg["content"]["parts"][0])
                md_content += f"### {role.capitalize()}\n{text}\n\n"

        _write_file(path_out / f"{title}.md", md_content)


def _parse_claude(data, path_out):
    for convo in data:
        title = convo.get("chat_title", "Memoria_Claude").replace("/", "_")
        date_str = convo.get("created_at", datetime.now().isoformat())
        md_content = _generate_frontmatter(title, date_str)

        for msg in convo.get("chat_messages", []):
            role = msg.get("sender", "user")
            text = msg.get("text", "")
            md_content += f"### {role.capitalize()}\n{text}\n\n"

        _write_file(path_out / f"{title}.md", md_content)


def _parse_generic(data, path_out):
    # Lógica de fallback para extraer texto de diccionarios planos
    for i, convo in enumerate(data):
        title = f"Memoria_Generica_{i}"
        md_content = _generate_frontmatter(title, datetime.now().isoformat())
        md_content += f"```json\n{json.dumps(convo, indent=2)}\n```\n"
        _write_file(path_out / f"{title}.md", md_content)


def _write_file(file_dest, content):
    with open(file_dest, "w", encoding="utf-8") as out:
        out.write(content)


if __name__ == "__main__":
    # Ejecuta el script apuntando a tu archivo de exportación
    export_file = "ruta_a_tu_archivo_exportado.json"
    if os.path.exists(export_file):
        process_export(export_file, "Context/AI_Memory/")
    else:
        print(f"Por favor coloca tu archivo JSON en la ruta: {export_file}")
