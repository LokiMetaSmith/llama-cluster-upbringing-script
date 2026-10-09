import type { Frame } from "../types.ts";
export interface CpuMetersOptions {
    [key: string]: unknown;
    commands: string[];
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        commands: string[];
    };
};
export default function cpuMeters({ commands }?: Partial<CpuMetersOptions>): Frame;
