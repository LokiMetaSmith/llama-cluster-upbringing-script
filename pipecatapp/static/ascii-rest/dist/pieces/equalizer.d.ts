import type { Frame } from "../types.ts";
export interface EqualizerOptions {
    [key: string]: unknown;
    /** Tempo, held to 60 to 180. */
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
export default function equalizer({ bpm }?: Partial<EqualizerOptions>): Frame;
