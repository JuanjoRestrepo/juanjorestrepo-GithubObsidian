import logging
import textwrap
from pathlib import Path

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def create_scaffold() -> None:
    """Crea la arquitectura base de la Fase 1 de forma idempotente."""

    # 1. Definir la estructura y el contenido
    files_to_create = {
        Path("Templates/Python/pyproject.toml"): textwrap.dedent("""\
            [project]
            name = "project-name"
            version = "0.1.0"
            description = "Descripción del proyecto modular"
            readme = "README.md"
            requires-python = ">=3.12"
            dependencies = [
                "polars>=0.20.0",
                "pydantic>=2.0.0",
                "structlog>=24.1.0",
            ]

            [project.optional-dependencies]
            dev = [
                "pytest>=8.0.0",
                "pytest-cov>=5.0.0",
                "ruff>=0.3.0",
                "mypy>=1.9.0",
            ]

            [tool.ruff]
            target-version = "py312"
            line-length = 88
            select = ["E", "F", "I", "W", "UP", "B", "SIM", "RUF"]

            [tool.mypy]
            python_version = "3.12"
            strict = true
            warn_return_any = true
            warn_unused_configs = true
            disallow_untyped_defs = true
            disallow_incomplete_defs = true

            [tool.pytest.ini_options]
            addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"
            testpaths = ["tests"]
        """),
        Path("Templates/Web/env.ts"): textwrap.dedent("""\
            import { createEnv } from "@t3-oss/env-nextjs";
            import { z } from "zod";

            export const env = createEnv({
              server: {
                DATABASE_URL: z.string().url(),
                NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
                NEXTAUTH_SECRET: process.env.NODE_ENV === "production" ? z.string().min(32) : z.string().min(32).optional(),
                API_KEY_RPA: z.string().min(1),
              },
              client: {
                NEXT_PUBLIC_APP_URL: z.string().url(),
              },
              runtimeEnv: {
                DATABASE_URL: process.env.DATABASE_URL,
                NODE_ENV: process.env.NODE_ENV,
                NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
                API_KEY_RPA: process.env.API_KEY_RPA,
                NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
              },
              emptyStringAsUndefined: true,
            });
        """),
        Path("Context/Architecture_Manifest.md"): textwrap.dedent("""\
            # Manifiesto de Arquitectura e Ingeniería

            ## 1. Principios Fundamentales
            *   **SOLID & DRY:** Responsabilidad única por módulo.
            *   **Separación de Preocupaciones (SoC):** Separar ingesta, modelado y UI.
            *   **Idempotencia:** Ejecuciones repetidas deben producir el mismo estado.

            ## 2. Jerarquía de Integración (RPA / Data)
            1.  **API:** REST/GraphQL autenticado.
            2.  **Direct DB:** Consultas SQL parametrizadas.
            3.  **Native UI:** Selectores nativos, POM.
            4.  **Citrix / Virtualizado:** Último recurso.

            ## 3. Observabilidad y Testing
            *   **Logging:** JSON estructurado obligatorio. Cero `print()`.
            *   **Cobertura:** >= 80% requerida.

            ## 4. Gestión de Secretos
            *   Cero secretos hardcodeados. Uso estricto de Secret Managers o .env validados.
        """),
    }

    # 2. Ejecutar la creación
    for file_path, content in files_to_create.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
            logging.info(f"Creado: {file_path}")
        else:
            logging.warning(f"Omitido (ya existe): {file_path}")


if __name__ == "__main__":
    create_scaffold()
    logging.info("Fase 1 completada exitosamente.")
