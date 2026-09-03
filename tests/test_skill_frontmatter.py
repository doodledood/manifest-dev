"""Frontmatter every strict-YAML CLI surface can read, not only Claude Code.

Claude Code reads skill frontmatter leniently; Pi parses it with a real YAML parser
and drops the skill when it does not parse. A malformed value therefore passes
unnoticed in the source plugin and then fails in every distribution copying it — a
skill leaves a startup warning behind, a prompt template leaves nothing at all.

The rules here are the shape a one-line top-level mapping must have, not a full
parse (no YAML library is available: the suite is standard-library only, since the
project declares no dependencies). Do not "fix" that by adding one: PyYAML and
js-yaml both *accept* the wrapped value that broke Pi, so a lenient parser here
would retire the guard while looking more rigorous than it is. The oracle these
rules were checked against is the `yaml` package Pi itself bundles. They cover the ways a `description` has actually
broken or can plausibly break: a value wrapped over several physical lines, a quote
that closes early or never, and a plain value carrying `: `, which YAML reads as
structure rather than text, or ` #`, which it reads as a comment and truncates at.
`frontmatter_problems` takes text rather than a path so these rules can be
exercised on known-bad input below.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
# Every tree a strict-YAML CLI reads frontmatter from, with the files it reads
# there. Pi loads its prompt templates through the same parser as its skills
# (package.json declares both), and their argument-hint lines are the longest values
# in those files — the shape most likely to be hard-wrapped there. A malformed
# template is dropped with no diagnostic at all, unlike a skill.
PARSED_ROOTS = (
    ("claude-plugins", "SKILL.md"),
    ("dist", "SKILL.md"),
    (".claude/skills", "SKILL.md"),
    ("dist/pi/prompts", "*.md"),
)
SKILL_ROOTS = tuple(root for root, pattern in PARSED_ROOTS if pattern == "SKILL.md")
# Local CLI installs and worktrees, per .gitignore's own list: real files on disk,
# shipped by nothing, and absent from a fresh checkout.
LOCAL_INSTALLS = {
    "worktrees",
    ".gemini",
    ".codex",
    ".opencode",
    "node_modules",
    ".venv",
}
KEY_LINE = re.compile(r"^([A-Za-z][\w.-]*):(?=[ \t]|$)[ \t]*(.*)$")
# The frontmatter vocabulary. An unrecognised key at column 0 is nearly always a
# wrapped value's continuation line that happens to contain a colon, which would
# otherwise read as a new entry and leave the value silently truncated.
KNOWN_KEYS = frozenset(
    {"name", "description", "user-invocable", "argument-hint", "metadata"}
)
# Shapes for the keys that have one. A wrapped value landing on a line that opens
# with a vocabulary word is read as a new entry, and these catch what the
# vocabulary alone cannot: the fragment does not look like the key's real value.
KEY_VALUE_SHAPES = {
    "name": re.compile(r"^[a-z0-9-]+$"),
    "user-invocable": re.compile(r"^(true|false)$"),
}
# Keys holding free prose. A '#' in prose cannot be told apart from a description
# cut short at it, so these must be quoted; elsewhere a trailing comment is normal.
PROSE_KEYS = frozenset({"description", "argument-hint"})
# Unquoted, these are a null, a boolean, or a number to YAML rather than text, and
# a loader expecting a string drops the skill or throws on it.
NOT_TEXT = re.compile(
    r"^(~|[Nn]ull|NULL|[Tt]rue|TRUE|[Ff]alse|FALSE|[-+.\d][\d.eE+-]*)$"
)
# What YAML lets follow a backslash inside a double-quoted scalar.
ESCAPES = set('0abtnvfre "/\\N_LP\tx\nuU')
# A plain value opening with one of these is read as structure, not text.
INDICATORS = "[]{},&*!%@`?"
# A block scalar is different: it is legal YAML and reads as the text written, but
# it spans several physical lines, which the convention forbids. Exempting it left
# its continuation lines unchecked, so it is refused rather than exempted.
BLOCK_SCALAR = "|>"
TRAILING_COMMENT = re.compile(r"[ \t]+#.*$")
NESTED_KEY = "metadata"
QUOTES = ("'", '"')
# YAML starts a comment only after a space or a tab — narrower than str.isspace(),
# which would accept a non-breaking space, and wider than a bare " #" test, which
# would miss a tab. Both mistakes let a truncated or unparseable value through.
COMMENT_SEPARATORS = (" ", "\t")
UNQUOTED_COMMENT = re.compile(r"[ \t]#")
COLON_SEPARATOR = re.compile(r":[ \t]")


def parsed_files(root: str, pattern: str) -> list[Path]:
    """Every real frontmatter file under one root.

    `rglob` does not descend into symlinked directories, so the linked entries in
    `.agents/skills/` and most of `.claude/skills/` are not walked twice: they
    resolve onto a directory another root already covers — `claude-plugins/` for
    plugin skills, `.claude/skills/` itself for the repo-local ones.
    """
    return sorted((ROOT / root).rglob(pattern))


def quoted_scalar(value: str) -> tuple[int | None, str | None]:
    """Walk a quoted scalar once.

    Returns the index just past its closing quote (None when it never closes) and
    any escape YAML does not define. One walk serves both questions: a second
    scanner over the same text disagreed with this one about `\\\\` pairs and about
    where the value stops.
    """
    quote = value[0]
    index = 1
    while index < len(value):
        char = value[index]
        if quote == '"' and char == "\\":
            escape = value[index + 1 : index + 2]
            if not escape:
                return None, None
            if escape not in ESCAPES:
                return None, escape
            index += 2
            continue
        if char == quote:
            if quote == "'" and value[index + 1 : index + 2] == "'":
                index += 2
                continue
            return index + 1, None
        index += 1
    return None, None


def scalar_text(value: str) -> str:
    """The value YAML would read: comment removed, one pair of quotes stripped."""
    bare = TRAILING_COMMENT.sub("", value).strip()
    if bare.startswith("#"):
        return ""
    if len(bare) > 1 and bare[0] in QUOTES and bare[-1] == bare[0]:
        return bare[1:-1].strip()
    return bare


def value_problem(key: str, value: str) -> str | None:
    """Describe how this value breaks its own line, or None when it is readable.

    A key with a declared shape may carry a trailing comment: YAML strips it and the
    shape check then sees the real value. For free prose there is no such check, so
    a `#` is indistinguishable from a description silently cut short at it.
    """
    if not value or value.startswith("#"):
        return None

    if value[0] in QUOTES:
        end, undefined_escape = quoted_scalar(value)
        if undefined_escape is not None:
            return (
                f"value for {key!r} contains the escape '\\{undefined_escape}', "
                "which YAML does not define; single-quote the value instead"
            )
        if end is None:
            return (
                f"value for {key!r} opens with {value[0]} and does not close it on "
                "this line; keep the whole value on one physical line"
            )
        rest = value[end:]
        if not rest.strip():
            return None
        if rest.strip().startswith("#"):
            if rest[:1] in COMMENT_SEPARATORS:
                return None
            return (
                f"value for {key!r} is followed by {rest.strip()!r} with no space "
                "or tab before the '#'; YAML reads '#' as a comment only after one"
            )
        return (
            f"value for {key!r} closes its quote early, leaving {rest.strip()!r} "
            "outside the value; an apostrophe inside a single-quoted value has "
            "to be doubled ('') to be part of the text"
        )

    if value[0] in BLOCK_SCALAR:
        return (
            f"value for {key!r} uses a block scalar, which is valid YAML but spans "
            "several physical lines; put the whole value on one physical line"
        )
    if value[0] in INDICATORS or value.startswith("- "):
        return (
            f"unquoted value for {key!r} opens with {value[0]!r}, which YAML reads "
            "as structure rather than text; wrap the value in single quotes"
        )
    if key in PROSE_KEYS and UNQUOTED_COMMENT.search(value):
        return (
            f"unquoted value for {key!r} contains ' #', which YAML reads as a "
            "comment and silently truncates; wrap the value in single quotes"
        )
    bare = scalar_text(value)
    if COLON_SEPARATOR.search(bare) or bare.endswith(":"):
        return (
            f"unquoted value for {key!r} contains ': ', which YAML reads as a "
            "nested mapping rather than text; wrap the value in single quotes"
        )
    return None


def frontmatter_block(text: str) -> list[str] | None:
    """The lines between the delimiters, or None when the file has no frontmatter.

    Every check reads the block through here, so nothing forms a second opinion
    about where the frontmatter ends and the body begins.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    closing = next(
        (
            offset
            for offset, line in enumerate(lines)
            if offset and line.strip() == "---"
        ),
        None,
    )
    return None if closing is None else lines[1:closing]


