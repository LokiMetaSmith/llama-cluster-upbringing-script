import type { Frame } from "../types.ts";
export interface GaugeOptions {
    [key: string]: unknown;
    label: string;
    unit: string;
    min: number;
    max: number;
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        label: string;
        unit: string;
        min: number;
        max: number;
    };
};
export default function gauge({ label, unit, min, max }?: Partial<GaugeOptions>): Frame;
