import type { Frame } from "../types.ts";
export interface GreptileOptions {
    [key: string]: unknown;
    /** Seconds between glints; 0 keeps the logo still. */
    shine: number;
}
export declare const meta: {
    name: string;
    category: "companies";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        shine: number;
    };
    palette: string[];
};
export default function greptile({ shine }?: Partial<GreptileOptions>): Frame;
