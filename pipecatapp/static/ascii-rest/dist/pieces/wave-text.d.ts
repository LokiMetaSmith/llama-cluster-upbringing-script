import type { Frame } from "../types.ts";
export interface WaveTextOptions {
    [key: string]: unknown;
    text: string;
    amp: number;
    wavelength: number;
    speed: number;
    spacing: number;
    settle: boolean;
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        text: string;
        amp: number;
        wavelength: number;
        speed: number;
        spacing: number;
        settle: true;
    };
};
export default function waveText({ text, amp, // rows from the level line to a crest
wavelength, // letters from crest to crest
speed, // letters a second the swell travels
spacing, // blank columns between letters
settle, }?: Partial<WaveTextOptions>): Frame;
