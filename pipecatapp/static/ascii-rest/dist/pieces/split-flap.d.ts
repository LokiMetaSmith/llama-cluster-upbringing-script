import type { Frame } from "../types.ts";
export interface SplitFlapOptions {
    [key: string]: unknown;
    title: string;
    start: string;
    flights: [time: string, destination: string, gate: string, remark: string][];
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        title: string;
        start: string;
        flights: [string, string, string, string][];
    };
};
export default function splitFlap({ title, start, flights }?: Partial<SplitFlapOptions>): Frame;
