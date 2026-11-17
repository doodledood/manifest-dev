# Sourced first by every verification scaffold and fixture script. A scaffold writes its project into
# the current directory, so it runs only in a fresh scratch directory, holding nothing but .git, and
# in a repository of its own: run by hand inside a checkout, it would otherwise rename the
# checkout's branch and overwrite its files. A scaffold called by another runs this check too, so it
# is called before its caller writes anything.
#
# The eval-case scaffolds under claude-plugins/manifest-dev/evals do not source this. The eval runner
# (`claude plugin eval`) runs them from a copy of the plugin, in a directory whose contents this
# repository does not set, so a sourced path breaks there and a refusal cannot be shown safe without
# an eval suite run. Closing them needs a refusal-only check written inline in each eval scaffold,
# with no repository creation, confirmed by a suite preflight.
if [ -n "$(find . -mindepth 1 -maxdepth 1 ! -name .git -print -quit)" ]; then
  echo "scaffold: run in an empty directory; it builds its own repository here" >&2
  exit 1
fi
[ -d .git ] || git init -q