def declared_description(text: str) -> str:
    """The description YAML reads from this file's frontmatter, or '' when unusable.

    Read from the block only: a `description:` line in the body is documentation
    a reader can see and the CLI never parses.
    """
    for line in frontmatter_block(text) or []:
        if line.startswith("description:"):
            written = line[len("description:") :]
            value = scalar_text(written)
            unquoted = TRAILING_COMMENT.sub("", written).strip()[:1] not in QUOTES
            return "" if unquoted and NOT_TEXT.match(value) else value
    return ""


def frontmatter_problems(text: str, where: str) -> list[str]:
    """Describe the ways this frontmatter breaks the one-line mapping shape."""
    block = frontmatter_block(text)
    if block is None:
        lines = text.split("\n")
        if not lines or lines[0].strip() != "---":
            return [f"{where}:1: file does not open with a --- frontmatter delimiter"]
        return [f"{where}:1: frontmatter is never closed by a --- line"]

    problems: list[str] = []
    seen_keys: set[str] = set()
    opened = ""
    nested_indent = 0
    for offset, line in enumerate(block):
        lineno = offset + 2
        if "\t" in line[: len(line) - len(line.lstrip(" \t"))]:
            problems.append(f"{lineno}: YAML forbids tab indentation: {line!r}")
            continue
        # Only a space or a tab is whitespace to YAML; str.strip() would discard a
        # line made of a non-breaking space, which YAML reads as a second key.
        if not line.strip(" \t") or line.lstrip(" \t").startswith("#"):
            continue

        # Only a space indents in YAML: a non-breaking space reads as text, which
        # turns a continuation line into a second implicit key and drops the skill.
        if line[0] == " ":
            if opened == NESTED_KEY:
                indent = len(line) - len(line.lstrip(" "))
                if nested_indent and indent != nested_indent:
                    problems.append(
                        f"{lineno}: this entry is indented {indent} spaces and the "
                        f"one above it {nested_indent}; YAML needs every entry of a "
                        "mapping at the same column"
                    )
                    continue
                nested_indent = indent
                nested = KEY_LINE.match(line.lstrip(" "))
                if nested is None:
                    problems.append(f"{lineno}: {line!r} is not a mapping entry")
                    continue
                problem = value_problem(nested.group(1), nested.group(2).strip())
                if problem is not None:
                    problems.append(f"{lineno}: {problem}")
                continue
            problems.append(
                f"{lineno}: {line!r} continues the previous value onto a second "
                "line; keep the whole value on one physical line, however long"
            )
            continue

        entry = KEY_LINE.match(line)
        if entry is None:
            problems.append(
                f"{lineno}: {line!r} is neither a 'key: value' entry nor an "
                "indented continuation, so the mapping does not parse; a value "
                "wrapped over several lines is the usual cause"
            )
            continue

        key, value = entry.group(1), entry.group(2).strip()
        if key not in KNOWN_KEYS:
            problems.append(
                f"{lineno}: {key!r} is not a frontmatter key "
                f"({', '.join(sorted(KNOWN_KEYS))}); a value wrapped onto this line "
                "is the usual cause, so keep the whole value on one physical line"
            )
            continue
        shape = KEY_VALUE_SHAPES.get(key)
        if shape is not None and not shape.match(scalar_text(value)):
            problems.append(
                f"{lineno}: {value!r} is not the shape {key!r} takes; a value "
                "wrapped onto this line is the usual cause"
            )
            continue
        # Only metadata opens a nested block, and only with no inline value of its
        # own — quotes included, since '' is a string to YAML and closes the block.
        inline = TRAILING_COMMENT.sub("", value).strip()
        if inline.startswith("#"):
            inline = ""
        if key == NESTED_KEY and inline:
            problems.append(
                f"{lineno}: {key!r} carries the inline value {inline!r}, so the "
                "indented entries below it are not part of any mapping"
            )
            continue
        opened = NESTED_KEY if key == NESTED_KEY else ""
        nested_indent = 0
        if key in seen_keys:
            problems.append(f"{lineno}: duplicate key {key!r}")
        seen_keys.add(key)

        problem = value_problem(key, value)
        if problem is not None:
            problems.append(f"{lineno}: {problem}")

    return [f"{where}:{problem}" for problem in problems]


