import type { Frame } from "../types.ts";
export interface HeartbeatOptions {
    [key: string]: unknown;
    /** The resting rate, held to 30 to 199. */
    bpm: number;
}
export declare const meta: {
    name: string;
    category: "data";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        bpm: number;
    };
};
export default function heartbeat({ bpm }?: Partial<HeartbeatOptions>): Frame;
