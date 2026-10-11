import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * AccessFormCard — the FIRST SCREEN of Northeastern's Research Computing access request form (a ServiceNow
 * item on the university Tech Service Portal), rebuilt as a card. SHOW-THE-THING LAW, rung 3: the real page is
 * behind university sign-in and could not be captured by the build, so this card reproduces only the layout and
 * the labels that were confirmed on 2026-10-11 and DRAWS NOTHING BELOW THAT POINT (the page fades out instead).
 *
 * What is confirmed (and therefore drawn):
 *   - a white page, grey inputs, a white top bar reading "Technology" in bold black, a left menu of seven items;
 *   - heading "Requester Information"; fields Requester (Last, First), Phone, Email, Location (drop-down),
 *     UserID, Department (drop-down);
 *   - "Please choose one:" with the two exact radio options;
 *   - two instruction paragraphs (their SUBSTANCE is confirmed; the paragraph wording below is the build's
 *     phrasing of that substance, to be checked against the real screenshot before the film is published).
 * Input values are PLACEHOLDERS ("Last, First", "you@northeastern.edu"): never a real person's data.
 *
 * Replacement path: when a real screen recording of the form exists, swap this card's beats (B30–B35 of
 * claude-liam-lecture-requesting-access-to-explorer) for BrowserCapture / a screen clip; see that film's BUILD-LOG.md.
 *
 * Camera: `moves` are keyframes (at = fraction of the beat, x/y = focus point as fractions of the PAGE, scale ≥ 1).
 * Keep every move out of the 45–55% window (GATE T and Gate V sample the midpoint). Each move takes `moveSeconds` then HOLDS.
 * Highlights: `target` + `at` (fraction) + `kind`:
 *   glow   tinted terracotta outline on a field or label (replaced by the next glow/ring)
 *   ring   thick terracotta ring held round a field (used once, on UserID)
 *   select fills a radio dot (the previous radio empties)
 *   mark   a terracotta highlighter sweep behind the key phrase of paragraph p1 or p2 (stays)
 * Prose-bearing props avoid the names GATE T §8.5 counts (note/text/title/...): the page text is the real artifact.
 */

export const accessFormMoveSchema = z.object({
  at:    z.number().min(0).max(1),
  x:     z.number().min(0).max(1).default(0.5),
  y:     z.number().min(0).max(1).default(0.3),
  scale: z.number().min(1).max(3).default(1),
});

export const accessFormHighlightSchema = z.object({
  target: z.enum(['heading', 'requester', 'phone', 'email', 'location', 'userid', 'department', 'choose', 'radio1', 'radio2', 'p1', 'p2']),
  at:     z.number().min(0).max(1),
  kind:   z.enum(['glow', 'ring', 'select', 'mark']).default('glow'),
});

export const accessFormCardSchema = z.object({
  /** The link shown under the window, as text (the form is reached through it). */
  link:      z.string().default('https://bit.ly/NURC-AccessRequest'),
  /** When the link appears (fraction of the beat). Omit to show it from the start. */
  linkAt:    z.number().min(0).max(1).optional(),
  moves:     z.array(accessFormMoveSchema).min(1).max(6).default([{ at: 0, x: 0.5, y: 0.3, scale: 1 }]),
  moveSeconds: z.number().default(1.2),
  highlights: z.array(accessFormHighlightSchema).max(12).default([]),
  /** When the page fades out and "The form continues" appears (fraction). Omit to leave the fade at its resting depth. */
  continuesAt: z.number().min(0).max(1).optional(),
  topBarLabel: z.string().default('Technology'),
  durationSeconds: z.number().default(10),
});
export type AccessFormCardProps = z.infer<typeof accessFormCardSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

// ── page geometry (page px; the page is 1680 wide = the window's width at scale 1) ──
const PW = 1680, PH = 1380;
const WIN = { left: 120, top: 36, width: 1680, height: 860 };
const MAIN_X = 420;
const COL1 = 420, COL2 = 1060, COLW = 560;
const ROW_Y = [230, 360, 490];            // label tops; inputs sit 40 px lower, 64 px tall
const RECT: Record<string, { x: number; y: number; w: number; h: number }> = {
  heading:    { x: MAIN_X - 14, y: 112, w: 640, h: 76 },
  requester:  { x: COL1 - 10, y: ROW_Y[0] - 6, w: COLW + 20, h: 118 },
  phone:      { x: COL2 - 10, y: ROW_Y[0] - 6, w: COLW + 20, h: 118 },
  email:      { x: COL1 - 10, y: ROW_Y[1] - 6, w: COLW + 20, h: 118 },
  location:   { x: COL2 - 10, y: ROW_Y[1] - 6, w: COLW + 20, h: 118 },
  userid:     { x: COL1 - 10, y: ROW_Y[2] - 6, w: COLW + 20, h: 118 },
  department: { x: COL2 - 10, y: ROW_Y[2] - 6, w: COLW + 20, h: 118 },
  choose:     { x: MAIN_X - 14, y: 628, w: 360, h: 60 },
  radio1:     { x: MAIN_X - 14, y: 700, w: 1220, h: 104 },
  radio2:     { x: MAIN_X - 14, y: 820, w: 1220, h: 104 },
  p1:         { x: MAIN_X - 14, y: 950, w: 1220, h: 146 },
  p2:         { x: MAIN_X - 14, y: 1106, w: 1220, h: 146 },
};