def test_every_shipped_frontmatter_parses() -> None:
    problems: list[str] = []
    for root, pattern in PARSED_ROOTS:
        for path in parsed_files(root, pattern):
            problems.extend(
                frontmatter_problems(
                    path.read_text(encoding="utf-8"),
                    str(path.relative_to(ROOT)),
                )
            )
    assert not problems, "unreadable frontmatter:\n" + "\n".join(problems)


def test_every_shipped_skill_declares_a_usable_description() -> None:
    """A description that parses to nothing drops the skill as surely as a syntax error."""
    missing = []
    for root, pattern in PARSED_ROOTS:
        for path in parsed_files(root, pattern):
            if not declared_description(path.read_text(encoding="utf-8")):
                missing.append(str(path.relative_to(ROOT)))
    assert not missing, (
        f"SKILL.md files with no usable description: {missing}; the CLIs drop a "
        "skill whose description is absent, empty, or only a comment"
    )


def test_a_description_in_the_body_is_not_read_as_frontmatter() -> None:
    body_only = "---\nname: x\n---\n\ndescription: 'documentation, not frontmatter'\n"
    assert not declared_description(body_only)
    assert declared_description("---\ndescription: 'real'\n---\n") == "real"
    assert not declared_description("---\ndescription: # todo: write one\n---\n")
    assert not declared_description("---\ndescription: '   '\n---\n")
    assert not declared_description("---\ndescription: null\n---\n")
    assert not declared_description("---\ndescription: 123\n---\n")
    assert declared_description("---\ndescription: '123 ways to fix it'\n---\n")


