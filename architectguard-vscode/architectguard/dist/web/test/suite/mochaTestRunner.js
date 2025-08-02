"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.run = run;
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
//# sourceMappingURL=mochaTestRunner.js.map