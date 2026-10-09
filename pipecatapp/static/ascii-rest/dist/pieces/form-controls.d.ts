import type { Frame } from "../types.ts";
export interface FormControlsOptions {
    [key: string]: unknown;
    title: string;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        title: string;
    };
};
export default function formControls({ title }?: Partial<FormControlsOptions>): Frame;