def test_every_parsed_root_contributes_files() -> None:
    empty = [root for root, pattern in PARSED_ROOTS if not parsed_files(root, pattern)]
    assert (
        not empty
    ), f"found no frontmatter files under {empty}; the walk covers nothing"


def walked_files() -> set[Path]:
    return {
        path for root, pattern in PARSED_ROOTS for path in parsed_files(root, pattern)
    }


def test_the_walk_reaches_every_skill_in_the_repository() -> None:
    """Derive the expected set, so narrowing the root list cannot go unnoticed."""
    everywhere = {
        path for path in ROOT.rglob("SKILL.md") if not LOCAL_INSTALLS & set(path.parts)
    }
    unreached = everywhere - walked_files()
    assert not unreached, (
        f"SKILL.md files no root reaches: {sorted(unreached)}; add the tree "
        "to PARSED_ROOTS or the guard silently stops covering it"
    )


def test_the_walk_reaches_every_surface_the_pi_package_ships() -> None:
    """package.json names the directories Pi loads; each one parses through this guard.

    Pi reads prompt-template frontmatter with the same parser as skills, so a
    directory declared there and absent from PARSED_ROOTS is an unguarded surface.
    """
    declared = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["pi"]
    shipped = {
        path
        for key in ("skills", "prompts")
        for directory in declared.get(key, [])
        for path in (ROOT / directory).rglob("*.md")
        if path.read_text(encoding="utf-8").startswith("---")
    }
    unreached = shipped - walked_files()
    assert not unreached, (
        f"frontmatter the Pi package ships and this guard never reads: "
        f"{sorted(unreached)}"
    )


