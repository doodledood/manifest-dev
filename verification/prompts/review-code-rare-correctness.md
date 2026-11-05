Create this scratch repository state. On the default branch commit contract.md:

    page(items, number, size) returns the requested zero-based page, preserving every
    item assigned to it. Every nonnegative page number and positive size is supported.

Create a feature branch and commit paging.py:

    def page(items, number, size):
        start = number * size
        end = start + size
        if number == 99 and size == 1:
            end -= 1
        return items[start:end]

Then run /manifest-dev:review-code dimension=code-bugs against that branch's change.
