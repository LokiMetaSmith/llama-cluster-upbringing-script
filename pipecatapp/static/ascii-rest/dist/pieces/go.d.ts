import type { Frame } from "../types.ts";
export interface GoOptions {
    [key: string]: unknown;
    /** Seconds between glints; 0 keeps the logo still. */
    shine: number;
}
export declare const meta: {
    name: string;
    category: "logos";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        shine: number;
    };
    palette: string[];
};
export default function go({ shine }?: Partial<GoOptions>): Frame;
