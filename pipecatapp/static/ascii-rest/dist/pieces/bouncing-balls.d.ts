import type { Frame } from "../types.ts";
export interface BouncingBallsOptions {
    [key: string]: unknown;
    balls: number;
}
export declare const meta: {
    name: string;
    category: "physics";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        balls: number;
    };
};
export default function bouncingBalls({ balls }?: Partial<BouncingBallsOptions>): Frame;
