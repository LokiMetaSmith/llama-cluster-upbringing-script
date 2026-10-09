export const meta = {
    name: "scramble",
    category: "type",
    note: "phrases decoding left to right out of flickering glyphs",
    cols: 44,
    rows: 3,
    fps: 20,
    options: { phrases: ["hello, world", "decoding the signal", "nothing is lost", "see you on the other side"] },
};
const GLYPHS = "!<>-_\\/[]{}=+*^?#%&$@0123456789abcdefxyz";
const OUT = 0.022; // seconds between columns breaking up
const IN = 0.05; // seconds between columns settling
const LEAD = 0.32; // seconds of pure noise before the first column settles
const HOLD = 1.9; // seconds a settled phrase stays
function mulberry32(a) {
    return () => {
        a = (a + 0x6d2b79f5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
}
export default function scramble({ phrases = meta.options.phrases } = {}) {
    const { cols, rows } = meta;
    const list = (phrases.length ? phrases : [""]).map((p) => String(p).slice(0, cols - 4));
    const rand = mulberry32(77);
    const placed = list.map((p) => ({ text: p, x: Math.floor((cols - p.length) / 2) }));
    // One transition per phrase, into it from the one before: when each column
    // breaks up and when it settles, with a little jitter so the front is ragged.
    let at = 0;
    const steps = placed.map((to, i) => {
        const from = placed[(i + placed.length - 1) % placed.length];
        const lo = Math.min(from.x, to.x);
        const hi = Math.max(from.x + from.text.length, to.x + to.text.length);
        const out = [], settle = [];
        for (let c = lo; c < hi; c++) {
            out.push(at + (c - lo) * OUT + rand() * 0.06);
            settle.push(at + LEAD + (c - lo) * IN + rand() * 0.14);
        }
        const s = { from, to, lo, hi, out, settle, start: at };
        at = Math.max(at + LEAD, ...settle) + HOLD;
        s.end = at;
        return s;
    });
    const period = at;
    // Frame 0 holds the first phrase, settled, just before it breaks up.
    const offset = steps[0].end - 0.7;
    const charAt = (p, c) => (c >= p.x && c < p.x + p.text.length ? p.text[c - p.x] : " ");
    return (t) => {
        const now = (((t + offset) % period) + period) % period;
        const s = steps.find((st) => now < st.end) || steps[0];
        const tick = Math.floor(now * 20);
        const line = new Array(cols).fill(" ");
        for (let c = 0; c < cols; c++) {
            if (c < s.lo || c >= s.hi)
                continue;
            const k = c - s.lo;
            const a = charAt(s.from, c), b = charAt(s.to, c);
            if (now < s.out[k])
                line[c] = a;
            else if (now >= s.settle[k])
                line[c] = b;
            else if (a === " " && b === " " && now < s.out[k] + 0.12)
                line[c] = " ";
            else {
                // A new glyph for this column on every tick, the same in every instance.
                let h = Math.imul(c ^ Math.imul(tick, 0x27d4eb2d), 0x9e3779b1);
                h = Math.imul(h ^ (h >>> 15), 0x85ebca77);
                line[c] = GLYPHS[((h ^ (h >>> 13)) >>> 0) % GLYPHS.length];
            }
        }
        const lines = [];
        for (let r = 0; r < rows; r++)
            lines.push(r === rows >> 1 ? line.join("") : " ".repeat(cols));
        return lines.join("\n");
    };
}
