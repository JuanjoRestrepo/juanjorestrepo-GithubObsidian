# Advanced Bash Scripting

## Table of Contents
1. Script Foundations and Safety Options
2. Variables, Arrays, and Parameter Expansion
3. Process Substitution and Redirection Mastery
4. Control Flow
5. Functions — Scope, Namerefs, Return Codes
6. Error Handling — trap ERR / EXIT / SIGTERM
7. CLI Argument Parsing with getopts
8. Job Control and Parallelism
9. Data Engineering Shell Patterns

---

## §1 Script Foundations and Safety Options

Every production Bash script must open with:

```bash
#!/usr/bin/env bash
# Description: What this script does, who owns it, last modified
# Usage: ./script.sh [OPTIONS] <input_file>
set -euo pipefail

# set -e  : Exit immediately on any non-zero return code
# set -u  : Treat unset variables as errors (catches typos in var names)
# set -o pipefail : A pipeline fails if ANY command in it fails (not just the last)
# Combined: set -euo pipefail — the minimum acceptable safety baseline

# Optional additions:
set -E          # ERR trap is inherited by functions and subshells
shopt -s nullglob    # Globs that match nothing expand to nothing (not the literal pattern)
shopt -s globstar    # Enable ** recursive glob matching
```

**Strict mode interaction with common patterns:**

```bash
# set -u will break this idiom — replace with explicit default:
# BAD:  if [ -z "$OPTIONAL_VAR" ]; then ...
# GOOD:
OPTIONAL_VAR="${OPTIONAL_VAR:-}"   # Safe default to empty string

# set -e will break grep when it finds no matches (exit 1 is a grep "no match" signal):
grep "pattern" file || true        # Suppress non-zero exit when no match is acceptable
```

---

## §2 Variables, Arrays, and Parameter Expansion

### Indexed Arrays

```bash
declare -a files=("data_2024_01.csv" "data_2024_02.csv" "data_2024_03.csv")
echo "${files[0]}"          # First element
echo "${files[@]}"          # All elements (quoted — safe with spaces)
echo "${#files[@]}"         # Array length
files+=("data_2024_04.csv") # Append

for f in "${files[@]}"; do
    echo "Processing: $f"
done
```

### Associative Arrays (Key-Value Maps)

```bash
declare -A db_config=(
    [host]="postgres.internal"
    [port]="5432"
    [dbname]="airflow"
)
echo "${db_config[host]}"
echo "${!db_config[@]}"   # Print all keys
echo "${db_config[@]}"    # Print all values

for key in "${!db_config[@]}"; do
    echo "$key = ${db_config[$key]}"
done
```

### Parameter Expansion Reference

```bash
VAR="hello_world.csv"

${VAR:-"default"}        # Use default if VAR is unset or empty
${VAR:="default"}        # Assign default if unset or empty (modifies VAR)
${VAR:?"Error: VAR required"}  # Exit with error message if unset or empty
${VAR:+value}            # Use value only if VAR is set and non-empty

${#VAR}                  # String length: 15
${VAR^}                  # Uppercase first char: Hello_world.csv
${VAR^^}                 # Uppercase all: HELLO_WORLD.CSV
${VAR,}                  # Lowercase first char
${VAR,,}                 # Lowercase all: hello_world.csv

# Prefix/suffix removal
${VAR#*_}                # Remove shortest match from front:  world.csv
${VAR##*_}               # Remove longest match from front:   csv  (greedy)
${VAR%.*}                # Remove shortest match from end:    hello_world
${VAR%%.*}               # Remove longest match from end:     hello_world

# Substring: ${VAR:offset:length}
${VAR:0:5}               # hello

# Replacement: ${VAR/pattern/replacement}
${VAR/_/-}               # Replace first underscore: hello-world.csv
${VAR//_/-}              # Replace all underscores:  hello-world.csv
```

---

## §3 Process Substitution and Redirection Mastery

### Process Substitution

