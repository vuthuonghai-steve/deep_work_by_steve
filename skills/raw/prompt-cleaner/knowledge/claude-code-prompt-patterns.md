# Claude Code Prompt Patterns — Complete Reference

> **Usage**: Load when not sure about tag syntax or need examples. Reference for writing structured prompts.
> Nguồn: Tổng hợp từ 7 tool reference tại `/home/steve/Work-space/siin/system-prompts-and-models-of-ai-tools/`

---

## 1. XML Tags Patterns

### 1.1 Claude Code Block Tags

**Source**: `Anthropic/Claude Code 2.0.txt`, `Sonnet 4.6 Prompt.txt`

```xml
<!-- Top-level Claude Sonnet 4.6 Structure -->
<claude_behavior>
  <product_information>...</product_information>
  <refusal_handling>...</refusal_handling>
  <legal_and_financial_advice>...</legal_and_financial_advice>
  <tone_and_formatting>
    <lists_and_bullets>...</lists_and_bullets>
  </tone_and_formatting>
  <anthropic_reminders>...</anthropic_reminders>
</claude_behavior>

<memory_system>...</memory_system>
<persistent_storage_for_artifacts>...</persistent_storage_for_artifacts>

<search_instructions>
  <core_search_behaviors>...</core_search_behaviors>
  <search_usage_guidelines>...</search_usage_guidelines>
  <CRITICAL_COPYRIGHT_COMPLIANCE>...</CRITICAL_COPYRIGHT_COMPLIANCE>
  <copyright_examples>...</copyright_examples>
  <harmful_content_safety>...</harmful_content_safety>
  <critical_reminders>...</critical_reminders>
</search_instructions>

<using_image_search_tool>...</using_image_search_tool>
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
<filesystem_configuration>...</filesystem_configuration>
<artifacts>...</artifacts>
<current_context>...</current_context>
```

### 1.2 Windsurf Section Tags

**Source**: `Windsurf/Prompt Wave 11.txt`

```xml
<!-- Windsurf Named Section Tags -->
<user_information>
  OS version, workspace URIs, workspace mappings
</user_information>

<tool_calling>
  Keep working until task complete. Make all necessary tool calls.
  DO NOT ask for confirmation. When all steps are done, report to user.
</tool_calling>

<making_code_changes>
  [Hướng dẫn thay đổi code cụ thể]
</making_code_changes>

<debugging>
  [Chiến lược debug]
</debugging>

<memory_system>
  Persistent memory instructions
</memory_system>

<code_research>
  Research before coding
</code_research>

<running_commands>
  Terminal command rules
</running_commands>

<browser_preview>
  Preview rules
</browser_preview>

<calling_external_apis>
  API integration guidelines
</calling_external_apis>

<communication_style>
  2nd person, markdown formatting
</communication_style>

<planning>
  Plan state management
</planning>
```

### 1.3 Replit Proposed Actions Tags

**Source**: `Replit/Prompt.txt`, `Replit/Tools.json`

```xml
<!-- Replit XML Proposed Actions -->
<proposed_file_replace_substring>
  file_path: string
  change_summary: string
  old_str: string
  new_str: string
</proposed_file_replace_substring>

<proposed_file_replace>
  file_path: string
  change_summary: string
  content: <![CDATA[
    [Full file content here]
  ]]>
</proposed_file_replace>

<proposed_file_insert>
  file_path: string
  change_summary: string
  line_number: number
  content: <![CDATA[
    [Content to insert]
  ]]>
</proposed_file_insert>

<proposed_file_delete>
  file_path: string
  change_summary: string
  line_start: number
  line_end: number
</proposed_file_delete>

<proposed_shell_command>
  working_directory: optional
  is_dangerous: boolean
  content: string
</proposed_shell_command>

<proposed_package_install>
  language: string
  package_list: string
</proposed_package_install>

<proposed_workflow_configuration>
  workflow_name: string
  set_run_button: boolean
  mode: "parallel" | "sequential"
</proposed_workflow_configuration>

<proposed_deployment_configuration>
  build_command: optional
  run_command: string
</proposed_deployment_configuration>

<proposed_workspace_tool_nudge>
  tool: string
</proposed_workspace_tool_nudge>

<proposed_actions summary="max 58 chars">
  [Summary of all proposed actions]
</proposed_actions>
```

### 1.4 Perplexity Block XML Tags

**Source**: `Perplexity/Prompt.txt`

