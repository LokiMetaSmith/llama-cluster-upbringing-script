import type { Frame } from "../types.ts";
export interface CandlesticksOptions {
    [key: string]: unknown;
    start: number;
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
        start: number;
        seed: number;
    };
};
export default function candlesticks({ start, seed }?: Partial<CandlesticksOptions>): Frame;
