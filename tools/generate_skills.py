#!/usr/bin/env python3
"""Generate the 55 skill specification markdown files from the JSON data sources."""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data"
SKILLS = ROOT / "skills"

CATEGORY_NAMES = {
    "A": "Payment Flows & Transactions",
    "B": "Banking Infrastructure & Ledgers",
    "C": "Wealth, Trading & Analytics",
    "D": "Security, Compliance & KYC",
    "E": "B2B SaaS, Lending & Credit",
}

CATEGORY_BLURB = {
    "A": "Consumer and merchant payment journeys: moving value between people, cards, codes and currencies.",
    "B": "The pipes underneath: clearing, ledgers, liquidity, contracts, reconciliation and treasury automation.",
    "C": "Portfolios, markets and analytics: growth curves, allocation, market microstructure and long-term investing.",
    "D": "Trust and control: identity, cryptography, fraud detection, access policy and defensive architecture.",
    "E": "Business money: credit, payroll, expenses, equity, revenue operations and the AI copilot layer.",
}


def format_duration(ms):
    return f"{ms / 1000:.0f}s ({ms:,} ms)"


def build_skill(skill):
    cat = skill["cat"]
    sid = skill["id"]
    title = f"Skill {sid} — {skill['name']}"
    subtitle_placeholder = "<caption text>"

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Category {cat}:** {CATEGORY_NAMES[cat]}")
    lines.append("")
    lines.append(f"> {skill['hook']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Skill Identity & Trigger")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| **Skill ID** | `{sid}` |")
    lines.append(f"| **Slug** | `skill-{sid}-{skill['slug']}` |")
    lines.append(f"| **Category** | {CATEGORY_NAMES[cat]} |")
    lines.append(f"| **Output file** | `output/skill-{sid}-{skill['slug']}.html` |")
    lines.append(f"| **Timeline length** | {format_duration(skill['dur'])} at 1x speed |")
    lines.append(f"| **Accent pair** | `{skill['accent']}` primary, `{skill['accent2']}` secondary |")
    lines.append("")
    lines.append("### Trigger Commands")
    lines.append("")
    lines.append("Any of the following must fire this skill:")
    lines.append("")
    lines.append(f"- `Execute Skill #{sid}`")
    lines.append(f"- `Run skill-{sid}-{skill['slug']}`")
    lines.append(f"- `Build the {skill['name'].lower()} explainer`")
    lines.append(f"- A natural-language request whose intent matches: _{skill['objective']}_")
    lines.append("")
    lines.append("### Objective")
    lines.append("")
    lines.append(skill["objective"])
    lines.append("")
    lines.append("### Deliverable Requirements")
    lines.append("")
    lines.append("- One self-contained `.html` file. No build step, no bundler, no local asset paths.")
    lines.append("- TailwindCSS via CDN **plus** inline CSS fallbacks so the layout survives a blocked CDN.")
    lines.append("- Inline SVG only. No external images, icon fonts or sprite sheets.")
    lines.append("- Full `TimelineEngine` control bar: Play / Pause / Replay, scrubber, step indicator, live captions, speed toggle (`1x`, `1.5x`, `2x`), theme toggle.")
    lines.append("- Deterministic rendering: the visual state must be a pure function of `progress` in `[0, 1]`.")
    lines.append("- Responsive down to 390px wide; the scene must scale rather than clip.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Scene-by-Scene Storyboard")
    lines.append("")
    lines.append("Scene boundaries are expressed as normalized timeline fractions so the engine can seek to any frame without drift.")
    lines.append("")
    lines.append("| Scene | Window | Caption |")
    lines.append("| --- | --- | --- |")

    scene_count = len(skill["scenes"])
    for i, scene in enumerate(skill["scenes"], start=1):
        name, window, _sub, _vis, _anim = scene
        lines.append(f"| **Scene {i}: {name}** | {window} | {scene[2]} |")
    lines.append("")

    for i, scene in enumerate(skill["scenes"], start=1):
        name, window, sub, vis, anim = scene
        lines.append(f"### Scene {i} — {name}")
        lines.append("")
        lines.append(f"**Timing window:** `{window}`")
        lines.append("")
        lines.append(f"**Narration subtitle:**")
        lines.append("")
        lines.append(f"> {sub}")
        lines.append("")
        lines.append(f"**On-screen elements:** {vis}")
        lines.append("")
        lines.append(f"**Animation physics:** {anim}")
        lines.append("")

    lines.append("### Scene Hand-off Rules")
    lines.append("")
    lines.append("- Each scene fades its predecessor out over the final 180 ms; there are no hard cuts.")
    lines.append("- The caption line crossfades with a 200 ms opacity transition and a 20 ms upward drift.")
    lines.append("- The step indicator text is `Step N of " + str(scene_count) + ": <Scene Name>` and must update exactly at the boundary fraction.")
    lines.append("- Scenes never overlap in the progress calculation; the active scene is the last one whose `start` is less than or equal to `progress`.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. SVG Vector Blueprint")
    lines.append("")
    lines.append("| Vector | Purpose | Construction |")
    lines.append("| --- | --- | --- |")
    for vec in skill["vectors"]:
        lines.append(f"| **{vec[0]}** | {vec[1]} | {vec[2]} |")
    lines.append("")
    lines.append("### SVG Implementation Notes")
    lines.append("")
    lines.append("- Use a single `<svg viewBox>` per scene group with `preserveAspectRatio=\"xMidYMid meet\"` so the artwork scales with the container.")
    lines.append("- Keep all stroke widths under 2.5 px at design scale; heavier strokes read as illustration rather than product UI.")
    lines.append("- Define gradients and filters once in a shared `<defs>` block; duplicating filter definitions causes measurable paint cost.")
    lines.append("- Drive self-drawing lines with `pathLength` normalization (`path.setAttribute('pathLength', 1)`) so dash offsets are expressed in 0 to 1 units.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Animation Physics")
    lines.append("")
    for item in skill["physics"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Shared Timing Constants")
    lines.append("")
    lines.append("```js")
    lines.append("const EASE = {")
    lines.append("  decel:  'cubic-bezier(0.16, 1, 0.3, 1)',   // Apple-style entry")
    lines.append("  inout:  'cubic-bezier(0.65, 0, 0.35, 1)',  // symmetric transitions")
    lines.append("  spring: { stiffness: 220, damping: 24 },   // damped settle")
    lines.append("  // linear is reserved for ambient rotation and real-time countdowns only")
    lines.append("};")
    lines.append("")
    lines.append("const clamp01 = (n) => Math.min(1, Math.max(0, n));")
    lines.append("const lerp = (a, b, t) => a + (b - a) * t;")
    lines.append("const band = (p, start, end) => clamp01((p - start) / (end - start));")
    lines.append("const easeOut = (t) => 1 - Math.pow(1 - t, 3);")
    lines.append("const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);")
    lines.append("const springOut = (t) => 1 - Math.exp(-6 * t) * Math.cos(9 * t);")
    lines.append("```")
    lines.append("")
    lines.append("Use `band(progress, start, end)` for every sub-animation. It is the reason scrubbing backward works.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Narration Subtitle Track")
    lines.append("")
    lines.append("These strings are the canonical captions. They render in the control bar and must not be paraphrased by the generator.")
    lines.append("")
    lines.append("```js")
    lines.append("const CAPTIONS = [")
    for i, scene in enumerate(skill["scenes"]):
        comma = "," if i < len(skill["scenes"]) - 1 else ""
        safe = scene[2].replace("'", "\\'")
        lines.append(f"  '{safe}'{comma}")
    lines.append("];")
    lines.append("```")
    lines.append("")
    lines.append("### Caption Styling")
    lines.append("")
    lines.append("- Font: Inter or Plus Jakarta Sans, 14 px at 500 weight, 1.5 line height.")
    lines.append("- Constrain to 2 lines maximum on desktop and 3 lines on mobile by shortening the scene copy, never by shrinking type below 13 px.")
    lines.append("- Colour: muted slate (`#64748B`) in light mode, `#94A3B8` in dark mode. Captions are secondary to the scene, never competing.")
    lines.append("- Reserve a fixed caption block height so scene changes never shift the control bar.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Reference Data Model")
    lines.append("")
    lines.append("Bind every number on screen to this object. Do not hard-code figures inside render functions.")
    lines.append("")
    lines.append("```js")
    lines.append(skill["data"])
    lines.append("```")
    lines.append("")
    lines.append("### Data Rules")
    lines.append("")
    lines.append("- All currency displays use `Intl.NumberFormat` with the correct locale and two decimals (or the correct precision for the asset).")
    lines.append("- Counters use `font-variant-numeric: tabular-nums` so digits do not shift width mid-count.")
    lines.append("- Any derived figure (totals, percentages, deltas) is computed from this object at load and asserted in a dev-only check.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Acceptance Checklist")
    lines.append("")
    lines.append("- [ ] Scrubbing from 100% back to 0% leaves every element in its exact initial state.")
    lines.append("- [ ] Pausing freezes all motion, including ambient loops and countdowns.")
    lines.append("- [ ] Changing speed to `1.5x` or `2x` does not desynchronize any sub-animation.")
    lines.append("- [ ] Both light and dark themes pass a 4.5:1 contrast check on body text.")
    lines.append("- [ ] Every number on screen traces back to the `Reference Data Model`.")
    lines.append("- [ ] The final frame holds for at least 800 ms and is a complete, readable statement.")
    lines.append("- [ ] No `linear` easing except for real-time countdowns and ambient rotation.")
    lines.append("- [ ] No external network requests beyond the TailwindCSS CDN.")
    lines.append("- [ ] Renders correctly at 390 px, 768 px, 1280 px and 1920 px widths.")
    lines.append("- [ ] `prefers-reduced-motion: reduce` collapses scene transitions to fades and disables ambient loops.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"### Skill Notes")
    lines.append("")
    lines.append(skill["notes"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Previous:** {prev_link(skill)}\u2003|\u2003**Next:** {next_link(skill)}\u2003|\u2003**Index:** [README](../README.md)")
    lines.append("")

    return "\n".join(lines)


PREV = {}
NEXT = {}


def prev_link(skill):
    idx = int(skill["id"]) - 1
    if idx < 1:
        return "_Start of series_"
    p = PREV.get(idx)
    return f"[{p['name']}](skill-{p['id']}-{p['slug']}.md)"


def next_link(skill):
    idx = int(skill["id"]) + 1
    n = NEXT.get(idx)
    if not n:
        return "_End of series_"
    return f"[{n['name']}](skill-{n['id']}-{n['slug']}.md)"


def main():
    all_skills = []
    for name in ("skills_01_20.json", "skills_21_40.json", "skills_41_55.json"):
        data = json.loads((DATA / name).read_text())
        all_skills.extend(data)

    all_skills.sort(key=lambda s: int(s["id"]))
    assert len(all_skills) == 55, f"expected 55 skills, found {len(all_skills)}"
    ids = [s["id"] for s in all_skills]
    assert len(set(ids)) == 55, "duplicate skill ids"

    for s in all_skills:
        PREV[int(s["id"])] = s
        NEXT[int(s["id"])] = s

    SKILLS.mkdir(exist_ok=True)
    for s in all_skills:
        body = build_skill(s)
        path = SKILLS / f"skill-{s['id']}-{s['slug']}.md"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
