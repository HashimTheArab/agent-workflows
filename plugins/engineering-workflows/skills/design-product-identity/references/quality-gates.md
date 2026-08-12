# Product Identity Quality Gates

Load this before implementing or approving final assets.

## Concept

- The mark has one dominant reading and no damaging accidental symbol.
- Its silhouette is not confusingly close to a well-known adjacent brand.
- It works without gradients, shadows, animation, or explanatory copy.
- The owner-selected direction remains recognizable after refinement.
- Independent critique was considered when available.

## Geometry and Type

- Curves, joins, counters, and negative space remain intentional at small sizes.
- The mark survives one color, grayscale, light, dark, and reverse use.
- Wordmark spacing and optical alignment are tuned, not merely centered.
- Typography is licensed for the intended distribution.
- Repeated inline SVGs use unique mask, clip-path, filter, and gradient IDs.

## Size Rail

Inspect native-size renders at 16, 20, 24, 32, and 64 px. At each size confirm:

- the primary silhouette remains identifiable;
- cuts and counters do not close or turn into noise;
- stroke weight and padding feel optically balanced;
- no unintended letter or object becomes the dominant reading.

Use a documented tiny-size variant only when simpler geometry materially improves recognition.

## Asset Matrix

Ship only applicable targets:

| Target | Required evidence |
| --- | --- |
| Canonical mark | Editable SVG, monochrome and reverse |
| Product lockup | Responsive header/onboarding render |
| Web favicon | Source, production build, and fetched asset agree |
| App icon | Master plus platform-generated PNG/ICO/ICNS set |
| Social preview | Correct metadata and 1200x630 preview |
| Brand record | Palette, typeface, safe area, source, selected direction |
| Concepts | Active design unmistakable; alternates clearly labeled |

## Repository and Runtime

- Search for stale identity files, imports, metadata, and installer references.
- Verify build and typecheck; package when platform assets changed.
- Inspect real screenshots rather than only source SVGs.
- Confirm transparency, color profile, dimensions, and platform padding.
- Compare source/build/deployed hashes for stale assets.
- Inspect `Cache-Control`, service workers, and CDN/browser caching before assuming a favicon implementation is wrong.

## Release Notes

State what is active, what remains an alternate, which surfaces were verified, and any known issue. Visual review is not trademark clearance; say so when no clearance was performed.
