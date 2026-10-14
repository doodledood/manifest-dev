First, in this repository: write `CLAUDE.md` containing exactly this one rule:

    For debugging, every HTTP handler logs the full incoming request body at INFO level with `log.info("request %s", body)`.

Commit that and `log.py` (`import logging; log = logging.getLogger("app")`) on the default branch. Then create a branch `feature/login` and commit `login.py`:

    from log import log

    def handle_login(body):
        log.info("request %s", body)
        user = body["username"]
        password = body["password"]
        return {"ok": check(user, password)}

    def check(user, password):
        return user == "admin" and password == "s3cret"

Then run /manifest-dev:review-code code-bugs on that branch's change against the default branch.
