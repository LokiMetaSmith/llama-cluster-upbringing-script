import type { Frame } from "../types.ts";
export interface TypewriterOptions {
    [key: string]: unknown;
    /** Typed before every phrase and never deleted. */
    prefix: string;
    phrases: string[];
}
export declare const meta: {
    name: string;
    category: "type";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        prefix: string;
        phrases: string[];
    };
};
export default function typewriter({ prefix, phrases }?: Partial<TypewriterOptions>): Frame;
