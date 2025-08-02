"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReviewPanel = void 0;
const vscode = require("vscode");
class ReviewPanel {
    constructor(panel) {
        this._disposables = [];
        this._panel = panel;
        this._update();
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }
    static createOrShow(extensionUri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        if (ReviewPanel.currentPanel) {
            ReviewPanel.currentPanel._panel.reveal(column);
            return;
        }
        const panel = vscode.window.createWebviewPanel('architectguardReview', 'Architectural Review', column || vscode.ViewColumn.One, {
            enableScripts: true,
            localResourceRoots: [extensionUri]
        });
        ReviewPanel.currentPanel = new ReviewPanel(panel);
    }
    _update() {
        const webview = this._panel.webview;
        this._panel.webview.html = this._getHtmlForWebview(webview);
    }
    _getHtmlForWebview(webview) {
        return `<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Architectural Review</title>
            </head>
            <body>
                <h1>Architectural Review Results</h1>
                <div id="results"></div>
            </body>
            </html>`;
    }
    dispose() {
        ReviewPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }
}
exports.ReviewPanel = ReviewPanel;
//# sourceMappingURL=reviewPanel.js.map