Process substitution `<(cmd)` makes a command's output appear as a file descriptor. This is distinct from command substitution `$(cmd)` which captures output as a string.

```bash
# Diff two query results without temp files
diff <(psql -Atc "SELECT id FROM table_a ORDER BY id" "$CONN_A") \
     <(psql -Atc "SELECT id FROM table_b ORDER BY id" "$CONN_B")

# Read multiple streams in a loop simultaneously
while IFS=',' read -r col1 col2 col3; do
    echo "Processing: $col1"
done < <(tail -n +2 data.csv)   # Skip header, feed CSV rows

# Tee to multiple destinations including transformations
pipeline_output | tee >(gzip > output.csv.gz) >(wc -l >> row_counts.log) > /dev/null
```

### Redirection Mastery

```bash
cmd > file        # Redirect stdout to file (overwrite)
cmd >> file       # Append stdout to file
cmd 2> err.log    # Redirect stderr to file
cmd 2>&1          # Redirect stderr to wherever stdout currently goes
cmd &> file       # Redirect both stdout and stderr to file (Bash 4+)
cmd > file 2>&1   # POSIX-compatible equivalent of &>
cmd 2>&1 | tee combined.log    # Pipe both streams through tee

# Discard output
cmd > /dev/null 2>&1

# Named pipe (FIFO) for producer/consumer decoupling
mkfifo /tmp/pipeline_fifo
producer_cmd > /tmp/pipeline_fifo &
consumer_cmd < /tmp/pipeline_fifo
rm /tmp/pipeline_fifo
```

### Heredoc Patterns

```bash
# Feed multi-line SQL to psql
psql "$DATABASE_URL" <<'SQL'
    INSERT INTO pipeline_runs (dag_id, run_date, status)
    VALUES ('etl_daily', CURRENT_DATE, 'started');
SQL
# Single-quoted 'SQL' delimiter: NO variable expansion inside

# Variable expansion enabled (double-quoted or unquoted delimiter)
psql "$DATABASE_URL" <<SQL
    UPDATE pipeline_runs SET status='complete' WHERE run_date='${RUN_DATE}';
SQL
```

---

## §4 Control Flow

```bash
# Numeric comparison: use (( )) or -lt/-gt/-eq
if (( row_count > 1000000 )); then
    echo "Switching to Polars for large dataset"
fi

# String comparison: use [[ ]] (safer than [ ])
if [[ "$ENV" == "production" ]]; then
    echo "Production guards active"
fi

# File tests
[[ -f "$FILE" ]]    # Is a regular file
[[ -d "$DIR" ]]     # Is a directory
[[ -r "$FILE" ]]    # Is readable
[[ -s "$FILE" ]]    # Exists and is non-empty
[[ -L "$LINK" ]]    # Is a symbolic link

# case with glob patterns — distro detection
case "$(. /etc/os-release && echo "$ID")" in
    ubuntu|debian)
        PKG_MANAGER="apt"
        ;;
    rhel|rocky|centos|almalinux)
        PKG_MANAGER="dnf"
        ;;
    *)
        echo "Unsupported distro" >&2
        exit 1
        ;;
esac

# select menu — interactive script prompts
PS3="Select environment: "
select env in development staging production quit; do
    case "$env" in
        production) CONN_STR="$PROD_DB_URL" ; break ;;
        staging)    CONN_STR="$STAGE_DB_URL"; break ;;
        quit)       exit 0 ;;
    esac
done
```

---

## §5 Functions — Scope, Namerefs, Return Codes

