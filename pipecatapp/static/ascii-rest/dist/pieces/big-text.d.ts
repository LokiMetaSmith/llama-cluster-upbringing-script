import type { Frame } from "../types.ts";
export interface BigTextOptions {
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
export default function bigText({ text }?: Partial<BigTextOptions>): Frame;
