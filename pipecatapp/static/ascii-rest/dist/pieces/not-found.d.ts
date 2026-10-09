import type { Frame } from "../types.ts";
export interface NotFoundOptions {
    [key: string]: unknown;
    code: string;
    title: string;
    message: string;
}
export declare const meta: {
    name: string;
    category: "ui";
    note: string;
    cols: number;
    rows: number;
    fps: number;
    options: {
        code: string;
        title: string;
        message: string;
    };
};
export default function notFound({ code, title, message, }?: Partial<NotFoundOptions>): Frame;
