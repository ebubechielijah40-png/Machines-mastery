# Inspected concept map

| Original scope | Status | Internal reconstruction |
| --- | --- | --- |
| Chapter10 §10.6, Local Functions and Closures | Selected mechanism inspected | Captured lexical frame versus caller frame, shared captured cells and distinct factory calls in [chapter11](chapters/11/README.md) |
| Chapter11 §§11.1–11.5 | Inspected, bounded companion developed | Static scope counterexample; declare/define state; resolver pass; fixed lexical distance; read/assignment; duplicate local and invalid return errors |
| Other chapters, original exercises and full jlox/clox implementations | Not reconstructed here | Existing expression-language and C units provide related original mechanisms, not automatic book coverage |

The companion's AST grammar is deliberately smaller than Lox and makes one
additional static restriction: a local assignment to its own not-yet-initialized
binding is rejected, as well as a read. It does not claim full Lox compatibility.
