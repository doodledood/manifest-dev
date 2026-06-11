# Slack mrkdwn reference

Slack messages render via `mrkdwn`, not GitHub-flavored markdown. The flavors diverge on common syntax — write every Slack post using these conventions, never the GitHub equivalents.

## Conversion table

| Intent | Slack mrkdwn | NOT (GitHub markdown) |
|--------|--------------|------------------------|
| Bold | `*bold*` | `**bold**` |
| Italic | `_italic_` | `*italic*` |
| Strikethrough | depends on send path: `~strike~` when the path passes mrkdwn through verbatim (raw API, korotovsky/slack-mcp-server); `~~strike~~` when it translates markdown first (claude.ai Slack MCP) | assuming one form works on every send path |
| Inline code | `` `code` `` | same |
| Code block | ```` ```code``` ```` (triple backticks) | same |
| Link with label | `<https://example.com\|label>` | `[label](https://example.com)` |
| Bare link | `<https://example.com>` or just the URL | bare URL works too |
| Section title | `*Title*` on its own line (bold; no header syntax) | `# Title`, `## Title` |
| Blockquote | `> quoted line` | same |
| Bullet list | `- item`, each item on its own physical line | inline markers — `•` or `-` mid-line is literal text |
| Numbered list | `1. item`, each item on its own physical line | expecting `1.` to be parsed — mrkdwn has no list parsing |
| User mention | `<@U123ABC>` | n/a |
| Channel mention | `<#C123ABC\|name>` | n/a |
| User group ping | `<!subteam^S123ABC>` | n/a |
| Channel-wide ping | `<!here>` (active only) or `<!channel>` (everyone) | n/a |
| Email link | `<mailto:user@example.com\|Email user>` | `[Email user](mailto:...)` |

## Common mistakes

- **Headers don't render.** Slack ignores `# H1`, `## H2`, etc. — they appear as literal `#` characters. Use `*Bold Title*` on its own line for section titles.
- **Double-asterisk bold doesn't render.** `**text**` shows the literal asterisks around the text. Single `*` only.
- **Italic and bold are swapped relative to CommonMark.** Bold is `*`, italic is `_`. Don't mix them up.
- **GitHub link syntax renders verbatim.** `[label](url)` shows the brackets and parens literally. Use `<url|label>`.
- **No nested formatting in links.** `<url|*bold label*>` does not render the inner bold; the label is plain text.
- **Newlines are literal `\n`.** Markdown's two-trailing-spaces newline does not apply; emit real newline characters.
- **mrkdwn has no list syntax at all.** Slack never parses `- `, `1. `, or `•` into formatted lists in app-published text — markers are literal characters, and the entire visual list effect comes from real newlines. A marker mid-line does nothing: `_Locked:_ • item one • item two` is one run-on blob no parser will reflow. Put every item on its own physical line, **including the first**: a lead-in label like `*Need a human:*` must end with a newline before item 1, otherwise item 1 hangs off the label's line while the rest stand alone.
- **Pipes inside link labels need escaping.** In a link `<url|label>`, a literal `|` in the label breaks parsing — drop or replace it.

## Source

Slack's authoritative formatting reference: https://docs.slack.dev/messaging/formatting-message-text
