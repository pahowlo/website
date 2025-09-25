Contains main source code for personal website hosted as a [GitHub page](https://pahowlo.github.io), to the exceptions of some private components.

## Requirements

- python (see `.python-version`) to run scripts.
- node (see `.nvmrc`) to support vite mostly.
- pnpm to install npm dependencies. Only if you want to be able to use reliably the pnpm scripts.

These are not strict requirements and you might get away using older versions, but I don't want to test all possible combinations.

## Quick start

Depending if some components are still private at the time, you might not be able to fetch all custom links
and thus build.

```shell
./.scripts/fetch_links.sh

pnpm install:all
pnpm build
pnpm build:preview
```
