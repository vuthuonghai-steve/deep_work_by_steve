# Shell Security Standards

> **Usage**: Reference document for detecting security vulnerabilities in shell scripts. Load this when analyzing hooks for security issues (Phase 2: Analysis).

---

## 1. Command Injection

### 1.1 Vulnerability Description

Command injection occurs when shell commands use untrusted input without proper sanitization. Attackers can execute arbitrary commands by injecting metacharacters.

### 1.2 Vulnerable Patterns

| Pattern | Example | Risk |
|---------|---------|------|
| Unquoted variables in backticks | `` cmd=`cat $file` `` | Critical |
| Unquoted variables with `$( )` | `cmd=$(cat $file)` | Critical |
| String concatenation | `cmd="ls $dir"` | Critical |
| eval usage | `eval "ls $input"` | Critical |
| pipe to shell | `echo $input \| bash` | Critical |

### 1.3 Secure Patterns

```bash
# SECURE: Always quote variables
cmd=$(cat "$file")
ls "$directory"

# SECURE: Use array for arguments
args=(-l "$filename")
ls "${args[@]}"

# SECURE: Validate input with case match
case "$input" in
    [a-zA-Z0-9_]*) safe_input="$input" ;;
    *) echo "Invalid input" >&2; exit 1 ;;
esac
```

### 1.4 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-CMD-001 | Unquoted variable in command substitution | Critical |
| SEC-CMD-002 | Use of `eval` with variable | Critical |
| SEC-CMD-003 | Pipe to `/bin/sh` or `bash` | Critical |
| SEC-CMD-004 | String concatenation in command | High |

---

## 2. Path Traversal

### 2.1 Vulnerability Description

Path traversal allows attackers to access files outside the intended directory by using `../` sequences.

### 2.2 Vulnerable Patterns

```bash
# VULNERABLE: No path validation
cat "$user_file"
cp "$src" "$dst"
```

### 2.3 Secure Patterns

```bash
# SECURE: Resolve and validate path
realpath_user() {
    local path="$1"
    local base_dir="$2"

    # Resolve to absolute path
    local real_path
    real_path=$(realpath "$path" 2>/dev/null) || return 1

    # Check if path is within base directory
    case "$real_path" in
        "$base_dir"/*) echo "$real_path" ;;
        *) return 1 ;;
    esac
}

# Usage
safe_file=$(realpath_user "$user_file" "$PROJECT_DIR") || {
    echo "Path traversal attempt detected" >&2
    exit 1
}
```

### 2.4 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-PATH-001 | File operations without path validation | High |
| SEC-PATH-002 | Use of `../` in user-controlled paths | High |
| SEC-PATH-003 | No check for null bytes in paths | Medium |

---

## 3. Privilege Escalation

### 3.1 Vulnerability Description

Scripts may inadvertently create opportunities for privilege escalation through world-writable files, insecure temp files, or improper permission handling.

### 3.2 Vulnerable Patterns

```bash
# VULNERABLE: World-writable temp file
temp_file="/tmp/config_$RANDOM"

# VULNERABLE: Using temp file without umask
touch /tmp/output

# VULNERABLE: Running commands with elevated privileges unnecessarily
sudo rm -rf /
```

### 3.3 Secure Patterns

```bash
# SECURE: Private temp file
temp_file=$(mktemp)
trap 'rm -f "$temp_file"' EXIT

# SECURE: Explicit umask
umask 077
temp_dir=$(mktemp -d)

# SECURE: Check for sudo usage necessity
if [[ "$EUID" -ne 0 ]] && [[ -w "/etc/" ]]; then
    echo "Warning: Running without sudo but /etc is writable"
fi
```

### 3.4 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-PRIV-001 | World-writable file creation | High |
| SEC-PRIV-002 | Insecure temp file naming | Medium |
| SEC-PRIV-003 | Unnecessary sudo usage | Low |

---

## 4. Input Validation

### 4.1 Vulnerability Description

Lack of input validation can lead to various attacks including command injection, path traversal, and unexpected behavior.

### 4.2 Validation Checklist

