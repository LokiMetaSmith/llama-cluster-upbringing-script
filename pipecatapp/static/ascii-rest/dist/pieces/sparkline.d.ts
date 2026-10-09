import type { Frame } from "../types.ts";
export interface SparklineSeries {
    label?: string;
    unit?: string;
    lo?: number;
    hi?: number;
    digits?: number;
    format?: (v: number) => unknown;
    values?: ArrayLike<number>;
}
export interface SparklineOptions {
    [key: string]: unknown;
    series: SparklineSeries[];
    range: boolean;
    rate: number;
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        series: ({
            label: string;
            unit: string;
            lo: number;
            hi: number;
            digits?: undefined;
        } | {
            label: string;
            unit: string;
            lo: number;
            hi: number;
            digits: number;
        })[];
        range: true;
        rate: number;
    };
};
export default function sparkline({ series, range, rate, }?: Partial<SparklineOptions>): Frame;
