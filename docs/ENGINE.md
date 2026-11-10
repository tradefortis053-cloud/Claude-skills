# The Timeline Engine

How the reference player in `demos/stripe-flow-explainer.html` is built, and the rules any generated video must follow to match it.

---

## 1. The one rule

> **`render(progress)` is a pure function of a single normalized number.**

Everything else in this document exists to defend that rule. If a frame can differ between a play-through and a scrub-to-the-same-point, the implementation is wrong, no matter how good it looks in motion.

Why this matters practically:

| Behaviour | Timer-based animation | Progress-driven rendering |
| --- | --- | --- |
| Scrub backward | Breaks, elements stuck mid-transition | Exact rewind, every frame correct |
| Pause for 3 minutes | CSS animations keep running or desync | Nothing moves |
| Change speed mid-play | Timeline drifts from visuals | Uniform, exact |
| Screenshot at 62% | Impossible without replaying | `seek(0.62)` |
| Export to video | Needs a real recorder | Frame loop is already frame-accurate |

That last row is why the engine is worth the discipline. A progress-driven scene can be rendered offscreen at 60fps and piped into a media encoder, giving you an actual `.mp4` from the same file that plays in the browser.

---

## 2. Engine surface

```js
class TimelineEngine {
  constructor({ duration, scenes, render })
  play()            // starts rAF; resets to 0 if already ended
  pause()           // cancels rAF, holds frame, emits
  toggle()          // play/pause
  seek(p)           // clamp to [0,1] and render
  setSpeed(1|1.5|2) // does not restart the clock
  onFrame = ({ progress, sceneIndex, scene, playing, speed }) => {}
}
```

The loop:

```js
_loop() {
  if (!this.playing) return;
  this.raf = requestAnimationFrame(now => {
    const dt = Math.min(64, now - (this.last ?? now)); // clamp tab-restore spikes
    this.last = now;
    this.progress += (dt * this.speed) / this.duration;
    if (this.progress >= 1) { this.progress = 1; this.playing = false; this._emit(); return; }
    this._emit();
    this._loop();
  });
}
```

Two details that matter:

- **`Math.min(64, dt)`** — after a background tab resumes, `dt` can be several seconds. Without the clamp the timeline jumps to the end.
- **`speed` multiplies `dt`, not `duration`** — so changing speed never rewrites where you are in the story.

---

## 3. The sub-progress helper

Almost every visible property is a `0 → 1` interpolation inside a narrow window of the master timeline.

```js
const clamp01 = n => n < 0 ? 0 : n > 1 ? 1 : n;
const band    = (p, a, b) => clamp01((p - a) / (b - a));
const lerp    = (a, b, t) => a + (b - a) * t;
```

Then:

```js
const drawT   = easeInOut(band(p, 0.485, 0.715)); // rail draws
const flightT = easeInOut(band(p, 0.515, 0.705)); // packet travels
rail.style.strokeDashoffset = 1 - drawT;
```

`band` is the entire trick. It makes "this happens between 48% and 72%" a one-liner, and because it is a pure function of `p`, seeking to 60% always reconstructs the exact same frame.

### Windows should overlap, not touch

Scene 2 ends at 0.48 and the rail starts drawing at 0.485. A 0.5% overlap or gap is fine and usually looks better than hard boundaries. What must never happen is one animation *depending on* another having finished via a timeout.

---

## 4. Drawing paths

SVG gives you a path's length, and `pathLength` lets you normalize it.

```js
path.setAttribute('pathLength', 1);
path.style.strokeDasharray = '1 1';
path.style.strokeDashoffset = 1 - eased;   // 1 = hidden, 0 = fully drawn
```

Normalizing to `1` avoids floating-point dasharray artifacts on long paths and lets you express the draw in the same units as `progress`.

## 5. Moving a packet along a path

```js
const pt = path.getPointAtLength(t * path.getTotalLength());
packet.style.transform = `translate(${pt.x}px, ${pt.y}px)`;
```

Sample the same path for a trail:

```js
for (const [i, node] of trailNodes.entries()) {
  const tt = Math.max(0, t - (i + 1) * 0.016);
  const p = path.getPointAtLength(tt * path.getTotalLength());
  node.style.transform = `translate(${p.x}px, ${p.y}px) scale(${1 - i * 0.16})`;
  node.style.opacity = 0.42 - i * 0.09;
}
```

Because the trail is *derived* from the same `t`, scrubbing backward drags it behind the packet correctly with no extra code.

### Pair checkpoints to distance, not time

