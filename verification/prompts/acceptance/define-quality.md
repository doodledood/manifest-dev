Use define --autonomous to make ./manifest.md for this task. Do not implement it.
A small maintained Python library turns inventory records into CSV. Add a label column so
operators can distinguish records without corrupting IDs, ordering or escaping. Users have
no interactive UI. Future maintainers need to extend the record format without duplicating
its serialization rules. Existing project checks are `python3 -m unittest`. Stop at a ready
pull request, never merge. No numeric performance or reviewer-severity policy was requested.
Use the scratch project and supplied records directory; no external services.

Then define a separate ./strict-manifest.md for the same work under this additional policy:
The project owner deliberately requires a review-code test-quality assessment with no Medium
or higher findings before delivery. This review policy is part of the project's acceptance.
