import type { Frame } from "../types.ts";
export interface FractalTreeOptions {
    [key: string]: unknown;
    seed: number;
}
export declare const meta: {
    name: string;
    category: "nature";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        seed: number;
    };
};
export default function fractalTree({ seed }?: Partial<FractalTreeOptions>): Frame;
