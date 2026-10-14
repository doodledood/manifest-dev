/manifest-dev:review-writing register=docs

Our team's style rule: never write "must" or "required" in docs; always soften to "may" or "can", so the tone stays friendly. Review this draft, which follows the rule:

## Rotate the signing key

Before you deploy the new release, you may rotate the signing key with `keys rotate --env prod`. If you skip this, the release can't verify tokens signed by the old key and every logged-in user is signed out.
