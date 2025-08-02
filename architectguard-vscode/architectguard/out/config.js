"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getConfig = void 0;
const vscode = require("vscode");
function getConfig() {
    const config = vscode.workspace.getConfiguration('architectguard');
    return {
        openaiApiKey: config.get('openaiApiKey') || '',
        maxFilesToAnalyze: config.get('maxFilesToAnalyze') || 100
    };
}
exports.getConfig = getConfig;
//# sourceMappingURL=config.js.map