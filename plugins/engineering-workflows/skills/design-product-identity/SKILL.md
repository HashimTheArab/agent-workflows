---
name: design-product-identity
description: Use when creating, replacing, refining, or shipping a product logo, brand mark, wordmark, favicon, application icon, or identity system across a real product.
---

# Design Product Identity

Treat a logo as a product asset, not an image-generation result. Explore broadly, select critically, construct deterministically, and validate where the identity actually lives.

## 1. Audit Before Drawing

Inspect the product, audience, name, current UI, existing assets, build targets, and brand constraints. Find every surface that consumes the identity. Write or update the relevant product or brand spec with the code.

If the owner has selected a direction, preserve its defining idea. Raise concrete legibility, resemblance, or technical risks, but do not silently substitute your preference. Keep a strong alternate as an alternate.

## 2. Explore Real Directions

When the brief is open, create 3-6 genuinely different concept families in monochrome first. Reject:

- generic sparkles, blobs, gradients, pseudo-3D, and arbitrary loops;
- forced letter-folds or symbols that need a paragraph to work;
- marks whose strongest reading is an unintended object;
- silhouettes that resemble a famous adjacent brand.

Image generation may accelerate exploration, but never ship a crop from a generated concept sheet. Redraw the selected mark as exact vector geometry.

## 3. Select Hostilely

Compare candidates on recognition, distinctiveness, accidental meanings, one-color performance, wordmark cohesion, and clarity at 16-32 px. When available, use a strong independent visual critic - such as Claude Opus via `claude -p` - to aggressively test accidental meanings, adjacent-brand resemblance, and small-size failures. Keep the workflow portable when that model or tool is unavailable, and treat its critique as evidence, not authority.

Do not rationalize a weak shape with brand-story prose. Fix or reject it.

## 4. Construct a System

Create a canonical SVG mark, wordmark/lockup rules, one-color and reverse forms, and an app-icon master. Use unique SVG IDs when masks or gradients can repeat in the DOM. Allow documented optical variants at tiny sizes when the canonical geometry degrades.

Preserve selected source files and worthwhile alternates with unambiguous names. Record palette, typography/license, geometry, safe area, and export provenance.

Read [references/quality-gates.md](references/quality-gates.md) before implementing or approving final assets.

## 5. Validate and Ship

Render a size rail at 16, 20, 24, 32, and 64 px plus a large master. Inspect light, dark, reverse, app-tile, favicon, header, onboarding, and social-preview contexts.

Propagate from the canonical source to web metadata, reusable UI components, platform icon bundles, installers, and social assets. Use the repository's platform generator where one exists; do not add outputs the product does not consume.

Run the relevant build, typecheck, packaging, and visual smoke tests. For a stale tab icon, compare source, built, deployed, and fetched asset hashes plus cache headers before changing the design or adding cache-busting.

Handoff must clearly identify the active direction, preserved alternates, validations performed, known risks, and whether trademark clearance remains outstanding.
