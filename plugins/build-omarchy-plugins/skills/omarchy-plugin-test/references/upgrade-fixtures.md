# Exercise upgrades from affected state

Use [upgrade-cases.json](../assets/upgrade-cases.json) only in a temporary test
root. Map its fictional paths/formats to the plugin's actual migration input;
create private-state parent directories with mode `0755` initially. Add an
owned legacy path replaced by a symlink to an unrelated canary, plus an
unreadable existing file. Run the production migration, then assert each
applicable expectation. Do not write system paths or start the sample services.

Run fresh install, affected-version upgrade, interrupted migration and repeat
migration. Verify reconnect/startup actually consumes the repaired state.
Preserve unrelated or user-modified data; never infer ownership from a name.
These are fixture inputs, not a migration implementation or recorded passes.

Checked 30 October 2026: [legacy cache](https://github.com/omacom/omarchy-plugin-marketplace/issues/13257#issuecomment-6502311163),
[saved Wi-Fi profile](https://github.com/omacom/omarchy-plugin-marketplace/issues/13283#issuecomment-6513914836),
[managed listener](https://github.com/omacom/omarchy-plugin-marketplace/issues/13323#issuecomment-6513057859).
