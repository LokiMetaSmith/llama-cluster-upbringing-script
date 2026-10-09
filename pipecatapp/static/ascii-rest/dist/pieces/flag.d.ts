import type { Frame } from "../types.ts";
export interface FlagOptions {
    [key: string]: unknown;
    stripes: number;
}
export declare const meta: {
    name: string;
    category: "physics";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        stripes: number;
    };
};
export default function flag({ stripes }?: Partial<FlagOptions>): Frame;
