"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.run = void 0;
// Imports mocha for the browser, defining the `mocha` global.
require("mocha/mocha");
mocha.setup({
    ui: 'tdd',
    reporter: undefined
});
function run() {
    return new Promise((c, e) => {
        try {
            // Run the mocha test
            mocha.run(failures => {
                if (failures > 0) {
                    e(new Error(`${failures} tests failed.`));
                }
                else {
                    c();
                }
            });
        }
        catch (err) {
            console.error(err);
            e(err);
        }
    });
}
exports.run = run;
//# sourceMappingURL=mochaTestRunner.js.map