const ENTRIES = [
    "docs/",
    "  guide.md",
    "  notes.md",
    "public/",
    "  favicon.ico",
    "  robots.txt",
    "src/",
    "  components/",
    "    button.ts",
    "    card.ts",
    "    menu.ts",
    "  lib/",
    "    fetch.ts",
    "    format.ts",
    "  index.ts",
    "  styles.css",
    "tests/",
    "  format.test.ts",
    "package.json",
    "README.md",
].join("\n");
export const meta = {
    name: "file tree",
    category: "ui",
    note: "a tree listing opened folder by folder, then closed again",
    cols: 36,
    rows: 23,
    fps: 15,
    options: { root: ".", entries: ENTRIES },
};
const MOVE = 0.13; // seconds per line the cursor steps
const PAUSE = 0.3; // on a folder before it opens or closes
const REVEAL = 0.07; // per line appearing or going
const HOLD = 1.8; // all open
const REST = 0.7; // all closed, held at both ends of the loop
// One entry per line, two spaces of indent per level, folders end in "/".
function parse(text) {
    const root = { kids: [] };
    const stack = [root];
    for (const raw of String(text).split("\n")) {
        const name = raw.trim();
        if (!name)
            continue;
        const depth = Math.floor((raw.length - raw.trimStart().length) / 2);
        const node = { name, dir: name.endsWith("/"), kids: [] };
        stack.length = Math.min(stack.length, depth + 1);
        stack[stack.length - 1].kids.push(node);
        if (node.dir)
            stack.push(node);
    }
    return root;
}
export default function fileTree({ root: label = ".", entries = ENTRIES } = {}) {
    const { cols, rows } = meta;
    const root = parse(entries);
    const dirs = [];
    let nd = 0, nf = 0;
    const collect = (n) => n.kids.forEach((k) => {
        k.dir ? nd++ : nf++;
        if (k.dir && k.kids.length)
            dirs.push(k);
        collect(k);
    });
    collect(root);
    // Counted over the whole tree, as tree itself does, not just what is open.
    const summary = `${nd} director${nd === 1 ? "y" : "ies"}, ${nf} file${nf === 1 ? "" : "s"}`;
    const shown = new Map(); // folder to how many of its entries are listed
    shown.set(root, root.kids.length);
    let cursor = dirs[0] || root.kids[0];
    // The lines on screen: the folders' entries in order, cut short where a
    // folder is closed or still opening. A closed folder that holds something
    // wears a "+", and the cursor is the branch turning into an arrow.
    const listing = () => {
        const out = [];
        const walk = (node, prefix) => {
            const n = shown.get(node) || 0;
            for (let i = 0; i < n; i++) {
                const kid = node.kids[i], last = i === node.kids.length - 1;
                const branch = (last ? "└─" : "├─") + (kid === cursor ? "> " : "─ ");
                const closed = kid.dir && kid.kids.length && !shown.get(kid);
                out.push({ node: kid, text: prefix + branch + kid.name + (closed ? " +" : "") });
                if (kid.dir)
                    walk(kid, prefix + (last ? "    " : "│   "));
            }
        };
        walk(root, "");
        return out;
    };
    // Centre the listing as it stands fully open, with room for the marker.
    dirs.forEach((d) => shown.set(d, d.kids.length));
    const width = Math.max(label.length, summary.length, ...listing().map((l) => l.text.length + 2));
    dirs.forEach((d) => shown.set(d, 0));
    const pad = " ".repeat(Math.max(0, Math.floor((cols - width) / 2)));
    // The tree grows down from the top; the count stays on the last row.
    const render = () => {
        const lines = [label, ...listing().map((v) => v.text)].slice(0, rows - 2);
        while (lines.length < rows - 1)
            lines.push("");
        lines.push(summary);
        return lines.map((s) => (pad + s).padEnd(cols).slice(0, cols)).join("\n");
    };
    // The whole loop as a list of pictures and how long each stays up.
    const snaps = [];
    let total = 0, start = 0;
    const snap = (dur) => {
        snaps.push({ at: total, text: render() });
        total += dur;
    };
    const step = (dir) => {
        const vis = listing();
        const i = vis.findIndex((v) => v.node === cursor);
        cursor = vis[i + dir].node;
        snap(MOVE);
    };
    const walkTo = (node) => {
        const vis = listing();
        const dir = vis.findIndex((v) => v.node === node) > vis.findIndex((v) => v.node === cursor) ? 1 : -1;
        while (cursor !== node)
            step(dir);
    };
    snap(REST);
    dirs.forEach((node, i) => {
        walkTo(node);
        snap(PAUSE);
        for (let k = 1; k <= node.kids.length; k++)
            (shown.set(node, k), snap(REVEAL));
        if (i + 1 === Math.ceil(dirs.length * 0.6))
            start = total;
    });
    snap(HOLD);
    for (let i = dirs.length - 1; i >= 0; i--) {
        const node = dirs[i];
        walkTo(node);
        snap(PAUSE);
        for (let k = node.kids.length - 1; k >= 0; k--)
            (shown.set(node, k), snap(REVEAL));
    }
    total += REST; // the last picture is the first one, so the loop closes on it
    return (t) => {
        const p = (t + start) % total;
        let i = 0;
        while (i + 1 < snaps.length && snaps[i + 1].at <= p)
            i++;
        return snaps[i].text;
    };
}
