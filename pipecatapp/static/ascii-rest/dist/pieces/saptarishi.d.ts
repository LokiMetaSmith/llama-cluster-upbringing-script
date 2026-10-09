import type { Frame } from "../types.ts";
export interface SaptarishiOptions {
    [key: string]: unknown;
    lines: boolean;
}
export declare const meta: {
    name: string;
    category: "space";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        lines: true;
    };
};
export default function saptarishi({ lines }?: Partial<SaptarishiOptions>): Frame;
