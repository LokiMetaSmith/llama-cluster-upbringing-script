import type { Frame } from "../types.ts";
export interface TvStaticOptions {
    [key: string]: unknown;
    set: boolean;
}
export declare const meta: {
    name: string;
    category: "effects";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        set: true;
    };
};
export default function tvStatic({ set }?: Partial<TvStaticOptions>): Frame;
