import type { Frame } from "../types.ts";
export interface SolarSystemOptions {
    [key: string]: unknown;
    /** How fast the planets go round: 1 is the innermost orbit in three seconds. */
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
        speed: number;
    };
};
export default function solarSystem({ speed }?: Partial<SolarSystemOptions>): Frame;
