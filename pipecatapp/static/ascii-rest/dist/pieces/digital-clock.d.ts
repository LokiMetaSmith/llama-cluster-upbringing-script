import type { Frame } from "../types.ts";
export interface DigitalClockOptions {
    [key: string]: unknown;
    hour12: boolean;
    seconds: boolean;
    date: boolean;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        hour12: false;
        seconds: true;
        date: true;
    };
    clock: true;
};
export default function digitalClock({ hour12, seconds, date }?: Partial<DigitalClockOptions>): Frame;
