import type { Frame } from "../types.ts";
export interface WaveInterferenceOptions {
    [key: string]: unknown;
    wavelength: number;
    separation: number;
}
export declare const meta: {
    name: string;
    category: "physics";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        wavelength: number;
        separation: number;
    };
};
export default function waveInterference({ wavelength, separation }?: Partial<WaveInterferenceOptions>): Frame;
