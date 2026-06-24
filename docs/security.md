# Security

## Never Commit

- Figma access tokens
- `.env` files
- browser snapshots
- screenshots from authenticated apps
- generated QA reports
- project-specific design-system catalogs
- local machine agent configuration

## Figma Tokens

Set `FIGMA_TOKEN` in your shell only when a workflow needs REST-backed library
catalog access. Live Desktop-plugin workflows do not require a token.

## Design QA Artifacts

Design QA snapshots can capture authenticated UI content. Write them to ignored
temporary folders such as `.tmp/design-qa/` and delete them when the review is
done.

## Reporting Issues

If you find a security issue, do not open a public issue with exploit details.
Contact the repository maintainers privately first.
