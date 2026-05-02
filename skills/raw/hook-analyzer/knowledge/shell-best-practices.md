# Shell Best Practices

> **Usage**: Reference document for shell scripting best practices and anti-patterns. Load this when analyzing hooks for code quality and reliability issues (Phase 2: Analysis).

---

## 1. Exit Codes and Error Handling

### 1.1 Proper Exit Code Usage

```bash
# Good: Explicit exit codes
exit 0      # Success
exit 1      # General error
exit 2      # Misuse of shell command
exit 126    # Command not executable
exit 127    # Command not found
exit 128+N  # Signal N (e.g., 130 = Ctrl+C = 128+2)

# Good: Capture exit code properly
some_command
exit_code=$?
if [[ $exit_code -ne 0 ]]; then
    echo "Command failed with exit code $exit_code" >&2
    exit $exit_code
fi
```

### 1.2 set Options for Error Handling

```bash
# Required for production scripts
set -e          # Exit on error (but see note below)
set -u          # Exit on undefined variable
set -o pipefail # Pipeline fails if any command fails

# Combined form
set -euo pipefail
```

### 1.3 Anti-Patterns

```bash
# BAD: set -e without understanding
set -e
cmd_that_might_fail || true  # This works but masks errors

# BAD: Ignoring exit codes
grep "pattern" file > /dev/null
# Should be: grep "pattern" file > /dev/null || true
```

### 1.4 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-EXIT-001 | Always use `set -euo pipefail` in scripts | Critical |
| BASH-EXIT-002 | Use explicit exit codes | High |
| BASH-EXIT-003 | Check exit codes for critical operations | High |
| BASH-EXIT-004 | Never use `exit 0` on error | High |

---

## 2. Signal Handling and Trap

### 2.1 Graceful Cleanup

```bash
# Good: Cleanup on exit
cleanup() {
    local exit_code=$?
    # Remove temp files
    rm -f "$temp_file" "$lock_file"
    # Close file descriptors
    exec 3>&-
    # Log exit
    echo "Script exiting with code $exit_code" >> "$log_file"
    exit $exit_code
}

trap cleanup EXIT
trap 'echo "Interrupted" >&2; exit 130' INT TERM
```

### 2.2 Common Signals

| Signal | Number | Description | Common Action |
|--------|--------|-------------|--------------|
| SIGHUP | 1 | Hangup | Reload config |
| SIGINT | 2 | Ctrl+C | Graceful stop |
| SIGTERM | 15 | Termination | Clean shutdown |

### 2.3 Anti-Patterns

```bash
# BAD: No cleanup on failure
temp_file=$(mktemp)
# If script fails here, temp file remains

# BAD: Overly broad trap
trap 'exit 1' ERR  # This can cause unexpected exits

# GOOD: Specific signal handling
trap 'handle_sigterm' TERM
```

### 2.4 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-SIGNAL-001 | Use trap for cleanup on EXIT | High |
| BASH-SIGNAL-002 | Handle SIGINT and SIGTERM | Medium |
| BASH-SIGNAL-003 | Don't trap ERR without understanding | Medium |

---

## 3. Subshell Usage

### 3.1 When to Use Subshells

```bash
# Good: Isolated variable scope
(
    cd /tmp
    # Variables here don't affect parent
    local_var="isolated"
)

# Good: Parallel execution
(
    process_data "dataset1"
) &
(
    process_data "dataset2"
) &
wait
```

### 3.2 Performance Considerations

```bash
# BAD: Unnecessary subshell in loop
for file in *.txt; do
    content=$(cat "$file")  # Subshell per iteration - slow
done

# GOOD: Use while read
while IFS= read -r line; do
    process "$line"
done < file.txt
```

### 3.3 Subshell vs Command Substitution

```bash
# Command substitution creates subshell
result=$(some_command)  # Subshell created

# Pipelines also create subshells (in bash 4.2+ with pipefail)
cat file | grep pattern

# Process substitution - no subshell
while read -r line; do
    process "$line"
done < <(command)
```

