# Release verification — 25 November 2026

## Executed local checks

- **9 Python test cases passed**, covering source IDs, official evidence on all factual rows, null handling, restaurant classifications, couple meal arithmetic, date/occupancy validation, hotel surcharge arithmetic, HTML semantics and all dashboard-local links/anchors/assets.
- **113 browser checks passed** after relocation to `/for-two/`: all nine pages at 1440, 390 and 320 CSS-pixel widths; no page-level horizontal overflow; axe WCAG A/AA checks at desktop/mobile widths; working navigation, category/search combination, empty states, cluster deep links, local hotel/suggestion persistence, review export and no-JavaScript data visibility. No browser JavaScript errors.
- **40 tracked HTML pages** across the combined repository scanned for relative file targets: **0 missing relative-file references**. This structural scan is not a factual verification of the other sessions’ content or a test of external link uptime.
- Git comparison against main at `62a8a24` confirms existing other-owner files are unchanged. Additions are confined to `for-two/**`, its unique validation workflow and the appended root coordination log.
- Dependency installation/audit reported zero vulnerabilities. Browser tooling is development-only; site runtime has no third-party script or font dependency.
- Fixed issues found during tests: duplicate empty table IDs, text contrast and insufficient inline-link differentiation. Browser initially lacked NSS libraries; the runner now uses the libraries shipped with the npm-packaged browser, without downloading system packages.

## Publication status

The direct GitHub Pages settings update was denied with HTTP 403. Existing Pages settings (`main`, `/`) and its deployment environment were left untouched.

- [PR #7](https://github.com/kanlerxz87-cyber/ChinaFun3/pull/7) merged on 25 November 2026 at 13:32 UTC, commit `e7c538fdec3a5451e8bc36dabdbc6b11a2244990`.
- Both repository and isolated-dashboard CI checks passed. [Isolated validation run](https://github.com/kanlerxz87-cyber/ChinaFun3/actions/runs/45624417603).
- [GitHub Pages build and deployment](https://github.com/kanlerxz87-cyber/ChinaFun3/actions/runs/45624561650) completed successfully for that exact merge commit, including the deployment job.
- Public-page fetch from the research tool failed both during and after deployment. Consequently, deployment is confirmed by GitHub, but independent public HTTP/content verification is **not confirmed**. Local browser rendering at the identical `/for-two/` path passed. The sandbox network allowlist does not include github.io.
- GitHub emitted a non-blocking Node 20 deprecation annotation for its Pages artifact action (automatically run on Node 24); no deployment failure occurred.

Published path: https://kanlerxz87-cyber.github.io/ChinaFun3/for-two/

## Research boundary

51 official/media records; 4 hotels; 7 restaurants; 5 activities; 6 dated seven-night hotel quote inputs. Four restaurant menus have usable published couple totals. 14 review issues remain visible; no unsupported one-hour ranking or complete trip budget was produced. Other owners’ root/docs/considered research was preserved, not independently endorsed. See [verification.md](verification.md).
