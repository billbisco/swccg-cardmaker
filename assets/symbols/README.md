# Shared set-symbol display exports

The artwork source is CardMaker's existing `assets/icons/set-*-{decipher,pc}.png` masters. Wiki consumers should reuse these exports rather than cut or redraw another parallel icon collection. `manifest.json` pins each master path/SHA256 and derivative SHA256. Existing source PNGs and CardMaker rendering are unchanged.

Regenerate from the repository root:

```sh
python tools/export_set_symbols.py
```

The exporter records the checkout's current Git commit. For a staged source bundle outside that checkout, pass `--root`, `--output` and an explicit40-character `--source-commit`; it will not silently attribute a parent repository's commit to CardMaker.

The96px files have true alpha and a lossless WebP encoding of the deterministic display resize. The script verifies decoded RGBA equality with that resize. This is not a claim that the96px derivative contains every pixel of the312px master; the original PNG remains authoritative and is retained. No palette substitution, generative reconstruction or background-color guess is used.

These files contain sphere artwork, as CardMaker's existing masters do. A complete printed symbol also needs its correct ring. CardMaker's classic inline recipe is the sphere at42px with a4px `#111` external ring (`render.py`, `DC_SPHERE_CSS`). A20px total display therefore uses a16.8px sphere and1.6px ring. Use a round clipping boundary so invisible RGB in source corners never shows. Infoboxes should place a linked expansion name alongside the icon.

Do not assume `pc` means a Virtual set mark or that `decipher` identifies a regular/AI ring. They name the existing image families. In particular **the current CardMaker Coruscant asset is not an approved regular silver-ring Wiki symbol**. The Wiki's physical-printing rule is regular Coruscant=silver ring, AI=gold; prove and store distinct variants before migration. Reflections Gold original/remaster must also remain distinct. Premiere has no symbol. Original Virtual, Legacy and Modern set marks require a separate inventory; this initial export does not assert those families complete.

Source provenance: `assets/icons/SET-ICONS-PROVENANCE.md` (its Rev80 section supersedes earlier rows) and `tools/set_spheres/sources.json`. Do not rely on the older provenance JSON alone: some source descriptions predate the Rev80 re-cuts. A shared-source migration should retain the original master checksums, printing-aware keys and preview evidence so Wiki and CardMaker cannot silently diverge.

Story435 in `swccg-guild/work` tracks the Wiki pilot, transparent backgrounds, searchable card-text presentation and migration gaps. Story286 separately tracks filling the wider Wiki infobox coverage. This export creates reusable assets; it does not itself change any Wiki card or claim every printed variant is verified.
