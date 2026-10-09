import type { Frame } from "../types.ts";
export interface MarqueeOptions {
    [key: string]: unknown;
    text: string;
    speed: number;
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
        speed: number;
    };
};
export default function marquee({ text, speed }?: Partial<MarqueeOptions>): Frame;
