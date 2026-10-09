import type { Frame } from "../types.ts";
export interface NewtonsCradleOptions {
    [key: string]: unknown;
    lifted: number;
}
export declare const meta: {
    name: string;
    category: "physics";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        lifted: number;
    };
};
export default function newtonsCradle({ lifted }?: Partial<NewtonsCradleOptions>): Frame;
