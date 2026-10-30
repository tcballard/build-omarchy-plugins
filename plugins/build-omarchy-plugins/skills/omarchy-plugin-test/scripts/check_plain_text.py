#!/usr/bin/env python3
"""Opt-in lexical QML text policy; not a QML parser or data-flow analysis."""

import argparse
import re
import sys
from pathlib import Path


TEXT_TYPES = {"Text", "Label", "TextEdit", "TextArea"}
TOKEN = re.compile(
    r"(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)"
    r"|(?P<string>\"(?:\\[\s\S]|[^\"\\])*\"|'(?:\\[\s\S]|[^'\\])*'|`(?:\\[\s\S]|[^`\\])*`)"
    r"|(?P<word>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)|(?P<newline>\n)|(?P<other>[^\s])"
)


def scan(source):
    tokens = []
    line = 1
    for match in TOKEN.finditer(source):
        if match.lastgroup != "comment":
            value = "STRING" if match.lastgroup == "string" else match.group()
            if value in {"'", '"', "`"}:
                raise ValueError("Unterminated string")
            tokens.append((value, line))
        line += match.group().count("\n")
    pairs, parents, stack = {}, {}, []
    for index, (value, _) in enumerate(tokens):
        if value == "{":
            parents[index] = stack[-1] if stack else None
            stack.append(index)
        elif value == "}":
            if not stack:
                raise ValueError("Unbalanced braces")
            pairs[stack.pop()] = index
    if stack:
        raise ValueError("Unbalanced braces")

    def direct(start):
        result, index = [], start + 1
        while index < pairs[start]:
            if index in pairs:
                result.append(("OBJECT", tokens[index][1]))
                index = pairs[index] + 1
            else:
                result.append(tokens[index])
                index += 1
        return result

    def bindings(items, name):
        result = []
        for index, (value, _) in enumerate(items):
            if value != name:
                continue
            tail = [token for token, _ in items[index + 1:] if token != "\n"]
            if len(tail) >= 2 and tail[0] == ":":
                result.append(tail[1])
        return result

    def plain(items):
        for index, (value, _) in enumerate(items):
            if value != "textFormat":
                continue
            tail = items[index + 1:]
            while tail and tail[0][0] == "\n":
                tail = tail[1:]
            if not tail or tail[0][0] != ":":
                return False
            tail = tail[1:]
            while tail and tail[0][0] == "\n":
                tail = tail[1:]
            if not tail or not re.fullmatch(r"(?:\w+\.)?(?:Text|TextEdit)\.PlainText", tail[0][0]):
                return False
            return len(tail) == 1 or tail[1][0] in {";", "\n"}
        return False

    problems = []
    for start, end in sorted(pairs.items()):
        previous = start - 1
        while previous >= 0 and tokens[previous][0] == "\n":
            previous -= 1
        kind = tokens[previous][0].split(".")[-1] if previous >= 0 else ""
        items = direct(start)
        ids = bindings(items, "id")
        object_id = ids[0] if len(ids) == 1 else ""
        reasons = []
        if kind in TEXT_TYPES and not plain(items):
            reasons.append(f"{kind} needs an explicit literal PlainText format")
        if kind == "ToolTip":
            content = None
            for child in pairs:
                if parents[child] == start and child >= 3:
                    prefix = [t for t, _ in tokens[start + 1:child] if t != "\n"]
                    if prefix[-3:-1] == ["contentItem", ":"]:
                        content = child
                        break
            child_type = ""
            if content is not None:
                child_type = next(t for t, _ in reversed(tokens[:content]) if t != "\n").split(".")[-1]
            if child_type not in TEXT_TYPES or not plain(direct(content)):
                reasons.append("ToolTip needs a plain-text contentItem")
        if any(re.fullmatch(r"(?:\w+\.)?ToolTip\.(?:text|show)", value) for value, _ in items):
            reasons.append("Attached ToolTip text/show needs an explicit plain-text ToolTip")
        if reasons:
            problems.append((tokens[start][1], object_id, "; ".join(reasons)))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--allow-rich-text", action="append", default=[], metavar="FILE:ID=REASON")
    args = parser.parse_args()
    root = args.source.absolute()
    base = root if root.is_dir() else root.parent
    allowances = {}
    for entry in args.allow_rich_text:
        key, separator, reason = entry.partition("=")
        file, colon, identifier = key.rpartition(":")
        if not separator or not reason.strip() or not colon or not re.fullmatch(r"[a-z_]\w*", identifier) or key in allowances:
            parser.error("Use a unique FILE:ID=REASON for each reviewed rich-text object")
        if Path(file).is_absolute() or ".." in Path(file).parts or "\\" in file:
            parser.error("Exception paths must be relative to the checked directory")
        allowances[key] = reason.strip()
    errors, used = [], set()
    entries = sorted(root.rglob("*")) if root.is_dir() else [root]
    files = []
    for entry in entries:
        if ".git" in entry.relative_to(base).parts:
            continue
        if entry.is_symlink():
            errors.append(f"{entry.relative_to(base)}: Symlinks are not checked")
        elif entry.suffix == ".qml":
            files.append(entry)
    for file in files:
        relative = file.relative_to(base).as_posix()
        if ".git" in file.relative_to(base).parts:
            continue
        try:
            if base.is_symlink():
                raise ValueError("Symlinks are not checked")
            if not file.is_file():
                raise ValueError("Expected a regular QML file")
            with file.open("rb") as stream:
                data = stream.read(2 * 1024 * 1024 + 1)
            if len(data) > 2 * 1024 * 1024:
                raise ValueError("QML exceeds the 2 MiB scan limit")
            for line, identifier, reason in scan(data.decode("utf-8")):
                key = f"{relative}:{identifier}"
                if identifier and key in allowances:
                    if key in used:
                        errors.append(f"Ambiguous exception: {key}")
                    used.add(key)
                    print(f"REVIEWED {key}: {allowances[key]}")
                else:
                    errors.append(f"{relative}:{line}: {reason}")
        except (OSError, ValueError) as error:
            errors.append(f"{relative}: {error}")
    errors.extend(f"Unused exception: {key}" for key in allowances.keys() - used)
    if not files:
        errors.append("No QML files found")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    if not errors:
        print("Plain-text policy passed; custom controls, dynamic assignments and runtime rendering still need review.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
