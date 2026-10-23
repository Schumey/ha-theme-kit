# Publishing through HACS

1. Create a **public** GitHub repo, push this project.
2. `hacs.json` in the root already says `"render_readme": true`. Set `name`.
3. Add repository topics (`home-assistant`, `hacs`, `theme`, …). The repo needs a description and a README.
4. Tag a release (`vX.Y.Z`, annotated) and create a GitHub release. HACS shows releases, not the default branch, when releases exist.
5. For HACS **default** listing (so people find it in the HACS search without adding a custom repository), submit a PR to `hacs/default`. Read their current rules first: the integration needs a valid `manifest.json`, a `hacs.json`, a release, brand images in `custom_components/<domain>/brand/` (or the `home-assistant/brands` repo) and a passing HACS action. Until then users add it via *HACS → ⋮ → Custom repositories → Integration*.
6. Tell users in the README to add to `configuration.yaml`:

   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```

Checklist before each release: `python tools/check.py x.y.z`, test dashboard looked at in light and dark, `CHANGELOG.md` section, annotated tag.