```xml
<!-- Perplexity Core Structure -->
<goal>
  Mô tả mục tiêu ngắn gọn 1 dòng
  Primary objective statement
</goal>

<format_rules>
  Quy tắc định dạng output chi tiết
  - Markdown formatting rules
  - Section structure requirements
</format_rules>

<restrictions>
  - NEVER use [specific phrase/action]
  - AVOID [patterns to avoid]
  - NEVER reproduce [content type]
</restrictions>

<query_type>
  [ACADEMIC|RECENT_NEWS|CODING|TRANSLATION|CALCULATION|GENERAL]
  Phân loại query + xử lý đặc biệt theo type
</query_type>

<planning_rules>
  Hướng dẫn suy nghĩ trước khi hành động
  - [Rule 1]
  - [Rule 2]
</planning_rules>

<output>
  Mẫu output cuối cùng
  Expected response structure
</output>

<citations>
  [index]: https://url
  [index]: https://url
</citations>

<personalization>
  User preferences hoặc "None"
</personalization>
```

### 1.5 Lovable Custom Tags

**Source**: `Lovable/Agent Prompt.txt`

```xml
<!-- Lovable Agent Structure -->
<lov-identity>
  You are [name], an AI editor by Lovable Technologies.
  You are embedded inside the Lovable web editor.
  [Additional persona details]
</lov-identity>

<lov-context>
  [Current code block being worked on]
  [User's project context]
</lov-context>

<lov-task>
  [Task description]
  <type>[feature|fix|design|analyze]</type>
  <priority>[high|medium|low]</priority>
</lov-task>

<lov-constraints>
  <never_do>
    - NEVER read files in context
    - NEVER ask for confirmation
  </never_do>
  <do_instead>
    - Make informed decisions based on context
  </do_instead>
</lov-constraints>

<lov-output>
  <format>[markdown|code|design]</format>
  <include_preview>[yes|no]</include_preview>
</lov-output>
```

### 1.6 Warp.dev Section Patterns

**Source**: `Warp.dev/Prompt.txt`

```xml
<!-- Warp.dev Structure -->
<user_information>
  [User context, OS, workspace]
</user_information>

<constraints>
  IMPORTANT: [rule]
  NEVER: [prohibited action]
</constraints>

<citations>
  [1]: https://url
</citations>

<style>
  <tone>[formal|informal|technical]</tone>
  <format>[markdown|plain|code]</format>
</style>
```

### 1.7 Google/Gemini `<changes>` Structure (QUAN TRỌNG)

**Source**: `Google/Gemini/` — AI Studio vibe-coder.txt

```xml
<!-- Gemini AI Studio Most Structured Output Format -->

<!-- Root container for all changes -->
<changes>
  <change>
    <file>[full_path_of_file_1]</file>
    <description>[description of change]</description>
    <content><![CDATA[
      Full content of file_1
      (No escaping needed inside CDATA)
    ]]></content>
  </change>

  <change>
    <file>[full_path_of_file_2]</file>
    <description>[description of change]</description>
    <content><![CDATA[
      Full content of file_2
    ]]></content>
  </change>
</changes>

<!-- Special rules for Gemini <changes>: -->

<!-- Rule 1: metadata.json MUST be first file -->
<!-- If changes include metadata.json, put it FIRST in the list -->

<!-- Rule 2: CDATA escaping rules -->
<!-- - Outer backticks: NOT escaped -->
<!-- - Inner backticks: escaped as \` -->
<!-- - HTML entities: NOT needed inside CDATA -->
<!-- - Backslash: escaped as \\ -->

<!-- Rule 3: metadata.json structure -->
<!-- Must include: file operations, success indicators -->
```

#### Full Gemini Example

```xml
<changes>
  <change>
    <file>src/api/auth.ts</file>
    <description>Added JWT authentication endpoint with login/logout</description>
    <content><![CDATA[
      import { Request, Response } from 'express';
      import jwt from 'jsonwebtoken';

      const SECRET = process.env.JWT_SECRET || 'dev-secret';

      export const login = async (req: Request, res: Response) => {
        const { email, password } = req.body;
        // implementation
      };
    ]]></content>
  </change>

  <change>
    <file>src/middleware/auth.ts</file>
    <description>Added auth middleware for protected routes</description>
    <content><![CDATA[
      import { Request, Response, NextFunction } from 'express';
      import jwt from 'jsonwebtoken';

      export const authMiddleware = (
        req: Request,
        res: Response,
        next: NextFunction
      ) => {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) return res.status(401).json({ error: 'Unauthorized' });
        // verify token
      };
    ]]></content>
  </change>
</changes>
```

---

## 2. ${VAR} Dynamic Context Syntax

### 2.1 Claude Code Environment Variables

**Source**: `Anthropic/Claude Code 2.0.txt`

```bash
# Dynamic variable interpolation syntax
${Working directory}          # Thư mục làm việc hiện tại
${Current working directory}  # Tương đương
${Last 5 Recent commits}     # Git history
${Current branch}            # Git branch
${GIT_STATUS}               # Trạng thái git
${OS}                       # Hệ điều hành
${CURRENT_DATE}             # Ngày hiện tại
${USER_LANGUAGE}            # Ngôn ngữ người dùng (vi/en)
```