# Frontmatter no CLI gets as written, in three kinds: shapes a strict YAML parser
# refuses outright; shapes it accepts while reading something other than the text
# written (' #' and an indented continuation carrying one truncate at the comment;
# a wrap onto a line that reads as a key truncates at the wrap); and shapes it
# accepts intact but which span several physical lines — an indented continuation, a
# block scalar — which the convention forbids.
MISREAD = {
    "wrapped quoted value": (
        "---\n"
        "name: x\n"
        "description: 'opens here\n"
        "and wraps to column zero'\n"
        "---\n",
        "does not close it",
    ),
    "quote that only opens": (
        "---\n" "description: 'opens only\n" "---\n",
        "does not close it",
    ),
    "apostrophe in a single-quoted value": (
        "---\n" "description: 'the user's manifest'\n" "---\n",
        "closes its quote early",
    ),
    "undefined escape in a double-quoted value": (
        "---\n" 'description: "flags a bare \\d+ pattern"\n' "---\n",
        "which YAML does not define",
    ),
    "comment jammed against a closing quote": (
        "---\n" "description: 'a value'# note\n" "---\n",
        "no space or tab before",
    ),
    "non-breaking space before a comment": (
        "---\n" "description: 'a value'\xa0# note\n" "---\n",
        "no space or tab before",
    ),
    "': ' in an unquoted value": (
        "---\n" "description: Goal-based chain: does things\n" "---\n",
        "nested mapping",
    ),
    "colon followed by a tab": (
        "---\n" "description: chain:\tdoes things\n" "---\n",
        "nested mapping",
    ),
    "unquoted value ending in a colon": (
        "---\n" "description: things:\n" "---\n",
        "nested mapping",
    ),
    "colon inside a nested entry": (
        "---\n" "name: x\n" "metadata:\n" "  name: Widget: v2\n" "---\n",
        "nested mapping",
    ),
    "' #' in an unquoted value": (
        "---\n" "description: does things # sometimes\n" "---\n",
        "silently truncates",
    ),
    "tab before a comment in an unquoted value": (
        "---\n" "description: a value\t# note\n" "---\n",
        "silently truncates",
    ),
    "plain value opening with a bracket": (
        "---\n" "description: [DEPRECATED] runs the old path\n" "---\n",
        "reads as structure",
    ),
    "plain value opening with a dash": (
        "---\n" "description: - runs the old path\n" "---\n",
        "reads as structure",
    ),
    "block scalar spanning several lines": (
        "---\n" "description: |\n" "  a longer value\n" "---\n",
        "spans several physical lines",
    ),
    "block scalar with nothing after it": (
        "---\n" "name: x\n" "description: |\n" "---\n",
        "spans several physical lines",
    ),
    "unquoted value wrapped onto a second line": (
        "---\n" "description: starts here\n" "and continues\n" "---\n",
        "neither a 'key: value' entry",
    ),
    "key with no space after the colon": (
        "---\n" "name: x\n" "description:does things\n" "---\n",
        "neither a 'key: value' entry",
    ),
    "non-breaking space used as indentation": (
        "---\n" "description: pursues it\n" "\xa0and continues\n" "---\n",
        "neither a 'key: value' entry",
    ),
    "line of non-breaking space": (
        "---\n"
        "name: x\n"
        "description: 'd'\n"
        "\xa0\n"
        "user-invocable: true\n"
        "---\n",
        "neither a 'key: value' entry",
    ),
    # Indented on purpose: it pins that a later key closes the metadata block. Read
    # as a nested entry instead, this line looks like a legitimate mapping entry.
    "wrapped description after a nested block": (
        "---\n"
        "name: x\n"
        "metadata:\n"
        "  internal: true\n"
        "description: pursues it with full\n"
        "  autonomy: reach a state\n"
        "---\n",
        "continues the previous value",
    ),
    "wrapped value whose second line reads as a key": (
        "---\n"
        "description: pursues it with full\n"
        "autonomy: reach a state where every criterion holds\n"
        "---\n",
        "is not a frontmatter key",
    ),
    "wrapped value landing on the name key": (
        "---\n"
        "name: x\n"
        "description: writes the file's\n"
        "name: size and mtime\n"
        "---\n",
        "is not the shape",
    ),
    "sequence under a nested block": (
        "---\n" "name: x\n" "metadata:\n" "  - internal\n" "---\n",
        "is not a mapping entry",
    ),
    "wrapped value landing on a key that has a shape": (
        "---\n"
        "name: x\n"
        "description: pursues it with full\n"
        "user-invocable: reach a state where every criterion holds\n"
        "---\n",
        "is not the shape",
    ),
    "unquoted value wrapped onto an indented line": (
        "---\n"
        "description: pursues it with full\n"
        "  autonomy: reach a state where every criterion holds\n"
        "---\n",
        "continues the previous value",
    ),
    "indented continuation carrying a comment": (
        "---\n" "description: reads a manifest\n" "  and then # stops here\n" "---\n",
        "continues the previous value",
    ),
    "plain indented continuation": (
        "---\n" "description: reads a manifest\n" "  and pursues it\n" "---\n",
        "continues the previous value",
    ),
    "empty value opening an indented block": (
        "---\n" "name: x\n" "description:\n" "  autonomy: reach a state\n" "---\n",
        "continues the previous value",
    ),
    "metadata carrying an inline value": (
        "---\n" "name: x\n" "metadata: ''\n" "  internal: true\n" "---\n",
        "carries the inline value",
    ),
    "metadata carrying an inline boolean": (
        "---\n" "name: x\n" "metadata: true\n" "  internal: true\n" "---\n",
        "carries the inline value",
    ),
    "wrapped line opening with a vocabulary word": (
        "---\n"
        "name: x\n"
        "description: reads the file's\n"
        "metadata: name, size, and mtime\n"
        "---\n",
        "carries the inline value",
    ),
    "tab indentation": (
        "---\n" "metadata:\n" "\tinternal: true\n" "---\n",
        "tab indentation",
    ),
    "tab inside the indentation run": (
        "---\n" "metadata:\n" "  \tinternal: true\n" "---\n",
        "tab indentation",
    ),
    "nested entries at different columns": (
        "---\n" "metadata:\n" "  internal: true\n" "    extra: 1\n" "---\n",
        "same column",
    ),
    "duplicate key": (
        "---\n" "name: x\n" "name: y\n" "---\n",
        "duplicate key",
    ),
    "no frontmatter": (
        "# just a heading\n",
        "does not open with a ---",
    ),
    "frontmatter never closed": (
        "---\n" "name: x\n",
        "never closed",
    ),
}

