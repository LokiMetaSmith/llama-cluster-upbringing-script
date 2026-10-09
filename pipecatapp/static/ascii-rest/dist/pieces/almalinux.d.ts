import type { Frame } from "../types.ts";
export interface AlmalinuxOptions {
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
export default function almalinux({ scan }?: Partial<AlmalinuxOptions>): Frame;
