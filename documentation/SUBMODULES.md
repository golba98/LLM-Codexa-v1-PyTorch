# Working with the component submodules

The eight Codexa component repositories appear under `components/` as Git
submodules. Each submodule is a pointer to one exact commit of an independent
repository; the component code and history stay in that repository.

## Cloning

Clone the showcase together with every component:

```bash
git clone --recurse-submodules https://github.com/golba98/LLM-Codexa-v1-PyTorch.git
```

If you already cloned without submodules, populate them afterwards:

```bash
git submodule update --init
```

A plain clone without either step leaves the `components/` directories empty.

## Pins are exact and do not update automatically

The showcase records a commit for every component, not a branch. Cloning,
pulling the showcase or running `git submodule update` always checks out those
recorded commits, even when the component's `main` branch has moved on. This
keeps the showcase reproducible: the same showcase commit always yields the
same component sources.

Each checked-out submodule is in a *detached HEAD* state at its pinned commit.
To make changes to a component, work in that component's own repository (or
check out a branch inside the submodule first) and submit them there.

Check the current pins and whether any working copy differs from them:

```bash
git submodule status
```

A leading `+` means the checked-out commit differs from the recorded pin; a
leading `-` means the submodule is not initialized.

## Bringing component updates into the showcase

Updates are deliberate and reviewed like any other change:

1. Make and merge the change in the component repository.
2. Move the pin in a showcase branch, either to the latest `main` of a
   component:

   ```bash
   git submodule update --remote components/LLM-Data
   ```

   or to a specific commit:

   ```bash
   git -C components/LLM-Data fetch origin
   git -C components/LLM-Data checkout <commit>
   ```

3. Review the new pin with `git diff --submodule=log`, update the pinned
   commits in the [component catalog](COMPONENTS.md), and commit the changed
   gitlink:

   ```bash
   git add components/LLM-Data documentation/COMPONENTS.md
   git commit -m "chore(components): update LLM-Data pin"
   ```

4. Open a pull request against the showcase.

`.gitmodules` sets `branch = main` for every component, which is the branch
`--remote` follows. Prefer moving components together to a set that has been
tested as a whole: the integration repository records its tested combination in
`compatibility.json`
([LLM-From-Scratch](https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1)).