READ_AS_WRITTEN = {
    "quoted one-liner": "---\nname: x\ndescription: 'Goal-based chain: does "
    "things.'\n---\n",
    "plain scalar with an apostrophe": "---\ndescription: the user's "
    "manifest\n---\n",
    "doubled apostrophe inside quotes": "---\ndescription: 'the user''s "
    "manifest'\n---\n",
    "trailing comment after a quoted value": "---\ndescription: 'a value'  # note"
    "\n---\n",
    "escaped quotes inside a double-quoted value": '---\ndescription: "say \\"hi'
    '\\" now"\n---\n',
    "comment line inside frontmatter": "---\n# why this exists\nname: x\n---\n",
    "key whose whole value is a comment": "---\ndescription: # todo: write one\n"
    "name: x\n---\n",
    "trailing whitespace on either delimiter": "--- \nname: x\n--- \n",
    "tab before a comment after a quoted value": "---\ndescription: 'a value'\t# "
    "note\n---\n",
    "nested mapping": "---\nname: x\nmetadata:\n  internal: true\n---\n",
    "colon with no space in a plain value": "---\nname: x\ndescription: runs "
    "at 10:30 daily\n---\n",
    "comment on the key that opens a nested block": "---\nname: x\nmetadata:  "
    "# internal marker\n  internal: true\n---\n",
    "literal backslash in a double-quoted value": '---\ndescription: "flags a '
    'bare \\\\d+ pattern"\n---\n',
    "backslash inside a trailing comment": '---\ndescription: "a value"  # '
    "matches \\d+\n---\n",
    # Verbatim from the frontmatter template in CLAUDE.md, comments included — the
    # comment on the name line itself contains ': ', which the value does not.
    "documented template with trailing comments": "---\nname: skill-name    "
    "       # Required: lowercase, hyphens, max 64 chars\nuser-invocable: true "
    "      # Optional: show in slash command menu (default: true)\ndescription: "
    "'x'\n---\n",
}