### 2.2 Template Interpolation Examples

```xml
<!-- Trong Claude Code prompt -->
<identity>
  Today is ${CURRENT_DATE}.
  You are working in ${Working directory}.
  Current branch: ${Current branch}.
</identity>

<!-- Trong Gemini <changes> structure -->
<context>
  <working_dir>${Working directory}</working_dir>
  <git_status>${GIT_STATUS}</git_status>
</context>
```

### 2.3 Perplexity Dynamic Context

**Source**: `Perplexity/Prompt.txt`

```xml
<context>
  <query_type>[INTERNATIONAL_NEWS|ACADEMIC|SUPPORT|...]</query_type>
  <user_location>${USER_LOCATION}</user_location>
  <current_date>${CURRENT_DATE}</current_date>
  <language>${USER_LANGUAGE}</language>
</context>
```

### 2.4 Lovable Context Injection

**Source**: `Lovable/Agent Prompt.txt`

```xml
<lov-context>
  <project>
    <name>[Project name]</name>
    <framework>[tech stack]</framework>
    <language>[programming language]</language>
  </project>
  <current_file>[file being edited]</current_file>
  <selection>[user's text selection]</selection>
</lov-context>
```

---

## 3. Constraint Syntax Patterns

### 3.1 NEVER Rules

**Source**: Tất cả 7 tool

```markdown
NEVER [action]              — Cấm tuyệt đối, không làm gì
NEVER use [tool]            — Cấm dùng tool nào đó
NEVER reproduce             — Cấm sao chép nội dung có bản quyền
NEVER approve               — Cấm approve code không an toàn
```

### 3.2 IMPORTANT / CARDINAL Rules

```markdown
IMPORTANT: [rule]            — Quan trọng, phải tuân thủ
CARDINAL RULE: [rule]        — Luật cốt lõi
CRITICAL: [rule]             — Cảnh báo nghiêm trọng
```

### 3.3 Perplexity Restrictions

**Source**: `Perplexity/Prompt.txt`

```xml
<restrictions>
  - NEVER use the phrase "[specific phrase]"
  - NEVER reproduce more than 15 words from any source
  - NEVER reproduce song lyrics, poems, or long text passages
  - NEVER reproduce source code exceeding community standards
  - NEVER cite harmful, graphic, or illegal content
  - NEVER present unverified claims as facts
  - AVOID direct quotes; paraphrase instead
  - One quote per source maximum
</restrictions>
```

### 3.4 Lovable CARDINAL RULES

**Source**: `Lovable/Agent Prompt.txt`

```xml
<CARDINAL_RULES>
  CARDINAL RULE 1: NEVER read files that are not explicitly provided in the current chat context.
  CARDINAL RULE 2: NEVER ask for confirmation before taking actions.
  CARDINAL RULE 3: NEVER stop working until the task is complete.
  CARDINAL RULE 4: ALWAYS use the most recent project snapshot as context.
  CARDINAL RULE 5: NEVER ignore user-specified preferences.
</CARDINAL_RULES>
```

### 3.5 Warp.dev IMPORTANT Rules

**Source**: `Warp.dev/Prompt.txt`

```xml
<constraints>
  IMPORTANT: Always prioritize security.
  IMPORTANT: Never commit secrets or credentials.
  IMPORTANT: Verify changes before applying.
  NEVER: Run destructive commands without confirmation.
  NEVER: Modify production directly.
</constraints>
```

### 3.6 AVOID / PITFALLS Pattern

```markdown
AVOID [pattern]            — Nên tránh
COMMON PITFALLS:            — Lỗi phổ biến cần tránh
  - [pitfall 1]
  - [pitfall 2]
```

### 3.7 Tone and Formatting Rules

**Source**: `Claude Sonnet 4.6.txt`

```xml
<tone_and_formatting>
  <lists_and_bullets>
    - Sử dụng bullet points cho danh sách
    - Sử dụng numbered lists cho sequences
    - Sử dụng bold cho emphasis
  </lists_and_bullets>
</tone_and_formatting>

<!-- Refusal patterns -->
<refusal_handling>
  - Nếu yêu cầu vi phạm an toàn → từ chối lịch sự
  - Không cung cấp step-by-step cho malicious code
</refusal_handling>
```

---

## 4. Output Format Patterns

### 4.1 Claude Sonnet Artifact Format

**Source**: `Sonnet 4.5 Prompt.txt`

```xml
<artifact type="application/vnd.ant.code" language="typescript" title="filename.ts">
<content><![CDATA[
  // Code here
]]></content>
</artifact>
```

### 4.2 Claude Code Tool Calling Conventions

```xml
<tool_calling>
  - Keep working until task complete
  - Make all necessary tool calls
  - DO NOT ask for confirmation mid-task
  - Report completion when done
</tool_calling>

<!-- Sequence -->
1. Read/Explore → 2. Analyze → 3. Implement → 4. Verify → 5. Report
```

