#!/usr/bin/env bash
# Model-check the ticket protocol with TLC.
#   check.sh <config>                       passes when TLC finds no error
#   check.sh --expect-violation <config>    passes only when TLC reports the one property the
#                                           config checks as violated, with its trace
# Exits 3 when Java or the pinned TLA+ tools are missing, so verify records it unreachable.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../../.." && pwd)"
pin="$here/../tla2tools.pin"
jar="${TLA2TOOLS_JAR:-$root/.tools/tla2tools.jar}"

expect=0
if [ "${1:-}" = "--expect-violation" ]; then expect=1; shift; fi
cfg="${1:?usage: check.sh [--expect-violation] <config name, e.g. races>}"
[ -f "$here/$cfg.cfg" ] || { echo "no config $here/$cfg.cfg" >&2; exit 2; }

# macOS can provide a `java` launcher even when no runtime is registered.
# Honor the standard JAVA_HOME for keg-only and other unregistered installations.
java_bin=java
if [ -n "${JAVA_HOME:-}" ]; then java_bin="$JAVA_HOME/bin/java"; fi
if ! "$java_bin" -version >/dev/null 2>&1; then
  echo "missing: a Java runtime (11 or newer), which TLC needs. Install a JDK from your package manager (for example openjdk-21-jdk or brew install openjdk), then re-run." >&2
  exit 3
fi
want="$(sed -n 's/^sha256=//p' "$pin")"
if [ ! -f "$jar" ]; then
  echo "missing: the TLA+ tools at $jar. Run scripts/setup.sh, which downloads the pinned version." >&2
  exit 3
fi
have="$( (sha256sum "$jar" 2>/dev/null || shasum -a 256 "$jar") | cut -d' ' -f1)"
if [ "$have" != "$want" ]; then
  echo "missing: the pinned TLA+ tools. $jar has checksum $have, not $want from $pin. Run scripts/setup.sh to replace it." >&2
  exit 3
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp "$here/TicketProtocol.tla" "$here/$cfg.cfg" "$work/"
cd "$work"
set +e
"$java_bin" -XX:+UseParallelGC -cp "$jar" tlc2.TLC -workers auto -metadir "$work/states" -config "$cfg.cfg" TicketProtocol.tla > tlc.out 2>&1
code=$?
set -e
cat tlc.out

if [ "$expect" = 0 ]; then
  if [ "$code" = 0 ] && grep -q "Model checking completed. No error has been found." tlc.out; then
    echo "PASS: $cfg: no property violated."; exit 0
  fi
  echo "FAIL: $cfg: TLC exited $code; see its output above." >&2; exit 1
fi

# One property per expect-violation config, so a reported violation is that property's.
props="$(sed -nE 's/^(INVARIANTS|PROPERTIES) *//p' "$cfg.cfg" | tr -s ' \n' ' ' | sed 's/ *$//')"
case "$props" in *" "*|"") echo "FAIL: $cfg must check exactly one property, not '$props'." >&2; exit 1;; esac
if grep -q "Invariant $props is violated" tlc.out || grep -q "Action property $props is violated" tlc.out \
   || { grep -q "Temporal properties were violated" tlc.out && grep -q "^PROPERTIES $props *$" "$cfg.cfg"; }; then
  echo "PASS: $cfg: TLC reports $props violated, as the pre-fix protocol should."; exit 0
fi
echo "FAIL: $cfg: TLC did not report $props violated (exit $code)." >&2; exit 1
