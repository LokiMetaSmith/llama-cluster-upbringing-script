import type { Frame } from "../types.ts";
export interface DividersOptions {
    [key: string]: unknown;
    width: number;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        width: number;
    };
};
export default function dividers({ width }?: Partial<DividersOptions>): Frame;
