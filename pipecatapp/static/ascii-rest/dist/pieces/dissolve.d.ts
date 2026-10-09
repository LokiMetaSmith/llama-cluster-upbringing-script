import type { Frame } from "../types.ts";
export interface DissolveOptions {
    [key: string]: unknown;
    /** A list of words, or one string of them split at commas and spaces. */
    words: string[] | string;
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        words: string[];
    };
};
export default function dissolve({ words }?: Partial<DissolveOptions>): Frame;
