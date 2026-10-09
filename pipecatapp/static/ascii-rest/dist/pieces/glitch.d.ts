import type { Frame } from "../types.ts";
export interface GlitchOptions {
    [key: string]: unknown;
    text: string;
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        text: string;
    };
};
export default function glitch({ text }?: Partial<GlitchOptions>): Frame;
