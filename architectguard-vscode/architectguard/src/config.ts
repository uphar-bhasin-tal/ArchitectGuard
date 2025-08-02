import * as vscode from 'vscode';

export interface ArchitectGuardConfig {
    openaiApiKey: string;
    maxFilesToAnalyze: number;
}

export function getConfig(): ArchitectGuardConfig {
    const config = vscode.workspace.getConfiguration('architectguard');
    return {
        openaiApiKey: config.get('openaiApiKey') || '',
        maxFilesToAnalyze: config.get('maxFilesToAnalyze') || 100
    };
}