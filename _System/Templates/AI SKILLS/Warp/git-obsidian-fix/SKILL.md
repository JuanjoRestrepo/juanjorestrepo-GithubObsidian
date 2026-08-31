# Obsidian Git Sync & Conflict Resolution

**Author:** Git Workflow Specialist  
**Standard:** Professional DevOps / High-Reliability Sync  
**Scope:** Multi-OS (macOS/Windows) Vault Management

---

## 1. Core Architecture & Prevention

El mayor problema al usar Git con Obsidian es el "ruido" de archivos de estado. Para evitar conflictos recurrentes entre Mac y Windows, es mandatorio ignorar los archivos de entorno local.

### `.gitignore` Recomendado

Crea este archivo en la raíz de tu vault para asegurar que las configuraciones de UI no colisionen:

```plaintext
# Obsidian system files
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json
.obsidian/appearance.json

# OS specific files
.DS_Store
Thumbs.db
```

---

## 2. Standard Operating Procedures (SOP)

### Caso A: El repositorio ha divergido (Diverged Branches)

**Escenario:**  
Hiciste commit en Windows, hiciste commit en Mac, y ahora `origin/main` y `local/main` tienen historias distintas.

**Solución Profesional: Atomic Rebase**

```bash
# Preservar estado actual
git stash

# Sincronizar historia
git pull origin main --rebase

# Reaplicar cambios
git stash pop
```

---

### Caso B: Recuperación de Archivos Borrados Accidentalmente

**Escenario:**  
El estado local marca un `deleted` que no deseas confirmar.

**Comando:**

```bash
git restore "ruta/al/archivo/borrado.md"
```

**Nota:**  
Si son múltiples archivos, usa:

```bash
git restore .
```

---

## 3. Workflow de Resolución de Conflictos

Si al hacer `git stash pop` o `rebase` encuentras conflictos en archivos `.md`:

### Identificar archivos afectados

```bash
git status --short
```

### Estrategia de resolución (Manual)

Abre el archivo en Obsidian o VS Code. Busca los marcadores:

```plaintext
<<<<<<< HEAD
# Tus cambios locales
=======
# Cambios del otro sistema
>>>>>>> [hash]
```

### Finalizar resolución

```bash
git add <archivo_resuelto>
git rebase --continue
```

---

## 4. Automation & Best Practices

| Práctica           | Razón Técnica                                                                   |
| ------------------ | ------------------------------------------------------------------------------- |
| Commit-per-Session | Evita colisiones masivas. Haz commit al terminar de escribir en un dispositivo. |
| Atomic Commits     | No mezcles cambios de configuración de Obsidian con notas de estudio.           |
| Pull before Write  | Ejecuta `git pull` al abrir Obsidian en un nuevo SO para evitar divergencias.   |
| SSH Keys           | Configura llaves SSH en Mac y Windows para evitar prompts constantes.           |

---

## 5. Troubleshooting (Quick Reference)

### Error: `cannot pull with rebase: You have unstaged changes`

**Causa:**  
Tienes archivos modificados que no han sido ni commiteados ni guardados.

**Fix:**

```bash
git add .
git stash
git pull origin main --rebase
git stash pop
```

---

### Error: `Permission denied (publickey)` en macOS

**Fix:**

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

---

### Forzar estado del remoto (Último recurso)

Si tu versión local es un desastre y la de Windows (en GitHub) es la correcta:

```bash
git fetch origin
git reset --hard origin/main
```

---
