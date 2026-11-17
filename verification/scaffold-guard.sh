# Sourced first by every verification scaffold and fixture script. A scaffold writes its project into
# the current directory, so it runs only in a fresh scratch directory: one holding nothing but a
# .git directory with no commit yet, or nothing at all, in which case it makes the repository. Run
# by hand inside a checkout or a no-checkout clone, it would otherwise rename that repository's
# branch and commit over its files. A scaffold called by another runs this check too, so it is
# called before its caller writes or commits anything.
#
# The eval-case scaffolds under claude-plugins/manifest-dev/evals do not source this. The eval runner
# (`claude plugin eval`) runs them from a copy of the plugin, in a directory whose contents this
# repository does not set, so a sourced path breaks there and a refusal cannot be shown safe without
# a paid run. Closing them needs a refusal-only check written inline in each eval scaffold, with no
# repository creation, confirmed by one ask-first scaffolded case run of the eval suite
# (scripts/evals/run_eval.sh with --scaffold); the suite's preflight runs no scaffold.
if [ -n "$(find . -mindepth 1 -maxdepth 1 ! -name .git -print -quit)" ] ||
  { [ -e .git ] && { [ ! -d .git ] || git rev-parse -q --verify HEAD >/dev/null; }; }; then
  echo "scaffold: run in an empty directory; it builds its own repository here" >&2
  exit 1
fi
[ -d .git ] || git init -q
