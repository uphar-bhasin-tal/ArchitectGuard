"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const path = require("path");
const child_process_1 = require("child_process");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
// export function activate(context: vscode.ExtensionContext) {
// 	// Use the console to output diagnostic information (console.log) and errors (console.error)
// 	// This line of code will only be executed once when your extension is activated
// 	console.log('Congratulations, your extension "ArchitecturalReviewGaurd" is now active in the web extension host!');
// 	// The command has been defined in the package.json file
// 	// Now provide the implementation of the command with registerCommand
// 	// The commandId parameter must match the command field in package.json
// 	const disposable = vscode.commands.registerCommand('ArchitecturalReviewGaurd.helloWorld', () => {
// 		// The code you place here will be executed every time your command is executed
// 		// Display a message box to the user
// 		vscode.window.showInformationMessage('Hello World from architectguard in a web extension host!');
// 	});
// 	context.subscriptions.push(disposable);
// }
// // This method is called when your extension is deactivated
// export function deactivate() {}
function activate(context) {
    let disposable = vscode.commands.registerCommand('architectguard.reviewArchitecture', async () => {
        try {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (!workspaceFolders) {
                vscode.window.showErrorMessage('No workspace folder open');
                return;
            }
            const projectRoot = workspaceFolders[0].uri.fsPath;
            // Show progress indicator
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Running Architectural Review",
                cancellable: true
            }, async (progress) => {
                progress.report({ message: "Analyzing project architecture..." });
                // Run the Python script
                try {
                    (0, child_process_1.execSync)(`python ${path.join(projectRoot, 'arc_lint.py')} --project-root ${projectRoot}`, {
                        cwd: projectRoot
                    });
                    // Read and display the results
                    const reviewPath = path.join(projectRoot, 'architectural_review.md');
                    const doc = await vscode.workspace.openTextDocument(reviewPath);
                    await vscode.window.showTextDocument(doc);
                }
                catch (error) {
                    vscode.window.showErrorMessage(`Error running architectural review: ${error}`);
                }
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to run architectural review: ${error}`);
        }
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map