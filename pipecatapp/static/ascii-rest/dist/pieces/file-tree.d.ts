import type { Frame } from "../types.ts";
export interface FileTreeOptions {
    [key: string]: unknown;
    /** The first line, above the listing. */
    root: string;
    /** One entry per line, two spaces of indent per level, folders end in "/". */
    entries: string;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        root: string;
        entries: string;
    };
};
export default function fileTree({ root: label, entries }?: Partial<FileTreeOptions>): Frame;
