import type { Frame } from "../types.ts";
export interface StarfieldOptions {
    [key: string]: unknown;
    stars: number;
    speed: number;
}
export declare const meta: {
    name: string;
    category: "space";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        stars: number;
        speed: number;
    };
};
export default function starfield({ stars, speed }?: Partial<StarfieldOptions>): Frame;
