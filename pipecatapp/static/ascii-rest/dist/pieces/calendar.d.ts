import type { Frame } from "../types.ts";
export interface CalendarOptions {
    [key: string]: unknown;
    monday: boolean;
    time: boolean;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        monday: false;
        time: true;
    };
    clock: true;
};
export default function calendar({ monday, time }?: Partial<CalendarOptions>): Frame;
