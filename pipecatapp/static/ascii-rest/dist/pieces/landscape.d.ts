import type { Frame } from "../types.ts";
export interface LandscapeOptions {
    [key: string]: unknown;
    /** The hour of the day, 0 to 24; null for the local time. */
    hour: number | null;
    /** The moon's age in lunations, 0 to 1; null for its real phase now. */
    phase: number | null;
}
export declare const meta: {
    name: string;
    category: "nature";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        hour: null;
        phase: null;
    };
    clock: true;
};
export default function landscape({ hour, phase }?: Partial<LandscapeOptions>): Frame;
