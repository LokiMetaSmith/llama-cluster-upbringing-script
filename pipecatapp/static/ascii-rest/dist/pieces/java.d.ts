import type { Frame } from "../types.ts";
export interface JavaOptions {
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
export default function java({ shine }?: Partial<JavaOptions>): Frame;
