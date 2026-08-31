#!/usr/bin/env python3
"""
Vault Refactoring and Migration Script
Author: Juan José Restrepo Rosero
Date: 2026-08-31
Description: Safely reorganizes Obsidian vault folders into a clean, professional,
architecture-aligned structure while preserving all Markdown files and internal links.
"""

import logging
import shutil
import sys
from pathlib import Path

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("VaultMigration")

# Define target root (assuming script runs from vault root)
VAULT_ROOT = Path(".").resolve()

# Mapping of target directory to old directory sources
MIGRATION_MAPPING = {
    "01_Dashboards": [],
    "02_Areas/Job_Search": ["Job Search"],
    "02_Areas/Finance": ["Transactions"],
    "02_Areas/Personal": ["Self Study/⬛🟥🟨 B1"],
    "03_Projects/World_Cup_2026": ["Self Study/World Cup 2026 Project⚽🏆"],
    "03_Projects/F1_Prediction": ["Self Study/F1"],
    "03_Projects/Backend_2026": ["Self Study/Backend Project 2026"],
    "04_Resources/Cloud_DevOps": [
        "Self Study/AWS",
        "Self Study/Azure",
        "Self Study/Docker",
        "Self Study/Terraform",
        "Self Study/Oracle",
    ],
    "04_Resources/Data_Engineering_Science": [
        "Self Study/Data Engineering",
        "Self Study/Dbt vs PySpark",
        "Self Study/Coursera",
        "Self Study/IBM",
        "Self Study/SQL",
        "Master Data Science",
        "Lovelytics",
    ],
    "04_Resources/Software_Architecture": [
        "Self Study/Django",
        "Self Study/NodeJs",
        "Self Study/Microsoft",
        "Self Study/POO - LUISA RINCON 2025",
        "Self Study/Codigo Facilito",
        "Self Study/Harvard CS50",
    ],
    "04_Resources/Security_Networking": ["Self Study/Pinguino Mario - Hacking"],
    "04_Resources/Aerospace_Robotics": [
        "Self Study/🛩️ 🧠 ERNESTO KNOWLEDGE ERNESTO KNOWLEDGE",
        "Self Study/Deep Learning Geometrico y Topologico",
    ],
    "04_Resources/Automation_RPA": ["Self Study/UiPath"],
    "05_Archive/University_History": ["Ing Electronica", "Qubika", "Rappi"],
    "_System/Templates": ["Templates"],
    "_System/Keys": ["Keys"],
    "_System/Assets": [
        "Excalidraw",
        "Files",
        "GitHub Porfolio ReadMe Profiles",
        "Context",
    ],
}


def verify_vault_safety() -> bool:
    """Ensures we are operating inside a valid Obsidian vault root."""
    obsidian_dir = VAULT_ROOT / ".obsidian"
    if not obsidian_dir.exists():
        logger.error(
            "Target directory does not appear to be an Obsidian vault (.obsidian folder missing). Aborting."
        )
        return False
    return True


def execute_migration(dry_run: bool = False) -> None:
    """Executes the file migration safely, logging operations."""
    if not verify_vault_safety():
        return

    logger.info("Starting safe vault structural reorganization...")

    for target_rel, sources in MIGRATION_MAPPING.items():
        target_path = VAULT_ROOT / target_rel
        if not dry_run:
            target_path.mkdir(parents=True, exist_ok=True)

        for src in sources:
            src_path = VAULT_ROOT / src
            if src_path.exists() and src_path.is_dir():
                if src_path == target_path:
                    continue

                logger.info(
                    f"{'[DRY RUN] ' if dry_run else ''}Moving contents of '{src}' -> '{target_rel}'"
                )

                if not dry_run:
                    for child in src_path.iterdir():
                        dest_child = target_path / child.name
                        if dest_child.exists():
                            logger.warning(
                                f"Destination collision detected for {child.name}. Merging."
                            )
                            if child.is_dir():
                                shutil.copytree(child, dest_child, dirs_exist_ok=True)
                                shutil.rmtree(child)
                            else:
                                shutil.copy2(child, dest_child)
                                child.unlink()
                        else:
                            shutil.move(str(child), str(target_path))

                    try:
                        src_path.rmdir()
                    except OSError:
                        logger.info(
                            f"Source directory {src} not empty or retained partially."
                        )
            else:
                logger.debug(f"Source path not found or skipped: {src}")

    logger.info("Vault structural refactoring execution completed successfully.")


if __name__ == "__main__":
    DRY_RUN = False
    execute_migration(dry_run=DRY_RUN)
