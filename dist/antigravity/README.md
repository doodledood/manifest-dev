# Manifest Dev in Google Antigravity

Link both plugin folders from a checkout to keep one copy of the skills. Manifest Dev contains the main workflow. Manifest Dev Tools
adds pull-request and prompt reviews, handoff, and teaching. Both use the same
skills as the other clients, with no account connection or MCP server required
by either plugin.

## Link a checkout

Run these commands from a folder where you want to keep the repository. If you
already have a checkout, skip the clone and use its path instead.

```sh
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev
mkdir -p "$HOME/.gemini/config/plugins"
ln -s "$PWD/claude-plugins/manifest-dev" "$HOME/.gemini/config/plugins/manifest-dev"
ln -s "$PWD/claude-plugins/manifest-dev-tools" "$HOME/.gemini/config/plugins/manifest-dev-tools"
```

If either destination already exists, inspect it before replacing it. Open
**Customizations → Installed** and confirm **Manifest Dev** and **Manifest Dev
Tools** appear. Start a new chat and try `/figure-out` or `/walk-pr`.

## Install a separate copy

With the [Antigravity CLI](https://antigravity.google/docs/cli/plugins/), run
`agy plugin install ./claude-plugins/manifest-dev` and
`agy plugin install ./claude-plugins/manifest-dev-tools` from the checkout. You
can also place a complete copy of each plugin folder under
`~/.gemini/config/plugins/`, keeping each folder's `.antigravity-plugin/` and
`skills/` together. See [Antigravity’s plugin documentation](https://antigravity.google/docs/plugins/).

Use one install method. If you previously added the same skills as standalone
global skills, remove only those prior copies so the plugins provide the skills
once.

## Update

In the checkout, run `git pull --ff-only`. Linked folders already point at the
new files. Use **View → Reload** or relaunch Antigravity, then start a new
chat; an existing chat may still know the older skill set. If you installed separate
copies, refresh both copies from the updated checkout instead. With the CLI,
uninstall both existing copies before installing them again from their local
folders. Compare the installed versions with `agy plugin list` or the Installed
tab.

A local install does not pull from GitHub. If you already update the checkout
with a scheduled job, linked folders use that same update without a second job.
