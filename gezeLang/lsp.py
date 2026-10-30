"""
lsp.py — Production Language Server Protocol (LSP) Server for GezeLang.
Supports JSON-RPC 2.0 over stdio for VS Code, Neovim, Emacs, Cursor, Zed, and Sublime Text.
Features:
- Real-time syntax diagnostics with Amharic explanations
- Intelligent autocompletion for 15 Ethiopic dialects and user-defined symbols
- Interactive Markdown hover cards with Python equivalents & code snippets
- Document symbols (Outline view for functions, classes, and variables)
- Go-to-definition navigation
"""

import ast
import io
import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from gezeLang.adapter import AdapterRegistry
from gezeLang.lexer import OromLexer
from gezeLang.parser import OromParser
from gezeLang.explainer import explain_error

logger = logging.getLogger("gezelang-lsp")

# LSP CompletionItemKind constants
KIND_TEXT = 1
KIND_METHOD = 2
KIND_FUNCTION = 3
KIND_CONSTRUCTOR = 4
KIND_FIELD = 5
KIND_VARIABLE = 6
KIND_CLASS = 7
KIND_INTERFACE = 8
KIND_MODULE = 9
KIND_PROPERTY = 10
KIND_UNIT = 11
KIND_VALUE = 12
KIND_ENUM = 13
KIND_KEYWORD = 14
KIND_SNIPPET = 15

# LSP SymbolKind constants
SYMBOL_FILE = 1
SYMBOL_MODULE = 2
SYMBOL_NAMESPACE = 3
SYMBOL_PACKAGE = 4
SYMBOL_CLASS = 5
SYMBOL_METHOD = 6
SYMBOL_PROPERTY = 7
SYMBOL_FIELD = 8
SYMBOL_CONSTRUCTOR = 9
SYMBOL_ENUM = 10
SYMBOL_INTERFACE = 11
SYMBOL_FUNCTION = 12
SYMBOL_VARIABLE = 13
SYMBOL_CONSTANT = 14