```bash
# Local scope is NOT automatic — always declare local
setup_logging() {
    local log_dir="${1:?setup_logging: log_dir argument required}"
    local log_level="${2:-INFO}"

    mkdir -p "$log_dir"
    echo "$(date -Iseconds) [$log_level] Logging initialized: $log_dir"
}

# Returning data from functions: use a nameref (avoid subshell overhead)
# Subshell approach (slow — spawns new process):
# result=$(compute_checksum "$file")

# Nameref approach (fast — no subprocess):
compute_checksum() {
    local file="${1:?file required}"
    local -n result_ref="${2:?result variable name required}"   # nameref: -n
    result_ref="$(sha256sum "$file" | cut -d' ' -f1)"
}

compute_checksum "/data/raw/batch.parquet" checksum_val
echo "Checksum: $checksum_val"

# Return codes: 0=success, 1-255=failure; use for boolean logic
is_file_complete() {
    local file="${1:?}"
    local expected_lines="${2:?}"
    local actual_lines
    actual_lines="$(wc -l < "$file")"
    (( actual_lines >= expected_lines ))  # Last expression exit code is the return
}

if is_file_complete "/data/raw/batch.csv" 100000; then
    echo "File complete"
fi
```

---

## §6 Error Handling — trap ERR / EXIT / SIGTERM

```bash
#!/usr/bin/env bash
set -euo pipefail

# ─── State tracking ─────────────────────────────────────────────
TEMP_DIR=""
PIPELINE_STATUS="UNKNOWN"

# ─── Cleanup handler (always runs — success and failure) ────────
cleanup() {
    local exit_code=$?
    if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
        echo "$(date -Iseconds) [INFO] Cleaned up temp dir: $TEMP_DIR"
    fi
    echo "$(date -Iseconds) [INFO] Pipeline exited with status: $exit_code"
    exit "$exit_code"
}

# ─── Error handler (runs on any non-zero exit) ──────────────────
error_handler() {
    local exit_code=$?
    local line_number=${BASH_LINENO[0]}
    local command="$BASH_COMMAND"
    echo "$(date -Iseconds) [ERROR] Command failed at line $line_number: $command (exit: $exit_code)" >&2
    PIPELINE_STATUS="FAILED"
}

# ─── Graceful shutdown for Airflow/systemd SIGTERM ──────────────
sigterm_handler() {
    echo "$(date -Iseconds) [WARN] SIGTERM received — shutting down gracefully" >&2
    PIPELINE_STATUS="TERMINATED"
    # Allow in-flight work to complete
    wait
    exit 143  # 128 + SIGTERM(15) — standard convention
}

trap cleanup EXIT
trap error_handler ERR
trap sigterm_handler SIGTERM SIGINT

# ─── Main ───────────────────────────────────────────────────────
TEMP_DIR="$(mktemp -d /var/tmp/pipeline.XXXXXX)"
echo "$(date -Iseconds) [INFO] Working dir: $TEMP_DIR"

# ... pipeline logic here ...
PIPELINE_STATUS="SUCCESS"
```

---

## §7 CLI Argument Parsing with getopts

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<USAGE
Usage: $(basename "$0") -e <env> -d <date> [-v] [-h]

Options:
  -e ENV    Target environment (dev|staging|prod) [required]
  -d DATE   Run date in YYYY-MM-DD format [required]
  -v        Verbose output
  -h        Show this help

Example:
  $(basename "$0") -e prod -d 2024-09-15 -v
USAGE
}

ENV=""
RUN_DATE=""
VERBOSE=false

while getopts ":e:d:vh" opt; do
    case "$opt" in
        e) ENV="$OPTARG" ;;
        d) RUN_DATE="$OPTARG" ;;
        v) VERBOSE=true ;;
        h) usage; exit 0 ;;
        :) echo "Error: -$OPTARG requires an argument" >&2; usage; exit 1 ;;
        \?) echo "Error: unknown option -$OPTARG" >&2; usage; exit 1 ;;
    esac
done
shift $(( OPTIND - 1 ))   # Remove parsed options; $@ now holds positional args

[[ -z "$ENV" ]]      && { echo "Error: -e ENV is required" >&2; exit 1; }
[[ -z "$RUN_DATE" ]] && { echo "Error: -d DATE is required" >&2; exit 1; }

$VERBOSE && echo "[DEBUG] ENV=$ENV RUN_DATE=$RUN_DATE"
```

---

## §8 Job Control and Parallelism

```bash
# Background a job
long_running_process &
BG_PID=$!

