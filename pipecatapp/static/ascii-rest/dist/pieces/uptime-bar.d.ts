import type { Frame } from "../types.ts";
export interface UptimeBarOptions {
    [key: string]: unknown;
    services: string[];
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        services: string[];
    };
};
export default function uptimeBar({ services }?: Partial<UptimeBarOptions>): Frame;
