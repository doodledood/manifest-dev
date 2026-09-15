# Generation contract

Build the artifact in the assigned brief using the assigned copy of the design skill. Read that skill and the references selected by its loading rules. Treat this as an autonomous, standalone design task; there is no repository application to modify or existing design system beyond what the brief supplies. Do not consult another design skill or another artifact generation.

This generation phase is read-only. Return the complete artifact as response text; the operator will write and inspect it in a browser afterward. Do not write files, run a browser, delegate, fetch external content or claim that you rendered or tested it. Use only the assigned brief, skill and its references as task inputs. These limits apply equally to both compared versions.

Return:

1. A concise design note recording the task model, creative direction, exact reference files read, and the absence of render/behavior verification.
2. Exactly one fenced `html` block containing a complete HTML document. Keep CSS and JavaScript inline and use no external assets or network requests. It must be usable immediately when the operator saves it as an HTML file. Do not omit code or use placeholders for implementation.

Do not name the experiment, skill version or arm in the artifact itself. The supplied brief decides what the audience sees.