def test_detector_reports_every_misread_shape() -> None:
    """Each sample must be caught by the rule it was added for, not by a neighbour.

    Asserting only that some problem was reported let a sample be caught by an
    adjacent rule, so a rule could be deleted with every test still green.
    """
    missed = {
        name: frontmatter_problems(text, "sample.md")
        for name, (text, fragment) in MISREAD.items()
        if not any(fragment in problem for problem in frontmatter_problems(text, "s"))
    }
    assert not missed, f"frontmatter not caught by the rule it pins: {missed}"


def test_a_problem_names_its_line_and_its_cause() -> None:
    wrapped = frontmatter_problems(MISREAD["wrapped quoted value"][0], "sample.md")
    assert wrapped[0].startswith("sample.md:3:"), wrapped
    assert "does not close it" in wrapped[0], wrapped


def test_detector_accepts_valid_shapes() -> None:
    false_positives = {
        name: problems
        for name, text in READ_AS_WRITTEN.items()
        if (problems := frontmatter_problems(text, "sample.md"))
    }
    assert (
        not false_positives
    ), f"detector rejected valid frontmatter: {false_positives}"


# ---------------------------------------------------------------------------
# Host-neutral shipped text
# ---------------------------------------------------------------------------
#
# Every host reads the same skill files — OpenCode and Pi point at
# claude-plugins/*/skills, Codex carries a byte-identical copy, and the skills.sh
# picker installs the plugin copies — so a word one harness uses for a capability
# every harness has makes the text wrong everywhere else. These rules hold over
# every shipped markdown file. Exempt: HTML comments (runtime literals matched
# across hosts, never prose a reader resolves) and the research digests under
# references/research/, which describe other systems in their own words.

SHIPPED_SKILL_ROOTS = (
    ROOT / "claude-plugins" / "manifest-dev" / "skills",
    ROOT / "claude-plugins" / "manifest-dev-tools" / "skills",
)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
RESEARCH_DIGEST = "references/research/"
PLUGIN_QUALIFIER = re.compile(r"manifest-dev(?:-tools)?:(?=[a-z])")
HOST_TOOL_NAMES = re.compile(
    r"\b(?:WebFetch|WebSearch|AskUserQuestion|TodoWrite)\b"
    r"|\b(?:Task|Skill|Bash) tool\b"
)
CONTEXT_FILE_NAME = "CLAUDE.md"
OTHER_CONTEXT_FILE_NAME = "AGENTS.md"
LAUNCH_VERB = re.compile(r"\bsub-?agents?\b", re.IGNORECASE)
# A delegation site: prose telling the reader to run work in another execution
# context. Each must carry, in the same paragraph, what to do on a host without one.
DELEGATION = re.compile(
    r"\b[Ll]aunch (?:one|an|a|each|every)\b[^.\n]{0,120}"
    r"\b(?:isolated (?:execution )?contexts?|verifier executions?)\b"
)
FALLBACK = re.compile(
    r"\binline\b|\bwhere none is available\b|\bno such (?:capability|context)\b"
    r"|\bno isolated (?:execution )?context\b"
)


def shipped_markdown() -> list[Path]:
    files = [
        path for root in SHIPPED_SKILL_ROOTS for path in sorted(root.rglob("*.md"))
    ]
    assert files, "no shipped markdown found"
    return files


def in_research_digest(path: Path) -> bool:
    return RESEARCH_DIGEST in path.as_posix()


def outside_html_comments(text: str) -> str:
    return HTML_COMMENT.sub("", text)


def line_hits(text: str, pattern: re.Pattern[str]) -> list[int]:
    return [
        number
        for number, line in enumerate(text.splitlines(), 1)
        if pattern.search(line)
    ]


def test_shipped_text_names_no_plugin_qualifier_outside_html_comments() -> None:
    problems = []
    for path in shipped_markdown():
        prose = outside_html_comments(path.read_text(encoding="utf-8"))
        for number in line_hits(prose, PLUGIN_QUALIFIER):
            problems.append(
                f"{path.relative_to(ROOT)}:{number}: plugin-qualified skill id"
            )
    assert not problems, "\n".join(problems)


