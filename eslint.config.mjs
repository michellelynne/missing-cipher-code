import js from "@eslint/js";
import globals from "globals";

// Apps Script loads every .gs file in a project into one shared scope, so names defined in one
// file are globals in the others. Each is listed here once.
const appsScriptGlobals = {
  DocumentApp: "readonly",
  DriveApp: "readonly",
  MimeType: "readonly",
  Logger: "readonly",
  Utilities: "readonly",
  EDITOR_SETTINGS: "readonly",
  FIX_BATCH: "readonly",
  IMAGES_ONLY_DOC: "readonly",
  EditorEngine: "readonly",
  ImagesTool: "readonly",
  WordCountTool: "readonly",
};

export default [
  { ignores: ["dist/**", "node_modules/**", "**/.google-docs-bundle.cjs"] },
  js.configs.recommended,
  {
    files: ["**/*.gs"],
    languageOptions: { ecmaVersion: 2020, sourceType: "script", globals: appsScriptGlobals },
    rules: {
      // Top-level functions are run by the author from the Apps Script editor, and each file
      // defines the shared names listed above for the other files.
      "no-unused-vars": "off",
      "no-redeclare": ["error", { builtinGlobals: false }],
    },
  },
  {
    files: ["**/*.cjs"],
    languageOptions: { ecmaVersion: 2022, sourceType: "commonjs", globals: globals.node },
  },
  {
    files: ["**/*.mjs"],
    languageOptions: { ecmaVersion: 2022, sourceType: "module", globals: globals.node },
  },
];
