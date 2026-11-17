# Sourced first by every scaffold and fixture script. A scaffold writes its project into the current
# directory, so it runs only in a fresh scratch directory, holding nothing but .git, and in a
# repository of its own: run by hand inside a checkout, it would otherwise rename the checkout's
# branch and overwrite its files. A scaffold another scaffold calls inherits the check.
if [ -z "${MANIFEST_DEV_SCAFFOLD_NESTED:-}" ]; then
  if find . -mindepth 1 -maxdepth 1 ! -name .git | grep -q .; then
    echo "scaffold: run in an empty directory; it builds its own repository here" >&2
    exit 1
  fi
  [ -d .git ] || git init -q
  export MANIFEST_DEV_SCAFFOLD_NESTED=1
fi
