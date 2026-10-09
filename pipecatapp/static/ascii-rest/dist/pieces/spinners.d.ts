import type { Frame } from "../types.ts";
export interface SpinnersOptions {
    [key: string]: unknown;
    /** Spinners to show, in this order; empty for all twelve. */
    names: string[];
    labels: boolean;
    speed: number;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        names: never[];
        labels: true;
        speed: number;
    };
};
export default function spinners({ names, labels, speed }?: Partial<SpinnersOptions>): Frame;