const MENU = ['Hardware Borrow/Return', 'Infrastructure', 'IT Professional Services', 'Media and Equipment',
              'Research Computing', 'Teaching and Learning', 'Web Solutions'];
const INK = '#2B2B2B';           // the real page's own look: near-black text on white
const INPUT_BG = '#ECECEC';      // grey inputs
const PH_INK = '#5C5C5C';        // placeholder ink (>= 4.5:1 on the grey)
const TOP = '#FFFFFF';           // the real top bar is WHITE with black bold text (Bear's screenshot)
const MENU_PLUS = new Set(['Hardware Borrow/Return', 'Infrastructure', 'IT Professional Services', 'Research Computing', 'Teaching and Learning']);  // items shown with a boxed plus in the screenshot

const Field: React.FC<{ x: number; y: number; label: string; ph: string; drop?: boolean; italic?: boolean }> = ({ x, y, label, ph, drop, italic = true }) => (
  <div style={{ position: 'absolute', left: x, top: y, width: COLW }}>
    <div style={{ fontFamily: CLAUDE_FONT.ui, fontSize: 28, fontWeight: 600, color: INK, height: 40 }}>{label}</div>
    <div style={{ height: 64, background: INPUT_BG, border: '2px solid #BDBDBD', borderRadius: 6, display: 'flex', alignItems: 'center',
                  justifyContent: 'space-between', padding: '0 18px', fontFamily: CLAUDE_FONT.ui, fontSize: 30, color: PH_INK,
                  fontStyle: italic ? 'italic' : 'normal' }}>
      <span>{ph}</span>
      {drop ? <span style={{ fontSize: 24, color: INK }}>▼</span> : null}
    </div>
  </div>
);