### 3.4 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-SUB-001 | Avoid subshells in tight loops | Medium |
| BASH-SUB-002 | Use command grouping for isolated side effects | Low |
| BASH-SUB-003 | Use process substitution over pipes when variables needed | Medium |

---

## 4. Variable Scope and Declaration

### 4.1 Local Variables

```bash
# Good: Use local in functions
my_function() {
    local var1="$1"
    local result=""
    # Process
    echo "$result"
}

# Good: Declare variables
declare -i count=0          # Integer
declare -a array=()         # Array
declare -A associative=()    # Associative array
declare -r constant="value" # Readonly
```

### 4.2 Global vs Local

```bash
# BAD: Accidental global in function
process_data() {
    result="processed"  # Creates global if not careful
}

# GOOD: Explicit local
process_data() {
    local result
    result="processed"
    echo "$result"
}
```

### 4.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-VAR-001 | Always use `local` in functions | High |
| BASH-VAR-002 | Use `declare` for type safety | Medium |
| BASH-VAR-003 | Use `readonly` for constants | Low |

---

## 5. Function Patterns

### 5.1 Function Declaration

```bash
# POSIX-compatible (preferred for portability)
function_name() {
    # Code
}

# Bash-specific (more features)
my_function() {
    local arg1="$1"
    shift
    local remaining="$@"
    return 0
}
```

### 5.2 Return Values

```bash
# Good: Use echo for return data, return for status
get_user() {
    local user_id="$1"
    [[ -z "$user_id" ]] && return 1

    local user_data
    user_data=$(find_user "$user_id")
    [[ -z "$user_data" ]] && return 1

    echo "$user_data"
    return 0
}

# Usage
if user_data=$(get_user "$id"); then
    echo "Found: $user_data"
else
    echo "User not found" >&2
fi
```

### 5.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-FUNC-001 | Use return for status, echo for data | High |
| BASH-FUNC-002 | Always use local variables in functions | High |
| BASH-FUNC-003 | Validate function arguments | Medium |

---

## 6. String Operations

### 6.1 Quoting

```bash
# MUST: Quote variable expansions
echo "$variable"
grep "$pattern" "$file"
rm "$file"

# Avoid: Unquoted variables
echo $variable    # Word splitting
echo *            # Glob expansion
```

### 6.2 String Manipulation

```bash
# Length
${#string}

# Substring
${string:start:length}
${string: -5}     # Last 5 chars (space before - is required)

# Replacement
${string/pattern/replacement}
${string//pattern/replacement}
${string/#prefix/replacement}
${string/%suffix/replacement}

# Default values
${var:-default}   # Use default if unset or empty
${var:=default}   # Assign default if unset or empty
${var:?error}     # Error if unset or empty
${var:+alternate} # Use alternate if set
```