# Wait for specific PID
wait "$BG_PID"
echo "Exit code: $?"

# Wait for ALL background jobs; capture any failures
pids=()
for shard in 01 02 03 04; do
    process_shard.sh "$shard" &
    pids+=($!)
done

failed=0
for pid in "${pids[@]}"; do
    wait "$pid" || (( failed++ ))
done
(( failed == 0 )) || { echo "ERROR: $failed shard(s) failed" >&2; exit 1; }

# Prevent a backgrounded job from receiving SIGHUP when shell exits
nohup long_job.sh > /var/log/long_job.log 2>&1 &
disown "$!"   # Remove from job table entirely
```

### xargs for Parallel Bulk Processing

```bash
# Process 8 files in parallel, 1 file per job
find /data/raw/ -name "*.csv" -print0 | \
    xargs -0 -P 8 -I {} bash -c 'process_file.sh "{}" || echo "FAILED: {}" >> /tmp/failures.log'

# Parallel with a shell function (requires export -f)
export -f process_file
find /data/raw/ -name "*.csv" | xargs -P 8 -I {} bash -c 'process_file "$@"' _ {}
```

### GNU Parallel (Preferred for Complex Parallelism)

```bash
# apt install parallel  /  dnf install parallel
find /data/raw/ -name "*.parquet" | \
    parallel --jobs 8 --joblog /var/log/parallel_run.log \
             --results /var/log/parallel_results/ \
             "python3 /opt/etl/transform.py {}"

# CSV column as job argument
parallel --colsep ',' python3 load_partition.py {1} {2} :::: partitions.csv
```

---

## §9 Data Engineering Shell Patterns

### Bulk CSV Processing Without Python

```bash
# Column extraction and transformation
cut -d',' -f1,3,5 raw.csv | sort -t',' -k2,2n | uniq > filtered.csv

# Count rows excluding header
tail -n +2 data.csv | wc -l

# Split large CSV into 1M-row chunks with header preservation
header=$(head -1 large.csv)
tail -n +2 large.csv | split -l 1000000 --filter='{ echo "$header"; cat; } > $FILE.csv' - chunk_

# Find files modified in last 24h (pipeline monitoring)
find /data/landing/ -name "*.csv" -mtime -1 -size +0c
```

### Filesystem-Triggered Pipeline Execution (inotifywait)

```bash
# apt install inotify-tools  /  dnf install inotify-tools
inotifywait -m -e close_write --format '%w%f' /data/landing/ | \
while IFS= read -r filepath; do
    [[ "$filepath" == *.csv ]] || continue
    echo "$(date -Iseconds) [INFO] New file detected: $filepath"
    python3 /opt/etl/ingest.py --file "$filepath" &
done
```

### Log Aggregation Pipelines

```bash
# Stream multiple service logs, tag by source, feed to a processor
{ tail -F /var/log/airflow/scheduler.log | sed 's/^/[airflow-scheduler] /';
  tail -F /var/log/spark/master.log      | sed 's/^/[spark-master] /';
} | grep -E "ERROR|WARN|CRITICAL" | tee /var/log/combined_errors.log
```

### Credential Injection from Environment File

```bash
# /etc/pipeline/.env (mode 640, owned by root:pipelineuser — never committed to git)
# DB_PASSWORD=secret123

# Source without exporting to child processes unless needed
set -a   # Automatically export all subsequent assignments
# shellcheck source=/dev/null
source /etc/pipeline/.env
set +a

# Or selectively export
DB_PASSWORD="$(grep '^DB_PASSWORD=' /etc/pipeline/.env | cut -d'=' -f2-)"
export DB_PASSWORD
```

### ShellCheck Integration

```bash
# Install
apt install shellcheck   # Ubuntu
dnf install ShellCheck   # RHEL

# Lint a script
shellcheck -S warning pipeline.sh

# In pre-commit hook
find . -name "*.sh" -exec shellcheck {} +
```