```bash
# REQUIRED: Validate all external input
validate_input() {
    local input="$1"
    local input_name="$2"

    # Check for empty input
    [[ -z "$input" ]] && {
        echo "Error: $input_name is empty" >&2
        return 1
    }

    # Check for null bytes (file injection)
    [[ "$input" == *$'\0'* ]] && {
        echo "Error: $input_name contains null bytes" >&2
        return 1
    }

    # Check for control characters (except newline)
    if [[ "$input" =~ [[:cntrl:]] ]] && [[ "$input" != *$'\n'* ]]; then
        echo "Error: $input_name contains control characters" >&2
        return 1
    fi

    # Check length limits
    [[ ${#input} -gt 4096 ]] && {
        echo "Error: $input_name exceeds maximum length" >&2
        return 1
    }

    return 0
}
```

### 4.3 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-INPUT-001 | Missing input validation for external data | High |
| SEC-INPUT-002 | No length check on user input | Medium |
| SEC-INPUT-003 | No null byte check | Medium |

---

## 5. Secure Variable Handling

### 5.1 Vulnerability Description

Improper handling of variables can lead to word splitting, pathname expansion, and unexpected command execution.

### 5.2 Secure Patterns

```bash
# SECURE: Always quote variable expansions
echo "$variable"
cat "$file"

# SECURE: Disable globbing and splitting
set -f
set -- "$variable"

# SECURE: Use IFS for splitting controlled input
IFS=',' read -ra parts <<< "$csv_input"

# SECURE: Mark as integer when needed
declare -i count=0
```

### 5.3 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-VAR-001 | Unquoted variable expansion | Medium |
| SEC-VAR-002 | Missing `set -f` before glob-prone operations | Low |
| SEC-VAR-003 | Use of uninitialized variables | Medium |

---

## 6. Race Conditions

### 6.1 Vulnerability Description

Time-of-check to time-of-use (TOCTOU) vulnerabilities occur when file checks and operations are not atomic.

### 6.2 Vulnerable Patterns

```bash
# VULNERABLE: TOCTOU race condition
if [[ -w "$file" ]]; then
    echo "data" > "$file"  # File might become unwritable between check and write
fi
```

### 6.3 Secure Patterns

```bash
# SECURE: Use noclobber and atomic operations
set -o noclobber
echo "data" > "$file" 2>/dev/null || handle_error

# SECURE: Use redirects with explicit error handling
if ! printf '%s' "data" > "$file"; then
    echo "Cannot write to $file" >&2
    exit 1
fi
```

### 6.4 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-RACE-001 | TOCTOU pattern in file operations | High |

---

## 7. Environment Variable Security

### 7.1 Vulnerability Description

Environment variables can be manipulated by attackers to control script behavior, inject code, or bypass security checks.

### 7.2 Vulnerable Patterns

```bash
# VULNERABLE: Using PATH from environment
ls  # May execute malicious $PATH

# VULNERABLE: Trusting IFS from environment
# VULNERABLE: Trusting LC_* variables
```

### 7.3 Secure Patterns

```bash
# SECURE: Sanitize environment
unset IFS
unset ENV
unset BASH_ENV

# SECURE: Use absolute paths
export PATH=/usr/local/bin:/usr/bin:/bin

# SECURE: Reset locale variables
export LANG=C
export LC_ALL=C
```

### 7.4 Detection Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| SEC-ENV-001 | Use of relative command paths | High |
| SEC-ENV-002 | No environment sanitization | Medium |
| SEC-ENV-003 | Trusting IFS/ENV from environment | Medium |

---

## 8. Summary Table

| Category | Critical Rules | High Rules | Medium Rules | Low Rules |
|----------|----------------|------------|---------------|-----------|
| Command Injection | SEC-CMD-001, SEC-CMD-002, SEC-CMD-003 | SEC-CMD-004 | | |
| Path Traversal | | SEC-PATH-001, SEC-PATH-002 | SEC-PATH-003 | |
| Privilege Escalation | | SEC-PRIV-001 | SEC-PRIV-002 | SEC-PRIV-003 |
| Input Validation | | SEC-INPUT-001 | SEC-INPUT-002, SEC-INPUT-003 | |
| Variable Handling | | | SEC-VAR-001, SEC-VAR-003 | SEC-VAR-002 |
| Race Conditions | | SEC-RACE-001 | | |
| Environment | | SEC-ENV-001 | SEC-ENV-002, SEC-ENV-003 | |

---

## 9. References

- OWASP Command Injection
- CWE-78: OS Command Injection
- CWE-22: Path Traversal
- CWE-379: Creation of Temporary File With Insecure Permissions
- POSIX Shell Command Language Specification
