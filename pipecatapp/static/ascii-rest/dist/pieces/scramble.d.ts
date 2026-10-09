import type { Frame } from "../types.ts";
export interface ScrambleOptions {
    [key: string]: unknown;
    phrases: string[];
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        phrases: string[];
    };
};
export default function scramble({ phrases }?: Partial<ScrambleOptions>): Frame;
