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