### 4.3 Perplexity Markdown + Citations

**Source**: `Perplexity/Prompt.txt`

```markdown
## Summary
[2-3 sentence overview]

## Key Findings
[Main points as paragraphs]

## Sources
[1]: https://example.com
[2]: https://example2.com

<citations>
  [1]: https://example.com
  [2]: https://example2.com
</citations>
```

### 4.4 Lovable Custom Output

**Source**: `Lovable/Agent Prompt.txt`

```xml
<lov-response>
  <type>[code_change|feature_request|design|explanation]</type>
  <content>
    [Markdown or code content]
  </content>
  <preview>
    [Optional: rendered preview for design/UI]
  </preview>
  <files_changed>
    [List of files modified]
  </files_changed>
</lov-response>
```

---

## 5. Identity & Persona Patterns

### 5.1 Claude Code Identity

**Source**: `Claude Code 2.0.txt`

```xml
<identity>
  You are Claude Code, an AI assistant by Anthropic.
  You are capable of performing a wide range of tasks.
  Today is ${CURRENT_DATE}.
</identity>

<communication_style>
  - Use concise language
  - Be direct and action-oriented
  - Ask clarifying questions when needed
</communication_style>
```

### 5.2 Replit Identity

**Source**: `Replit/Prompt.txt`

```xml
<identity>
  You are a helpful coding assistant embedded inside the Replit IDE.
  You have access to the user's workspace, files, and running processes.
  You speak [USER_LANGUAGE] based on user context.
</identity>

<capabilities>
  <capability type="file_editing">Full file read/write</capability>
  <capability type="shell">Terminal command execution</capability>
  <capability type="deployment">Deploy to Replit infrastructure</capability>
</capabilities>
```

### 5.3 Perplexity Identity

**Source**: `Perplexity/Prompt.txt`

```xml
<identity>
  You are an AI assistant by Perplexity.
  You are a search expert.
  You are truthful, accurate, and helpful.
  You cite sources for all factual claims.
  You speak in the user's language.
</identity>
```

---

## 6. Best Practices Summary

### 6.1 Required Tags (Claude Code)

| Tag | Bắt buộc? | Mô tả |
|-----|---------|-------|
| `<goal>` | ✅ | Mục tiêu chính — 1-3 dòng |
| `<constraints>` | ✅ | Rules, giới hạn, NEVER/IMPORTANT |
| `<context>` | Tùy | Thông tin môi trường, codebase |
| `<output_format>` | Tùy | Format trả về mong đợi |
| `<identity>` | Tùy | Persona, ngôn ngữ |
| `${VAR}` | Tùy | Dynamic context |

### 6.2 Recommended Structure Order

```
1. <goal>              — Mục tiêu (đầu tiên, bắt buộc)
2. <identity>          — Persona (nếu cần)
3. <context>           — Context (nếu có)
4. <constraints>       — Rules (nếu có)
5. <workflow>          — Steps (nếu phức tạp)
6. <output_format>     — Output (nếu cần format cụ thể)
```

### 6.3 CDATA Escaping Priority Rules (Gemini)

**Source**: `Google/Gemini/AI Studio vibe-coder.txt`

```
### Priority 1: File Content (Inner)
When placing content inside CDATA blocks:
- Escape backticks: \`
- Escape backslashes: \\

### Priority 2: Surrounding Structure (Outer)
The structure OUTSIDE CDATA:
- Use regular characters
- DO NOT escape backticks outside CDATA

### Priority 3: Nested Structures
For JSON inside XML inside CDATA:
- Escape quotes at the CDATA boundary
- Escape at the JSON/XML boundary
```

### 6.4 Universal Constraint Keywords

```markdown
# Priority Order (highest to lowest)
CARDINAL RULE:   — Luật cốt lõi, không thể vi phạm
NEVER:           — Cấm tuyệt đối
IMPORTANT:       — Quan trọng, phải tuân thủ
AVOID:           — Nên tránh
PREFER:          — Ưu tiên
```

### 6.5 Anti-Patterns (Tránh)

| ❌ Anti-pattern | ✅ Correct |
|---------------|-----------|
| Prompt dài không cấu trúc | XML tags rõ ràng |
| Không có `<goal>` | Bắt buộc có `<goal>` |
| Hardcode path thay vì `${VAR}` | Dùng `${VAR}` |
| Không có constraints | Thêm `<constraints>` |
| Không có output format | Thêm `<output_format>` |
| Gemini: Quên CDATA wrapper | Dùng `<content><![CDATA[...]]>` |
| Gemini: metadata.json không first | Luôn đặt metadata.json đầu tiên |
| Perplexity: Không cite source | Luôn dùng `<citations>` |
