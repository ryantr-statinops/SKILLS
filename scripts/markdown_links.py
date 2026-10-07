"""Extract rendered Markdown link destinations without treating code as links."""

from __future__ import annotations

import re

REFERENCE_DEFINITION_RE = re.compile(
    r"^[ ]{0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]*)>|([^\s]+))",
    re.MULTILINE,
)


def _masked(value: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in value)


def _mask_inline_code(line: str) -> str:
    chars = list(line)
    index = 0
    while index < len(line):
        if line[index] != "`" or (index > 0 and line[index - 1] == "\\"):
            index += 1
            continue
        end = index
        while end < len(line) and line[end] == "`":
            end += 1
        delimiter = line[index:end]
        close = line.find(delimiter, end)
        if close < 0:
            index = end
            continue
        finish = close + len(delimiter)
        for position in range(index, finish):
            if chars[position] != "\n":
                chars[position] = " "
        index = finish
    return "".join(chars)


def _mask_code(text: str) -> str:
    output = []
    fence_char: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        stripped = content.lstrip(" ")
        indent = len(content) - len(stripped)
        if fence_char is not None:
            marker_length = len(stripped) - len(stripped.lstrip(fence_char))
            if indent <= 3 and marker_length >= fence_length and not stripped[marker_length:].strip():
                fence_char = None
                fence_length = 0
            output.append(_masked(line))
            continue
        marker = stripped[:1]
        marker_length = len(stripped) - len(stripped.lstrip(marker)) if marker in {"`", "~"} else 0
        if indent <= 3 and marker in {"`", "~"} and marker_length >= 3:
            fence_char = marker
            fence_length = marker_length
            output.append(_masked(line))
            continue
        output.append(_mask_inline_code(line))
    return "".join(output)


def _escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _closing_bracket(text: str, start: int) -> int | None:
    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def _inline_destination(text: str, start: int) -> tuple[str, int] | None:
    index = start + 1
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text):
        return None
    if text[index] == "<":
        close = text.find(">", index + 1)
        if close < 0:
            return None
        target = text[index + 1:close]
        index = close + 1
    else:
        target_chars = []
        paren_depth = 0
        while index < len(text):
            char = text[index]
            if char == "\\" and index + 1 < len(text):
                target_chars.append(text[index + 1])
                index += 2
                continue
            if char.isspace() and paren_depth == 0:
                break
            if char == "(":
                paren_depth += 1
            elif char == ")":
                if paren_depth == 0:
                    break
                paren_depth -= 1
            target_chars.append(char)
            index += 1
        target = "".join(target_chars)
    if not target:
        return None
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text):
        return None
    if text[index] == ")":
        return target, index + 1

    quote: str | None = None
    paren_depth = 0
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if quote is not None:
            if char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            if paren_depth == 0:
                return target, index + 1
            paren_depth -= 1
        index += 1
    return None


def extract_markdown_link_targets(text: str) -> list[str]:
    """Return inline and reference-definition destinations outside code spans."""
    visible = _mask_code(text)
    targets = []
    for match in REFERENCE_DEFINITION_RE.finditer(visible):
        targets.append(match.group(1) if match.group(1) is not None else match.group(2))
        start, end = match.span()
        visible = visible[:start] + _masked(visible[start:end]) + visible[end:]

    index = 0
    while index < len(visible):
        if visible[index] != "[" or _escaped(visible, index):
            index += 1
            continue
        label_end = _closing_bracket(visible, index)
        if label_end is None or label_end + 1 >= len(visible) or visible[label_end + 1] != "(":
            index = (label_end + 1) if label_end is not None else index + 1
            continue
        parsed = _inline_destination(visible, label_end + 1)
        if parsed is None:
            index = label_end + 1
            continue
        target, index = parsed
        targets.append(target)
    return targets
