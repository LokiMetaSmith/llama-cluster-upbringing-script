import type { Frame } from "../types.ts";
export interface BarChartDataset {
    name: string;
    values: number[];
}
export interface BarChartOptions {
    [key: string]: unknown;
    title: string;
    labels: string[];
    datasets: BarChartDataset[];
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        title: string;
        labels: string[];
        datasets: {
            name: string;
            values: number[];
        }[];
    };
};
export default function barChart({ title, labels, datasets, }?: Partial<BarChartOptions>): Frame;