# Keyword documentation dictionary
KEYWORD_DOCS: Dict[str, Dict[str, str]] = {
    "ስራ": {
        "title": "የተግባር (Function) መግለጫ",
        "desc": "አዲስ ተግባር (Function) ለመፍጠር የሚያገለግል ቁልፍ ቃል።",
        "example": "```gezeLang\nስራ ደምር(ሀ, ለ):\n    መልስ ሀ + ለ\n```",
        "py": "def"
    },
    "ክፍለ": {
        "title": "የክፍል (Class) መግለጫ",
        "desc": "አዲስ ክፍል (Class) እና የነገር አወቃቀር ለመፍጠር ያገለግላል።",
        "example": "```gezeLang\nክፍለ ተማሪ:\n    ስራ __init__(እኔ, ስም):\n        እኔ.ስም = ስም\n```",
        "py": "class"
    },
    "ከሆነ": {
        "title": "የሁኔታ መፈተሻ (If Statement)",
        "desc": "የተሰጠው ሁኔታ እውነት ከሆነ የሚፈጸም የቁጥጥር ፍሰት።",
        "example": "```gezeLang\nከሆነ ውጤት >= 50:\n    አሳይ(\"አልፏል\")\n```",
        "py": "if"
    },
    "ካልሆነ": {
        "title": "አማራጭ ሁኔታ (Else Statement)",
        "desc": "የመጀመሪያው ሁኔታ ሐሰት ከሆነ የሚከናወን አማራጭ ክፍልፍል፤",
        "example": "```gezeLang\nከሆነ x > 0:\n    አሳይ(\"አዎንታዊ\")\nካልሆነ:\n    አሳይ(\"አሉታዊ ወይም ዜሮ\")\n```",
        "py": "else"
    },
    "ካልሆነከሆነ": {
        "title": "ተጨማሪ ሁኔታ መፈተሻ (Elif)",
        "desc": "ተከታታይ የሁኔታ አማራጮችን ለመፈተሽ ያገለግላል።",
        "example": "```gezeLang\nከሆነ x > 0:\n    አሳይ(\"አዎንታዊ\")\nካልሆነከሆነ x < 0:\n    አሳይ(\"አሉታዊ\")\n```",
        "py": "elif"
    },
    "እስከሆነ": {
        "title": "ተደጋጋሚ ሉፕ (While Loop)",
        "desc": "የተሰጠው ሁኔታ እውነት ሆኖ እስካለ ድረስ የሚደጋገም ዑደት።",
        "example": "```gezeLang\nቆጣሪ = 1\nእስከሆነ ቆጣሪ <= 5:\n    አሳይ(ቆጣሪ)\n    ቆጣሪ += 1\n```",
        "py": "while"
    },
    "ለእያንዳንዱ": {
        "title": "የስብስብ ሉፕ (For Loop)",
        "desc": "በዝርዝር ወይም በስብስብ ውስጥ ላሉ ንጥሎች ሁሉ የሚከናወን ሉፕ።",
        "example": "```gezeLang\nለእያንዳንዱ ንጥል ውስጥ ክልል(1, 6):\n    አሳይ(ንጥል)\n```",
        "py": "for"
    },
    "ውስጥ": {
        "title": "በስብስብ ውስጥ መኖር (In)",
        "desc": "አንድ እሴት በስብስብ ውስጥ መኖሩን ለመፈተሽ ወይም በሉፕ ውስጥ ንጥሎችን ለማውጣት ያገለግላል።",
        "py": "in"
    },
    "መልስ": {
        "title": "ውጤት መመለሻ (Return)",
        "desc": "ከተግባር ውጤት ወደ ጠሪው ለመመለስ የሚያገለግል ቃል።",
        "py": "return"
    },
    "አሳይ": {
        "title": "ማሳያ (Print)",
        "desc": "ጽሑፍን ወይም እሴቶችን ወደ ተጠቃሚው ማሳያ (Console) ማውጫ።",
        "example": "```gezeLang\nአሳይ(\"ሰላም ለኢትዮጵያ!\")\n```",
        "py": "print"
    },
    "ጠይቅ": {
        "title": "ግቤት መቀበያ (Input)",
        "desc": "ከተጠቃሚው የግቤት መረጃ ለመቀበል ያገለግላል።",
        "py": "input"
    },
    "እና": {
        "title": "አመክንዮአዊ 'እና' (Logical AND)",
        "desc": "ሁለቱም ሁኔታዎች እውነት ከሆኑ እውነት የሚመልስ አመክንዮ።",
        "py": "and"
    },
    "ወይም": {
        "title": "አመክንዮአዊ 'ወይም' (Logical OR)",
        "desc": "ከሁለቱ አንዱ እውነት ከሆነ እውነት የሚመልስ አመክንዮ።",
        "py": "or"
    },
    "አይደለም": {
        "title": "አመክንዮአዊ 'አይደለም' (Logical NOT)",
        "desc": "የእሴቱን ተቃራኒ አመክንዮ የሚሰጥ።",
        "py": "not"
    },
    "እውነት": {
        "title": "የእውነት እሴት (True)",
        "desc": "እውነት (Boolean True) እሴት።",
        "py": "True"
    },
    "ሐሰት": {
        "title": "የሐሰት እሴት (False)",
        "desc": "ሐሰት (Boolean False) እሴት።",
        "py": "False"
    },
    "ምንም": {
        "title": "ባዶ እሴት (None)",
        "desc": "ምንም እሴት አለመኖሩን የሚያሳይ ባዶ እሴት (NoneType)።",
        "py": "None"
    },
    "አምጣ": {
        "title": "ሞጁል ማስመጣት (Import)",
        "desc": "ውጫዊ ቤተ-መጽሐፍት ወይም ሞጁል ወደ ፕሮግራሙ ለማስገባት ያገለግላል።",
        "py": "import"
    },
    "ከ": {
        "title": "ከሞጁል መምረጫ (From)",
        "desc": "ከተወሰነ ሞጁል ውስጥ የተወሰኑ ተግባራትን ብቻ ለመምረጥ ያገለግላል።",
        "py": "from"
    },
    "እንደ": {
        "title": "ተለዋጭ ስም መስጫ (As)",
        "desc": "ለተመረጠ ሞጁል ወይም እሴት አጭር ተለዋጭ ስም ለመስጠት ያገለግላል።",
        "py": "as"
    },
    "ሞክር": {
        "title": "ስህተት መሞከሪያ (Try)",
        "desc": "ስህተት ሊያስከትሉ የሚችሉ የኮድ ክፍሎችን ለመጠበቅ ያገለግላል።",
        "py": "try"
    },
    "ስህተት": {
        "title": "ስህተት መያዣ (Except)",
        "desc": "የተፈጠረን ስህተት በመያዝ ፕሮግራሙ እንዳይቋረጥ አማራጭ መፍትሔ መስጫ።",
        "py": "except"
    },
    "መጨረሻ": {
        "title": "የመጨረሻ ማስፈጸሚያ (Finally)",
        "desc": "ስህተት ቢፈጠርም ባይፈጠርም ሁልጊዜ የሚፈጸም የኮድ ክፍልፍል።",
        "py": "finally"
    },
    "ጋር": {
        "title": "የግብዓት አስተዳዳሪ (With Context Manager)",
        "desc": "ፋይሎችን ወይም ግብዓቶችን ደህንነቱ በተጠበቀ መንገድ ለመክፈትና ለመዝጋት ያገለግላል።",
        "py": "with"
    },
    "አቋርጥ": {
        "title": "ሉፕ ማቋረጫ (Break)",
        "desc": "የሚሄደውን ሉፕ ወዲያውኑ አቋርጦ ለመውጣት ያገለግላል።",
        "py": "break"
    },
    "ቀጥል": {
        "title": "ወደ ቀጣይ ዙር ማለፊያ (Continue)",
        "desc": "የአሁኑን የሉፕ ዙር ዘሎ በቀጥታ ወደ ቀጣዩ ዙር ለመሸጋገር ያገለግላል።",
        "py": "continue"
    },
    "ለጊዜው": {
        "title": "ባዶ ይለፍ (Pass)",
        "desc": "ለጊዜው ምንም የማይሰራ ባዶ የቦታ መያዣ።",
        "py": "pass"
    },
    "አጭር": {
        "title": "አጭር ተግባር (Lambda)",
        "desc": "በአንድ መስመር የሚገለጽ ያልተሰየመ አጭር ተግባር (Anonymous Function)።",
        "py": "lambda"
    },
    "ርዝመት": {
        "title": "ርዝመት መለኪያ (Len)",
        "desc": "የአንድ ጽሑፍ ወይም ስብስብ የንጥሎች ብዛት ለማወቅ ያገለግላል።",
        "py": "len"
    },
    "ክልል": {
        "title": "የቁጥር ክልል (Range)",
        "desc": "ከተወሰነ ጅምር እስከ ማብቂያ የቁጥሮች ተከታታይ ለማመንጨት ያገለግላል።",
        "py": "range"
    },
    "ዝርዝር": {
        "title": "የዝርዝር አይነት (List)",
        "desc": "የሚቀያየሩ ንጥሎች ስብስብ መፍጠሪያ።",
        "py": "list"
    },
    "መዝገብ": {
        "title": "የመዝገብ አይነት (Dict)",
        "desc": "ቁልፍና እሴት (Key-Value) የያዘ መዋቅር መፍጠሪያ።",
        "py": "dict"
    },
    "ጽሑፍ": {
        "title": "የጽሑፍ አይነት (Str)",
        "desc": "የቃላት እና ፊደላት ጽሑፍ መፍጠሪያ።",
        "py": "str"
    },
    "ቁጥር": {
        "title": "ሙሉ ቁጥር (Int)",
        "desc": "ሙሉ ቁጥር አይነት (Integer)።",
        "py": "int"
    },
    "ትክክለኛ": {
        "title": "ተንሳፋፊ ነጥብ ቁጥር (Float)",
        "desc": "የነጥብ ወይም የክፍልፋይ ቁጥር አይነት።",
        "py": "float"
    },
    "ክፈት": {
        "title": "ፋይል መክፈቻ (Open)",
        "desc": "ፋይሎችን ለማንበብ ወይም ለመጻፍ መክፈቻ።",
        "py": "open"
    },
    "እኔ": {
        "title": "የአሁኑ ነገር መጠሪያ (Self)",
        "desc": "በክፍል ውስጥ የአሁኑን ነገር (Instance) ለማመልከት የሚያገለግል መጠሪያ።",
        "py": "self"
    }
}


