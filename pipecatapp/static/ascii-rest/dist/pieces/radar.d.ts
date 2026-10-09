import type { Frame } from "../types.ts";
export interface RadarOptions {
    [key: string]: unknown;
    /** The scope's range, printed in the corner; the rings are a third of it apart. */
    range: number;
    unit: string;
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        range: number;
        unit: string;
    };
};
export default function radar({ range, unit }?: Partial<RadarOptions>): Frame;
