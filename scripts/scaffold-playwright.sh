# Sourced by a verification scaffold whose scenario needs its page rendered; it only defines
# link_playwright, so running this file does nothing. A page check run from the scratch project
# finds Playwright where a web project's own install would put it: under ./node_modules.
# link_playwright links the module the driving machine names in DESIGN_TOOLS_PLAYWRIGHT there (a
# `playwright` or `playwright-core` directory, the setting scripts/design-evals/browser.mjs reads),
# keeps node_modules out of the fixture's commits, and leaves the linked module's name in
# playwright_module for the fixture's package.json. Without the setting the scaffold stops: a
# drive that cannot render ends BLOCKED after its model quota is spent. The browser is the one
# Playwright bundles. Nothing here launches it, because a scaffold runs with a scratch HOME, where
# Playwright would not find its browsers.
link_playwright() {
  local module=${DESIGN_TOOLS_PLAYWRIGHT:-} name
  if [ -z "$module" ]; then
    echo "scaffold: set DESIGN_TOOLS_PLAYWRIGHT to a playwright or playwright-core module directory" >&2
    return 1
  fi
  name=$(basename "$module")
  case "$name" in
    playwright | playwright-core) ;;
    *)
      echo "scaffold: DESIGN_TOOLS_PLAYWRIGHT must end in playwright or playwright-core, not $name" >&2
      return 1
      ;;
  esac
  if [ ! -f "$module/package.json" ]; then
    echo "scaffold: no Playwright module at $module" >&2
    return 1
  fi
  mkdir -p node_modules
  ln -s "$module" "node_modules/$name"
  printf 'node_modules\n' > .gitignore
  playwright_module=$name
}
