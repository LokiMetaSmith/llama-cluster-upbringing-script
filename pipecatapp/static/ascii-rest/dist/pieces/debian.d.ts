import type { Frame } from "../types.ts";
export interface DebianOptions {
    [key: string]: unknown;
    /** Seconds between scans; 0 keeps the logo still. */
    scan: number;
}
export declare const meta: {
    name: string;
    category: "distros";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        scan: number;
    };
    palette: string[];
};
export default function debian({ scan }?: Partial<DebianOptions>): Frame;