export const AccessFormCard: React.FC<AccessFormCardProps> = ({ link, linkAt, moves, moveSeconds, highlights, continuesAt, topBarLabel }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames: total } = useVideoConfig();
  const winIn = clamp(spring({ frame, fps, config: { damping: 26, stiffness: 150, mass: 0.8 } }), 0, 1);
  const sp = (start: number) => clamp(spring({ frame: frame - start, fps, config: { damping: 22, stiffness: 130, mass: 0.7 } }), 0, 1);
  const at = (f: number) => Math.round(f * total);

  // camera: hold each keyframe, ease to the next from its `at`
  const mv = [...moves].sort((a, b) => a.at - b.at);
  const mf = Math.max(1, Math.round(moveSeconds * fps));
  let cam = { x: mv[0].x, y: mv[0].y, scale: mv[0].scale };
  for (let i = 1; i < mv.length; i++) {
    const start = at(mv[i].at);
    if (frame < start) break;
    const t = interpolate(frame, [start, start + mf], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
    const f = mv[i - 1];
    cam = { x: f.x + (mv[i].x - f.x) * t, y: f.y + (mv[i].y - f.y) * t, scale: f.scale + (mv[i].scale - f.scale) * t };
  }
  const imgW = PW * cam.scale, imgH = PH * cam.scale;
  const tx = clamp(WIN.width / 2 - cam.x * imgW, WIN.width - imgW, 0);
  const ty = clamp(WIN.height / 2 - cam.y * imgH, WIN.height - imgH, 0);

  // highlights --------------------------------------------------------------------------------------------
  const hs = [...highlights].sort((a, b) => a.at - b.at);
  const boxHs = hs.filter((h) => h.kind === 'glow' || h.kind === 'ring');
  const selHs = hs.filter((h) => h.kind === 'select');
  const markHs = hs.filter((h) => h.kind === 'mark');
  const boxLayer = boxHs.map((h, i) => {
    const start = at(h.at);
    const inP = sp(start);
    const next = boxHs[i + 1];
    // a ring persists; a glow gives way to the next box highlight
    const outP = h.kind === 'ring' || !next ? 0 : clamp((frame - at(next.at)) / 6, 0, 1);
    const r = RECT[h.target];
    const o = inP * (1 - outP);
    const ring = h.kind === 'ring';
    const pad = ring ? 10 : 0;
    return (
      <div key={`b${i}`} style={{ position: 'absolute', left: r.x - pad, top: r.y - pad, width: r.w + pad * 2, height: r.h + pad * 2,
                                  borderRadius: ring ? 18 : 12, border: `${ring ? 8 : 5}px solid ${CLAUDE.SPARK}`,
                                  background: ring ? 'transparent' : 'rgba(217,119,87,0.12)', opacity: o,
                                  transform: `scale(${0.96 + 0.04 * inP})` }} />
    );
  });
  const selected = (() => { let s = ''; selHs.forEach((h) => { if (frame >= at(h.at)) s = h.target; }); return s; })();
  const selStart = (() => { let s = 0; selHs.forEach((h) => { if (frame >= at(h.at)) s = at(h.at); }); return s; })();
  const markP = (t: 'p1' | 'p2') => { const h = markHs.find((m) => m.target === t); return h ? clamp((frame - at(h.at)) / 18, 0, 1) : 0; };
  const mk = (p: number): React.CSSProperties => ({
    backgroundImage: 'linear-gradient(rgba(217,119,87,0.38), rgba(217,119,87,0.38))', backgroundRepeat: 'no-repeat',
    backgroundSize: `${Math.round(p * 100)}% 100%`, backgroundPosition: '0 0', padding: '2px 0', fontWeight: 600,
  });

  const radio = (key: 'radio1' | 'radio2', y: number, textLine: string) => {
    const on = selected === key;
    const p = on ? sp(selStart) : 0;
    return (
      <div key={key} style={{ position: 'absolute', left: MAIN_X, top: y, width: 1190, height: 96, display: 'flex', alignItems: 'flex-start',
                              background: on ? 'rgba(217,119,87,0.10)' : 'transparent', borderRadius: 12, padding: '6px 10px' }}>
        <div style={{ width: 38, height: 38, borderRadius: 19, border: `4px solid ${on ? CLAUDE.SPARK : '#6E6E6E'}`, marginTop: 6, marginRight: 22,
                      flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#FFFFFF' }}>
          {on ? <div style={{ width: 20, height: 20, borderRadius: 10, background: CLAUDE.SPARK, transform: `scale(${p})` }} /> : null}
        </div>
        <div style={{ fontFamily: CLAUDE_FONT.ui, fontSize: 30, lineHeight: '42px', color: INK, flex: 1 }}>{textLine}</div>
      </div>
    );
  };

  // link and the closing fade ---------------------------------------------------------------------------------
  const linkP = linkAt === undefined ? 1 : sp(at(linkAt));
  const contP = continuesAt === undefined ? 0 : sp(at(continuesAt));
  const bob = Math.sin(frame / 7) * 8;

  return (
    <AbsoluteFill style={{ backgroundColor: CLAUDE.PAGE }}>
      <div style={{ position: 'absolute', left: WIN.left, top: WIN.top, width: WIN.width, height: WIN.height, background: '#FFFFFF',
                    border: `2px solid ${CLAUDE.INK}`, borderRadius: 16, overflow: 'hidden', boxShadow: '0 14px 44px rgba(61,57,41,0.16)',
                    opacity: winIn, transform: `translateY(${(1 - winIn) * 14}px)` }}>
        <div style={{ position: 'absolute', left: tx, top: ty, width: PW, height: PH, transform: `scale(${cam.scale})`, transformOrigin: '0 0' }}>
          {/* top bar */}
          <div style={{ position: 'absolute', left: 0, top: 0, width: PW, height: 80, background: TOP, display: 'flex', alignItems: 'center', boxShadow: '0 3px 6px rgba(0,0,0,0.22)', zIndex: 2 }}>
            <span style={{ marginLeft: 40, fontFamily: CLAUDE_FONT.ui, fontSize: 38, fontWeight: 800, color: '#111111', letterSpacing: 0 }}>{topBarLabel}</span>
          </div>
          {/* left menu */}
          <div style={{ position: 'absolute', left: 0, top: 80, width: 360, height: PH - 80, background: '#F4F4F4', borderRight: '2px solid #DADADA' }}>
            {MENU.map((m, i) => (
              <div key={m} style={{ position: 'absolute', left: 0, top: 24 + i * 74, width: 358, height: 62, background: '#EAEEF1', display: 'flex', alignItems: 'center', whiteSpace: 'nowrap', fontFamily: CLAUDE_FONT.ui, fontSize: 26, color: INK }}>
                {MENU_PLUS.has(m) ? <span style={{ marginLeft: 24, marginRight: 12, width: 20, height: 20, border: `2px solid ${INK}`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, lineHeight: '16px' }}>+</span> : <span style={{ marginLeft: 24 }} />}
                {m}
              </div>
            ))}
          </div>
          {/* heading */}
          <div style={{ position: 'absolute', left: MAIN_X, top: 120, fontFamily: CLAUDE_FONT.ui, fontSize: 48, fontWeight: 700, color: INK }}>Requester Information</div>
          {/* the six fields (values are placeholders) */}
          <Field x={COL1} y={ROW_Y[0]} label="Requester" ph="Last, First" />
          <Field x={COL2} y={ROW_Y[0]} label="Phone" ph="" />
          <Field x={COL1} y={ROW_Y[1]} label="Email" ph="you@northeastern.edu" />
          <Field x={COL2} y={ROW_Y[1]} label="Location" ph="your campus" drop />
          <Field x={COL1} y={ROW_Y[2]} label="UserID" ph="your user ID" />
          <Field x={COL2} y={ROW_Y[2]} label="Department" ph="your department" drop />
          {/* the one required choice */}
          <div style={{ position: 'absolute', left: MAIN_X, top: 636, fontFamily: CLAUDE_FONT.ui, fontSize: 34, fontWeight: 700, color: INK }}>
            Please choose one:<span style={{ color: '#B3261E' }}> *</span>
          </div>
          {radio('radio1', 702, 'I do not have access to the High Performance Computer (HPC) cluster. I am requesting a new account.')}
          {radio('radio2', 822, 'I already have access to the High Performance Computer (HPC) cluster. I need to update my sponsor information.')}
          {/* the two instruction paragraphs */}
          <div style={{ position: 'absolute', left: MAIN_X, top: 960, width: 1190, fontFamily: CLAUDE_FONT.ui, fontSize: 30, lineHeight: '42px', color: INK }}>
            To have access to the HPC environment, all users must belong to a{' '}
            <span style={mk(markP('p1'))}>sponsor-owned storage space</span>. If the sponsor does not have a storage space, they can request one{' '}
            <span style={{ color: '#0B57D0', textDecoration: 'underline' }}>here</span>.
          </div>
          <div style={{ position: 'absolute', left: MAIN_X, top: 1116, width: 1190, fontFamily: CLAUDE_FONT.ui, fontSize: 30, lineHeight: '42px', color: INK }}>
            Alternatively, if a storage space already exists,{' '}
            <span style={mk(markP('p2'))}>its owner can add members</span> to the cluster themselves, following the{' '}
            <span style={{ color: '#0B57D0', textDecoration: 'underline' }}>documentation</span>.
          </div>
          {/* highlights sit above the page content */}
          {boxLayer}
          {/* the page ends here: nothing is drawn below the paragraphs; this fade is the card's edge */}
          <div style={{ position: 'absolute', left: 0, top: 1250, width: PW, height: PH - 1250, background: 'linear-gradient(rgba(255,255,255,0), #FFFFFF 85%)' }} />
        </div>
        {/* "the form continues" cue */}
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 330, opacity: contP,
                      background: 'linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0.97) 70%)' }} />
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 34, textAlign: 'center', opacity: contP }}>
          <div style={{ fontFamily: CLAUDE_FONT.serif, fontSize: 50, fontWeight: 600, color: CLAUDE.INK }}>The form continues</div>
          <div style={{ marginTop: 6, color: CLAUDE.SPARK, fontSize: 56, transform: `translateY(${bob}px)`, lineHeight: 1 }}>⌄</div>
        </div>
      </div>
      {/* caption row: where the form lives, and what the values are */}
      <div style={{ position: 'absolute', left: WIN.left, right: WIN.left, top: WIN.top + WIN.height + 40, display: 'flex', justifyContent: 'space-between',
                    alignItems: 'baseline' }}>
        <div style={{ fontFamily: CLAUDE_FONT.mono, fontSize: 34, color: CLAUDE.INK, opacity: linkP, position: 'relative' }}>
          {link}
          <div style={{ position: 'absolute', left: 0, bottom: -10, height: 6, width: `${Math.round(linkP * 100)}%`, background: CLAUDE.SPARK, borderRadius: 3 }} />
        </div>
        <div style={{ fontFamily: CLAUDE_FONT.serif, fontStyle: 'italic', fontSize: 32, color: CLAUDE.INK_SOFT }}>Placeholder values; your own details fill these</div>
      </div>
    </AbsoluteFill>
  );
};

export const accessFormCardDefaultProps: AccessFormCardProps = accessFormCardSchema.parse({});