def test_shipped_text_names_no_host_tool() -> None:
    problems = []
    for path in shipped_markdown():
        text = path.read_text(encoding="utf-8")
        for number in line_hits(text, HOST_TOOL_NAMES):
            problems.append(f"{path.relative_to(ROOT)}:{number}: host tool name")
    assert not problems, "\n".join(problems)


def test_shipped_text_names_the_context_file_only_where_it_detects_or_compares() -> (
    None
):
    """`CLAUDE.md` is one harness's instance of the project context file. A file may
    name it only as one of several (a detection table or a comparison also naming
    `AGENTS.md`) or inside a research digest."""
    problems = []
    for path in shipped_markdown():
        if in_research_digest(path):
            continue
        text = path.read_text(encoding="utf-8")
        if CONTEXT_FILE_NAME in text and OTHER_CONTEXT_FILE_NAME not in text:
            for number, line in enumerate(text.splitlines(), 1):
                if CONTEXT_FILE_NAME in line:
                    problems.append(
                        f"{path.relative_to(ROOT)}:{number}: names {CONTEXT_FILE_NAME} alone"
                    )
    assert not problems, "\n".join(problems)


def test_shipped_text_never_names_a_subagent_outside_research_digests() -> None:
    problems = []
    for path in shipped_markdown():
        if in_research_digest(path):
            continue
        text = path.read_text(encoding="utf-8")
        for number in line_hits(text, LAUNCH_VERB):
            problems.append(f"{path.relative_to(ROOT)}:{number}: names a subagent")
    assert not problems, "\n".join(problems)


def test_every_delegation_site_carries_an_inline_fallback() -> None:
    problems = []
    for path in shipped_markdown():
        if in_research_digest(path):
            continue
        text = path.read_text(encoding="utf-8")
        for paragraph in re.split(r"\n[ \t]*\n", text):
            if DELEGATION.search(paragraph) and not FALLBACK.search(paragraph):
                first = paragraph.strip().splitlines()[0][:80]
                problems.append(f"{path.relative_to(ROOT)}: no fallback near {first!r}")
    assert not problems, "\n".join(problems)


def test_no_shipped_skill_is_marked_internal() -> None:
    """`metadata.internal` reads as "do not install" to skill pickers, which dropped
    /do's own dependencies. A dependency ships as user-invocable: false instead."""
    problems = []
    for root in SHIPPED_SKILL_ROOTS:
        for skill_md in sorted(root.glob("*/SKILL.md")):
            block = frontmatter_block(skill_md.read_text(encoding="utf-8")) or []
            if any(line.strip().startswith("internal:") for line in block):
                problems.append(f"{skill_md.relative_to(ROOT)}: metadata.internal")
    assert not problems, "\n".join(problems)


SKILL_REFERENCE = re.compile(
    r"(?:invoke|activate|activates|activating|launch|run|runs|running|delegate|delegates)"
    r"[^.\n]{0,60}?the `([a-z0-9-]+)` skill",
    re.IGNORECASE,
)


def test_every_skill_a_shipped_skill_names_ships_beside_it() -> None:
    shipped = {
        path.name
        for root in SHIPPED_SKILL_ROOTS
        for path in root.iterdir()
        if path.is_dir()
    }
    problems = []
    for path in shipped_markdown():
        text = outside_html_comments(path.read_text(encoding="utf-8"))
        for match in SKILL_REFERENCE.finditer(text):
            name = match.group(1)
            if name not in shipped:
                problems.append(
                    f"{path.relative_to(ROOT)}: names `{name}`, which does not ship"
                )
    assert not problems, "\n".join(problems)


def test_every_dependency_only_skill_is_not_user_invocable() -> None:
    """A skill whose description says another skill calls it is a dependency and
    must not appear in slash menus."""
    problems = []
    for root in SHIPPED_SKILL_ROOTS:
        for skill_md in sorted(root.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8")
            block = frontmatter_block(text) or []
            description = declared_description(text)
            called = re.search(r"\b[Cc]alled by\b", description) is not None
            hidden = any(line.strip() == "user-invocable: false" for line in block)
            if called and not hidden:
                problems.append(
                    f"{skill_md.relative_to(ROOT)}: called-by skill is user-invocable"
                )
    assert not problems, "\n".join(problems)