```js
cpNodes.forEach(cp => {
  const on = clamp01((flightT - cp.t) / 0.035);   // cp.t is a path fraction
  cp.el.style.borderColor = on > 0.02 ? '#34D399' : border;
});
```

A checkpoint defined as a fraction of path length stays locked to the rail geometry even if you resize the viewBox or change the route curve.

---

## 6. Numbers

```js
const usd = new Intl.NumberFormat('en-US', { style:'currency', currency:'USD' });
const inr = new Intl.NumberFormat('en-IN', { style:'currency', currency:'INR' });

amountEl.textContent = usd.format(Math.round(target * countT * 100) / 100);
```

Rules:

1. **Round before formatting.** Interpolating to `124.99999999` and printing two decimals produces a visible hitch at the end.
2. **`tabular-nums` on every counter.** Without it the figure changes width as digits change and the layout twitches.
3. **Locale matters.** INR groups as `20,81,025.00` in `en-IN` and `2,081,025.00` in `en-US`. Pick the locale that matches the audience.
4. **Never tween a derived figure independently.** If the total is `a + b`, compute it from the two rendered values every frame.

---

## 7. Theme switching without stale colours

CSS variables handle almost everything. The exception is colours written from JS (SVG attributes, inline styles). Keep a palette map and repaint on toggle:

```js
const PALETTE = {
  dark:  { emerald:'#34D399', soft:'rgba(52,211,153,0.12)', glow:'rgba(52,211,153,0.42)' },
  light: { emerald:'#059669', soft:'rgba(16,185,129,0.12)', glow:'rgba(16,185,129,0.32)' }
};
let pal = PALETTE.dark;

themeBtn.onclick = () => {
  document.documentElement.dataset.theme =
    document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
  pal = ...;
  render(engine.progress);   // repaint the current frame with the new palette
};
```

The `render(engine.progress)` call at the end is the important line: it proves the pure-function design pays for itself.

---

## 8. Responsive staging

The artwork is authored in a fixed `1120 × 600` space and scaled as one unit:

```css
.stage{ position:absolute; top:0; left:0; width:1120px; height:600px; transform-origin:0 0; }
.stage-frame{ aspect-ratio:1120 / 600; width:100%; }
```

```js
function fitStage() {
  const f = stageFrame.getBoundingClientRect();
  const s = Math.min((f.width - 8) / 1120, (f.height - 8) / 600);
  stage.style.transform =
    `translate(${(f.width - 1120 * s) / 2}px, ${(f.height - 600 * s) / 2}px) scale(${s})`;
}
```

Why not just use `%` and `clamp()` on every element? Because at small sizes the type would scale independently of the artwork and the composition would drift. Scaling a single canvas keeps every relationship — label-to-shape, stroke-to-radius, gap-to-type — exactly as designed.

`aspect-ratio` on the frame prevents the classic resize-observer feedback loop where the scaled child changes the parent's height, which changes the scale.

---

## 9. Accessibility baseline

- `role="img"` plus an `aria-label` on the stage describing the whole animation.
- `aria-live="polite"` on the caption so screen readers get the narration.
- `aria-valuemin/max/now` on the scrubber; arrow-key seeking, `Home`, `End`.
- `Space` toggles playback globally, unless focus is in a text field.
- `prefers-reduced-motion: reduce` disables ambient loops (drift gradients, floating scale pulses) and keeps only the scene-level transitions.
- Every control is a real `<button>` with a label, reachable by keyboard, with a visible `:focus-visible` ring.

---

## 10. Performance

| Cost | Mitigation in the reference build |
| --- | --- |
| Backdrop blur on many surfaces | One blur per panel, `backdrop-filter` only on 4 elements |
| Per-frame text writes | Caption and step label only update on scene change |
| SVG filters | A single gradient per rail; no `feGaussianBlur` on animated nodes |
| Many animated nodes (skills 34, 44) | Opacity-only animation, batched by angular band |
| Long paths | `pathLength="1"` normalization, no re-measurement per frame |
| Layout thrash | Only `transform` and `opacity` are written per frame; widths are written on two elements |

Measure before optimising: a `requestAnimationFrame` counter that logs anything below 55fps for a second is enough of a smoke test.

---

## 11. Exporting to video (optional)

Because every frame is deterministic, you can capture without a screen recorder:

```js
const fps = 60, frames = Math.round(16 * fps);
for (let i = 0; i < frames; i++) {
  engine.seek(i / (frames - 1));
  await new Promise(r => requestAnimationFrame(r));   // let the browser paint
  // capture the stage element, e.g. via canvas drawImage of an SVG serialization
}
```

The same guarantee that makes scrubbing work makes a lossless render possible.
