import type { Frame } from "../types.ts";
export interface FirefliesOptions {
    [key: string]: unknown;
    seed: number;
    count: number;
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
        count: number;
    };
};
export default function fireflies({ seed, count }?: Partial<FirefliesOptions>): Frame;
