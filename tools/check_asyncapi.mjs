// Checks an AsyncAPI file with the official parser. tools/check_examples.py runs this.
//   node tools/check_asyncapi.mjs case-study-reference/code/messaging/asyncapi.yaml
// Needs npm install first, for @asyncapi/parser.

import { Parser, fromFile } from "@asyncapi/parser";

const severityNames = ["error", "warning", "info", "hint"];
const parser = new Parser();
const { document, diagnostics } = await fromFile(parser, process.argv[2]).parse();
const problems = diagnostics.filter((diagnostic) => diagnostic.severity <= 1);
for (const diagnostic of problems) {
  console.log(severityNames[diagnostic.severity] + " " + diagnostic.code + ": " + diagnostic.message + " at " + diagnostic.path.join("."));
}
if (!document || problems.some((diagnostic) => diagnostic.severity === 0)) {
  process.exit(1);
}
console.log("valid");
