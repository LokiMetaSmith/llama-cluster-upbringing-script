import type { Frame } from "../types.ts";
export interface TerminalOptions {
    [key: string]: unknown;
    prompt: string;
    title: string;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        prompt: string;
        title: string;
    };
};
export default function terminal({ prompt, title }?: Partial<TerminalOptions>): Frame;
