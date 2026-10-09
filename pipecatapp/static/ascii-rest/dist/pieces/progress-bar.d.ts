import type { Frame } from "../types.ts";
export interface ProgressBarOptions {
    [key: string]: unknown;
    labels: string[];
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        labels: string[];
    };
};
export default function progressBar({ labels }?: Partial<ProgressBarOptions>): Frame;
