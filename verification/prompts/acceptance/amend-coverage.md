Use define --autonomous to amend ./manifest.md in place. Read decisions.md for the granted
revision authority. Do not execute the implementation.
QA found that an empty label was lost. AC-1.1 already states that empty labels are preserved;
the sole sample in Evidence was nonempty. Update what was inadequate.
The streaming design in the Approach was replaced by one bounded in-memory serializer; the
supported dataset is small, all records survive, and format ownership remains single. Encode
this working design change and preserve the owner's delivery boundary and required proof.
Keep the current 200 ms claim: the responsiveness amendment is a separate pending decision.
Use the supplied records directory. No external services.
