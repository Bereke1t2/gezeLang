# Architecture of GezeLang

GezeLang is a **source-to-source transpiler** designed to parse code written in Ethiopian languages like Amharic, Afan Oromo, Tigrinya, etc., and convert it into completely standard Python 3.

## Phase 1: Lexical Translation
Because Python allows Unicode identifiers by default (e.g., `ሒሳብ = 10`), we only need to translate the *keywords*.

The `OromLexer` loads a `keywords.json` mapping (e.g. `{"ስራ": "def", ...}`).
It tokenizes the `.amh` source stream using standard `tokenize`, and searches for `NAME` tokens that match local keywords. If a match is found, it swaps it for the Python keyword. Finally, it untokenizes it.

## Phase 2: AST Parsing
The translated Python string is then parsed into a Python Abstract Syntax Tree (AST) using the standard `ast.parse()` library. 

If there is a `SyntaxError`, GezeLang catches it, maps the error coordinates back to the original source, and uses the `explainer.py` to give a translated helpful error message in the user's local language.

## Phase 3: Code Generation
The AST is then unparsed back to strings using `ast.unparse()`. This results in perfectly clean, standard Python code.

## Runtime Execution
Because the resulting code is executed in standard `CPython`, there is **zero performance overhead**. The variables keep their Unicode names, while all keywords are internally executed natively as Python keywords.
