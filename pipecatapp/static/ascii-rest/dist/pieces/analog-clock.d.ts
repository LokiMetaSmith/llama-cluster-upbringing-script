import type { Frame } from "../types.ts";
export interface AnalogClockOptions {
    [key: string]: unknown;
    numerals: boolean;
    seconds: boolean;
}
export declare const meta: {
    name: string;
    category: "objects";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        numerals: true;
        seconds: true;
    };
    clock: true;
};
export default function analogClock({ numerals, seconds }?: Partial<AnalogClockOptions>): Frame;
