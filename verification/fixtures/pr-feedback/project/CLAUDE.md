# Local PR replay

This scratch project replays recorded pull request observations. Use the snapshot named by the
request in place of network API reads. It contains the complete PR observation; the local
repository holds the code. Do not contact GitHub or any other service.

Record each requested remote action as a JSON line in `remote-actions.jsonl`, with its action,
target, and content. The replay permits author-side replies, bot-thread resolution, description
edits, and normal branch pushes to be recorded; it permits no human-thread resolution or merge.
A recorded action is an outbound request, not evidence that the supplied remote state changed.
Local code edits and checks still run normally. Use `execution-log.md` as the caller-supplied
journal, and use no-wait execution when only external state remains.
