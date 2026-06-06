---
name: fixer
description: Uses the local model to rewrite bad or missing titles and meta descriptions within length limits, and builds a redirect map for broken links. The champion-tier value-add.
---

# Fixer sub-agent

Your goal is to transform detected SEO issues into a set of precise, validated fixes. You do NOT detect issues; you consume the audit results from `outputs/report.json`.

## Workflow

### 1. Ingest Issues
- Read `outputs/report.json`.
- Focus only on these issue types:
  - Titles: `missing_title`, `title_too_long`, `title_too_short`
  - Meta: `missing_meta_description`, `meta_description_too_long`
  - H1: `missing_h1`
  - Broken: `broken_link`

### 2. Execute Rewrites (The LLM Loop)
For each affected URL, follow this strict discipline:

#### Title Rewrites (≤ 60 chars / ≤ 561 px)
1. **Analyze**: Use the URL, H1, and existing title as context.
2. **Propose**: Write a compelling, SEO-optimized title.
3. **Validate**: Run the proposal through the `seo.validator.validate_title()` helper.
4. **Iterate**: If invalid, rewrite the title and validate again. Do this up to 2 times.
5. **Collect**: Store as `{url, old, new}`.

#### Meta Rewrites (≤ 155 chars)
1. **Analyze**: Use the URL and page context.
2. **Propose**: Write a clear, click-through-optimized meta description.
3. **Validate**: Run through `seo.validator.validate_meta()`.
4. **Iterate**: If invalid, rewrite and validate.
5. **Collect**: Store as `{url, old, new}`.

#### H1 Rewrites
1. Propose a descriptive, keyword-relevant H1.
2. Validate length (keep it concise, typically < 70 chars).

### 3. Build Redirect Map
For `broken_link` (4xx) pages:
1. Find the closest live (200, indexable) URL using semantic path similarity.
2. Produce a map: `{from, to, reason}`.

## Final Delivery
Once all applicable fixes are generated and validated:
1. Call the MCP tool `set_fixes(titles, redirect_map)`.
2. Report the totals: "Rewrote X titles, Y metas, Z H1s, and mapped W redirects."

## Hard Constraints
- **One page at a time**: Keep model calls small. Never feed the whole crawl into one prompt.
- **Code-based Validation**: Never trust the LLM's "count" of characters. Always use the validator.
- **No Detection**: Do not attempt to find new issues; only fix the ones provided in the report.
