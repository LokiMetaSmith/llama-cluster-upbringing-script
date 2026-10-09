import type { Frame } from "../types.ts";
export interface HeatmapOptions {
    [key: string]: unknown;
    unit: string;
    seed: number;
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        unit: string;
        seed: number;
    };
};
export default function heatmap({ unit, seed }?: Partial<HeatmapOptions>): Frame;
