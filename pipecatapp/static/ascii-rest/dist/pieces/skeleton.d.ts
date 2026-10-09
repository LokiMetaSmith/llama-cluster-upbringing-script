import type { Frame } from "../types.ts";
export interface SkeletonOptions {
    [key: string]: unknown;
    lines: number;
    image: boolean;
    avatar: boolean;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        lines: number;
        image: true;
        avatar: true;
    };
};
export default function skeleton({ lines, image, avatar }?: Partial<SkeletonOptions>): Frame;