def get_word_at_position(text: str, line: int, character: int) -> str:
    """Extract full Unicode token/word around a specific 0-based line and character."""
    lines = text.splitlines()
    if line < 0 or line >= len(lines):
        return ""
    l = lines[line]
    if character < 0 or character > len(l):
        return ""

    start = character
    while start > 0 and (l[start - 1].isalnum() or l[start - 1] == '_'):
        start -= 1
    end = character
    while end < len(l) and (l[end].isalnum() or l[end] == '_'):
        end += 1
    return l[start:end]


def read_jsonrpc_message(stream: io.BufferedIOBase) -> Optional[Dict[str, Any]]:
    """Read a JSON-RPC 2.0 message with Content-Length header from stream."""
    content_length = None
    while True:
        line = stream.readline()
        if not line:
            return None
        line_str = line.decode('latin1').strip()
        if not line_str:
            break
        if line_str.lower().startswith("content-length:"):
            try:
                content_length = int(line_str.split(":", 1)[1].strip())
            except ValueError:
                return None

    if content_length is None:
        return None

    body = stream.read(content_length)
    if not body:
        return None
    try:
        return json.loads(body.decode('utf-8'))
    except Exception as e:
        logger.error(f"Failed to parse JSON body: {e}")
        return None


def write_jsonrpc_message(stream: io.BufferedIOBase, payload: Dict[str, Any]) -> None:
    """Write a JSON-RPC 2.0 message with Content-Length header to stream."""
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
    stream.write(header + body)
    stream.flush()