### 6.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-STR-001 | Always quote variable expansions | Critical |
| BASH-STR-002 | Use parameter expansion over external commands | Medium |
| BASH-STR-003 | Use [[ for pattern matching | Medium |

---

## 7. Arrays and Iteration

### 7.1 Array Declaration

```bash
# Indexed array
files=(file1.txt file2.txt file3.txt)

# Associative array (requires Bash 4+)
declare -A config
config[key1]="value1"
config[key2]="value2"
```

### 7.2 Iteration Patterns

```bash
# Good: Iterate over array
for file in "${files[@]}"; do
    process "$file"
done

# Good: Iterate with index
for i in "${!files[@]}"; do
    echo "$i: ${files[$i]}"
done

# Good: Read lines into array
mapfile -t lines < file.txt
```

### 7.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-ARR-001 | Always quote array expansions | Critical |
| BASH-ARR-002 | Use proper array iteration | High |
| BASH-ARR-003 | Use mapfile for large file reads | Low |

---

## 8. Input/Output

### 8.1 File Descriptors

```bash
# Standard streams
stdin=0
stdout=1
stderr=2

# Good: Redirect stderr
command 2> error.log

# Good: Redirect both
command > output.log 2>&1

# Good: Redirect to stderr
echo "Error message" >&2

# Good: Use custom file descriptor
exec 3> output.txt
echo "To fd 3" >&3
exec 3>&-
```

### 8.2 Here Documents

```bash
# Good: Multi-line input
cat << EOF
Line 1
Line 2
Variable: $variable
EOF

# Good: With indentation (strip leading tabs)
cat <<-EOF
	Indented content
	EOF
```

### 8.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-IO-001 | Use stderr for errors | High |
| BASH-IO-002 | Redirect stderr after stdout | High |
| BASH-IO-003 | Always quote heredoc delimiters | Medium |

---

## 9. Common Anti-Patterns

### 9.1 Parsing Output

```bash
# BAD: Parsing ls output
files=$(ls -1)  # Fragile with spaces/special chars

# GOOD: Use globbing
for file in *; do
    [[ -f "$file" ]] && process "$file"
done
```

### 9.2 Using External Commands

```bash
# BAD: Using sed for simple substitution
result=$(echo "$var" | sed 's/foo/bar/')

# GOOD: Use bash built-in
result=${var/foo/bar}

# BAD: Using grep then cut
value=$(echo "$text" | grep "pattern" | cut -d: -f2)

# GOOD: Use bash regex
if [[ "$text" =~ pattern:(.+) ]]; then
    value=${BASH_REMATCH[1]}
fi
```

### 9.3 Testing

```bash
# BAD: Using [ for pattern matching
[ "$var" == "pattern" ]

# GOOD: Using [[ for pattern matching
[[ "$var" == "pattern" ]]

# GOOD: Using regex
[[ "$var" =~ ^[[:alnum:]]+$ ]]
```

### 9.4 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-ANTI-001 | Never parse ls output | Critical |
| BASH-ANTI-002 | Use bash built-ins over external commands when possible | Medium |
| BASH-ANTI-003 | Always use [[ over [ for tests | High |

---

## 10. Performance Tips

### 10.1 Command Efficiency

```bash
# BAD: Multiple greps in pipeline
cat file | grep "a" | grep "b" | grep "c"

# GOOD: Single grep with regex
grep "a.*b.*c" file

# BAD: cat for single file
cat file | process

# GOOD: Direct redirection
process < file
```

### 10.2 Caching

```bash
# Good: Cache repeated command results
if [[ -z "$cached_result" ]]; then
    cached_result=$(expensive_command)
fi
```

### 10.3 Best Practice Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| BASH-PERF-001 | Combine multiple greps when possible | Medium |
| BASH-PERF-002 | Avoid unnecessary cat usage | Low |
| BASH-PERF-003 | Cache expensive operations | Low |

---

## 11. Summary Table

| Category | Critical Rules | High Rules | Medium Rules | Low Rules |
|----------|----------------|------------|---------------|-----------|
| Exit Codes | BASH-EXIT-001 | BASH-EXIT-002, BASH-EXIT-003, BASH-EXIT-004 | | |
| Signals | | | BASH-SIGNAL-001, BASH-SIGNAL-002, BASH-SIGNAL-003 | |
| Subshell | | | BASH-SUB-001, BASH-SUB-003 | BASH-SUB-002 |
| Variables | | BASH-VAR-001 | BASH-VAR-002 | BASH-VAR-003 |
| Functions | | BASH-FUNC-001, BASH-FUNC-002 | BASH-FUNC-003 | |
| Strings | BASH-STR-001 | | BASH-STR-002, BASH-STR-003 | |
| Arrays | BASH-ARR-001 | BASH-ARR-002 | | BASH-ARR-003 |
| I/O | | BASH-IO-001, BASH-IO-002 | BASH-IO-003 | |
| Anti-Patterns | BASH-ANTI-001 | BASH-ANTI-003 | BASH-ANTI-002 | |
| Performance | | | BASH-PERF-001, BASH-PERF-002 | BASH-PERF-003 |

---

## 12. References

- Google Shell Style Guide
- Bash Manual
- POSIX Shell Command Language
- ShellCheck Wiki