class LanguageServer:
    """GezeLang Language Server Protocol (LSP) Engine."""

    def __init__(self, default_lang: str = 'amharic'):
        self.default_lang = default_lang
        self.documents: Dict[str, str] = {}
        self.doc_dialects: Dict[str, str] = {}
        AdapterRegistry.discover(Path(__file__).parent / 'adapters')

    def get_dialect_for_uri(self, uri: str) -> str:
        """Infer dialect from URI or default."""
        if uri in self.doc_dialects:
            return self.doc_dialects[uri]
        lower = uri.lower()
        for l in AdapterRegistry.list_langs():
            if lower.endswith(f".{l}") or f"_{l}" in lower:
                return l
        return self.default_lang

    def handle_message(self, msg: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Dispatch a single JSON-RPC message and return list of response/notification dicts."""
        method = msg.get("method")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            return [self.handle_initialize(msg_id, params)]
        elif method == "initialized":
            return []
        elif method == "textDocument/didOpen":
            return self.handle_did_open(params)
        elif method == "textDocument/didChange":
            return self.handle_did_change(params)
        elif method == "textDocument/didClose":
            return self.handle_did_close(params)
        elif method == "textDocument/completion":
            return [self.handle_completion(msg_id, params)]
        elif method == "textDocument/hover":
            return [self.handle_hover(msg_id, params)]
        elif method == "textDocument/definition":
            return [self.handle_definition(msg_id, params)]
        elif method == "textDocument/documentSymbol":
            return [self.handle_document_symbol(msg_id, params)]
        elif method == "shutdown":
            return [{"jsonrpc": "2.0", "id": msg_id, "result": None}]
        elif method == "exit":
            return []

        # Unhandled method request
        if msg_id is not None:
            return [{
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not implemented"}
            }]
        return []

    def handle_initialize(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """LSP initialize handshake with server capabilities declaration."""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "capabilities": {
                    "textDocumentSync": 1,  # Full document sync
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": [".", " ", ":"]
                    },
                    "hoverProvider": True,
                    "definitionProvider": True,
                    "documentSymbolProvider": True
                },
                "serverInfo": {
                    "name": "gezelang-lsp",
                    "version": "1.2.0"
                }
            }
        }

    def handle_did_open(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        td = params.get("textDocument", {})
        uri = td.get("uri", "")
        text = td.get("text", "")
        self.documents[uri] = text
        return [self.publish_diagnostics(uri, text)]

    def handle_did_change(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        td = params.get("textDocument", {})
        uri = td.get("uri", "")
        changes = params.get("contentChanges", [])
        if changes:
            text = changes[-1].get("text", "")
            self.documents[uri] = text
            return [self.publish_diagnostics(uri, text)]
        return []

    def handle_did_close(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        td = params.get("textDocument", {})
        uri = td.get("uri", "")
        if uri in self.documents:
            del self.documents[uri]
        return [{
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {"uri": uri, "diagnostics": []}
        }]

    def publish_diagnostics(self, uri: str, text: str) -> Dict[str, Any]:
        """Parse document and return LSP publishDiagnostics notification."""
        lang = self.get_dialect_for_uri(uri)
        diagnostics = []

        try:
            lexer = OromLexer(text, lang=lang)
            py_src = lexer.translate()
            parser = OromParser()
            parser.parse(py_src, original_source=text)
        except Exception as e:
            # Extract line and column information
            lines = text.splitlines()
            err_line = 0
            err_col = 0
            err_msg = str(e)

            # Try to extract syntax error coordinates
            m = re.search(r'መስመር\s+(\d+),\s*ቦታ\s+(\d+)', err_msg)
            if m:
                err_line = max(0, int(m.group(1)) - 1)
                err_col = max(0, int(m.group(2)) - 1)

            max_col = len(lines[err_line]) if err_line < len(lines) else 100

            diagnostics.append({
                "range": {
                    "start": {"line": err_line, "character": err_col},
                    "end": {"line": err_line, "character": max_col}
                },
                "severity": 1,  # Error
                "source": f"GezeLang ({lang})",
                "message": err_msg
            })

        return {
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics
            }
        }

    def handle_completion(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Return completion items for Ethiopic keywords and user-defined symbols."""
        td = params.get("textDocument", {})
        uri = td.get("uri", "")
        lang = self.get_dialect_for_uri(uri)
        adapter = AdapterRegistry.get(lang)

        items = []

        # 1. Dialect keywords
        for eth_kw, py_kw in adapter._a2p.items():
            doc_entry = KEYWORD_DOCS.get(eth_kw, {})
            title = doc_entry.get("title", f"GezeLang Keyword ({lang})")
            desc = doc_entry.get("desc", f"Maps to Python '{py_kw}'.")
            example = doc_entry.get("example", "")

            md_doc = f"### {eth_kw} — {title}\n\n**Python:** `{py_kw}`\n\n{desc}"
            if example:
                md_doc += f"\n\n**ምሳሌ (Example):**\n{example}"

            items.append({
                "label": eth_kw,
                "kind": KIND_KEYWORD,
                "detail": f"({lang}) → {py_kw}",
                "documentation": {
                    "kind": "markdown",
                    "value": md_doc
                },
                "insertText": eth_kw
            })

        # 2. User-defined symbols in the document
        text = self.documents.get(uri, "")
        if text:
            try:
                py_src = OromLexer(text, lang=lang).translate()
                tree = ast.parse(py_src)
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        items.append({
                            "label": node.name,
                            "kind": KIND_FUNCTION,
                            "detail": f"ስራ {node.name}(...)",
                            "documentation": f"User-defined function in document (line {node.lineno}).",
                            "insertText": f"{node.name}()"
                        })
                    elif isinstance(node, ast.ClassDef):
                        items.append({
                            "label": node.name,
                            "kind": KIND_CLASS,
                            "detail": f"ክፍለ {node.name}",
                            "documentation": f"User-defined class in document (line {node.lineno}).",
                            "insertText": node.name
                        })
                    elif isinstance(node, ast.Assign):
                        for tgt in node.targets:
                            if isinstance(tgt, ast.Name):
                                items.append({
                                    "label": tgt.id,
                                    "kind": KIND_VARIABLE,
                                    "detail": f"ተለዋዋጭ (Variable) {tgt.id}",
                                    "documentation": f"Variable defined on line {node.lineno}.",
                                    "insertText": tgt.id
                                })
            except Exception:
                pass

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "isIncomplete": False,
                "items": items
            }
        }

    def handle_hover(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Return interactive markdown hover card for keywords and symbols."""
        td = params.get("textDocument", {})
        pos = params.get("position", {})
        uri = td.get("uri", "")
        line = pos.get("line", 0)
        char = pos.get("character", 0)

        text = self.documents.get(uri, "")
        if not text:
            return {"jsonrpc": "2.0", "id": msg_id, "result": None}

        word = get_word_at_position(text, line, char)
        if not word:
            return {"jsonrpc": "2.0", "id": msg_id, "result": None}

        lang = self.get_dialect_for_uri(uri)
        adapter = AdapterRegistry.get(lang)

        # 1. Keyword Hover
        if word in adapter._a2p:
            py_kw = adapter._a2p[word]
            doc_entry = KEYWORD_DOCS.get(word, {})
            title = doc_entry.get("title", f"የGezeLang ቁልፍ ቃል ({lang})")
            desc = doc_entry.get("desc", f"ወደ Python '{py_kw}' የሚቀየር ቁልፍ ቃል።")
            example = doc_entry.get("example", "")

            hover_md = f"## 🇪🇹 {word} ({title})\n\n"
            hover_md += f"**Python Equivalent:** `{py_kw}`\n\n"
            hover_md += f"{desc}\n"
            if example:
                hover_md += f"\n**ምሳሌ:**\n{example}"

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": hover_md
                    }
                }
            }

        # 2. Document Symbol Hover
        try:
            py_src = OromLexer(text, lang=lang).translate()
            tree = ast.parse(py_src)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == word:
                    args_str = ", ".join(a.arg for a in node.args.args)
                    doc_str = ast.get_docstring(node) or "ተግባር (Function) ያለ ማብራሪያ"
                    val = f"```gezeLang\nስራ {node.name}({args_str}):\n```\n\n{doc_str}\n\n*መስመር {node.lineno} ላይ የተገለጸ*"
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "contents": {"kind": "markdown", "value": val}
                        }
                    }
                elif isinstance(node, ast.ClassDef) and node.name == word:
                    doc_str = ast.get_docstring(node) or "ክፍል (Class)"
                    val = f"```gezeLang\nክፍለ {node.name}:\n```\n\n{doc_str}\n\n*መስመር {node.lineno} ላይ የተገለጸ*"
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "contents": {"kind": "markdown", "value": val}
                        }
                    }
        except Exception:
            pass

        return {"jsonrpc": "2.0", "id": msg_id, "result": None}

    def handle_definition(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Navigate to symbol definition in document."""
        td = params.get("textDocument", {})
        pos = params.get("position", {})
        uri = td.get("uri", "")
        line = pos.get("line", 0)
        char = pos.get("character", 0)

        text = self.documents.get(uri, "")
        if not text:
            return {"jsonrpc": "2.0", "id": msg_id, "result": None}

        word = get_word_at_position(text, line, char)
        if not word:
            return {"jsonrpc": "2.0", "id": msg_id, "result": None}

        lang = self.get_dialect_for_uri(uri)
        try:
            py_src = OromLexer(text, lang=lang).translate()
            tree = ast.parse(py_src)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == word:
                    def_line = node.lineno - 1
                    def_col = node.col_offset
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "uri": uri,
                            "range": {
                                "start": {"line": def_line, "character": def_col},
                                "end": {"line": def_line, "character": def_col + len(word)}
                            }
                        }
                    }
                elif isinstance(node, ast.Assign):
                    for tgt in node.targets:
                        if isinstance(tgt, ast.Name) and tgt.id == word:
                            def_line = node.lineno - 1
                            def_col = tgt.col_offset
                            return {
                                "jsonrpc": "2.0",
                                "id": msg_id,
                                "result": {
                                    "uri": uri,
                                    "range": {
                                        "start": {"line": def_line, "character": def_col},
                                        "end": {"line": def_line, "character": def_col + len(word)}
                                    }
                                }
                            }
        except Exception:
            pass

        return {"jsonrpc": "2.0", "id": msg_id, "result": None}

    def handle_document_symbol(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Return hierarchical outline symbols of functions, classes, and variables."""
        td = params.get("textDocument", {})
        uri = td.get("uri", "")
        text = self.documents.get(uri, "")
        if not text:
            return {"jsonrpc": "2.0", "id": msg_id, "result": []}

        lang = self.get_dialect_for_uri(uri)
        symbols = []

        try:
            py_src = OromLexer(text, lang=lang).translate()
            tree = ast.parse(py_src)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    start_l = node.lineno - 1
                    end_l = getattr(node, 'end_lineno', node.lineno) - 1
                    symbols.append({
                        "name": node.name,
                        "kind": SYMBOL_FUNCTION,
                        "range": {
                            "start": {"line": start_l, "character": node.col_offset},
                            "end": {"line": end_l, "character": 100}
                        },
                        "selectionRange": {
                            "start": {"line": start_l, "character": node.col_offset},
                            "end": {"line": start_l, "character": node.col_offset + len(node.name)}
                        }
                    })
                elif isinstance(node, ast.ClassDef):
                    start_l = node.lineno - 1
                    end_l = getattr(node, 'end_lineno', node.lineno) - 1
                    symbols.append({
                        "name": node.name,
                        "kind": SYMBOL_CLASS,
                        "range": {
                            "start": {"line": start_l, "character": node.col_offset},
                            "end": {"line": end_l, "character": 100}
                        },
                        "selectionRange": {
                            "start": {"line": start_l, "character": node.col_offset},
                            "end": {"line": start_l, "character": node.col_offset + len(node.name)}
                        }
                    })
                elif isinstance(node, ast.Assign):
                    for tgt in node.targets:
                        if isinstance(tgt, ast.Name):
                            start_l = node.lineno - 1
                            symbols.append({
                                "name": tgt.id,
                                "kind": SYMBOL_VARIABLE,
                                "range": {
                                    "start": {"line": start_l, "character": tgt.col_offset},
                                    "end": {"line": start_l, "character": tgt.col_offset + len(tgt.id)}
                                },
                                "selectionRange": {
                                    "start": {"line": start_l, "character": tgt.col_offset},
                                    "end": {"line": start_l, "character": tgt.col_offset + len(tgt.id)}
                                }
                            })
        except Exception:
            pass

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": symbols
        }

    def run_stdio(self, in_stream: Optional[io.BufferedIOBase] = None, out_stream: Optional[io.BufferedIOBase] = None):
        """Run standard I/O JSON-RPC processing loop."""
        in_s = in_stream or sys.stdin.buffer
        out_s = out_stream or sys.stdout.buffer

        while True:
            msg = read_jsonrpc_message(in_s)
            if msg is None:
                break
            responses = self.handle_message(msg)
            for resp in responses:
                write_jsonrpc_message(out_s, resp)
            if msg.get("method") == "exit":
                break


def run_server():
    """CLI entrypoint for running the GezeLang LSP server."""
    server = LanguageServer()
    server.run_stdio()


if __name__ == "__main__":
    run_server()
