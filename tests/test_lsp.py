"""
tests/test_lsp.py — Comprehensive tests for GezeLang Language Server Protocol (LSP).
"""

import io
import pytest
from gezeLang.lsp import (
    LanguageServer,
    read_jsonrpc_message,
    write_jsonrpc_message,
    KIND_KEYWORD,
    KIND_FUNCTION,
    SYMBOL_FUNCTION,
    SYMBOL_CLASS
)


@pytest.fixture
def lsp_server():
    """Create a fresh LanguageServer instance."""
    return LanguageServer(default_lang='amharic')


def test_jsonrpc_framing():
    """Verify JSON-RPC 2.0 Content-Length header framing."""
    buf = io.BytesIO()
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "testMethod",
        "params": {"foo": "bar", "ethiopic": "ሰላም"}
    }
    write_jsonrpc_message(buf, payload)
    buf.seek(0)
    received = read_jsonrpc_message(buf)
    assert received == payload


def test_lsp_initialize(lsp_server):
    """Verify initialize request declares full language capabilities."""
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "clientInfo": {"name": "VSCode", "version": "1.90.0"},
            "capabilities": {}
        }
    }
    responses = lsp_server.handle_message(init_req)
    assert len(responses) == 1
    resp = responses[0]
    assert resp["id"] == 1
    caps = resp["result"]["capabilities"]
    assert caps["hoverProvider"] is True
    assert caps["definitionProvider"] is True
    assert caps["documentSymbolProvider"] is True
    assert caps["textDocumentSync"] == 1
    assert "completionProvider" in caps


def test_lsp_diagnostics_clean_and_error(lsp_server):
    """Verify didOpen publishes empty diagnostics for valid code and error diagnostics for invalid code."""
    uri_valid = "file:///workspace/valid.amh"
    valid_code = """ስራ ሰላም():
    መልስ "ሰላም"
"""
    open_valid = {
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": uri_valid,
                "languageId": "gezelang",
                "version": 1,
                "text": valid_code
            }
        }
    }
    resps = lsp_server.handle_message(open_valid)
    assert len(resps) == 1
    assert resps[0]["method"] == "textDocument/publishDiagnostics"
    assert resps[0]["params"]["diagnostics"] == []

    # Now open invalid code (missing colon after function definition)
    uri_invalid = "file:///workspace/invalid.amh"
    invalid_code = """ስራ ስህተት()
    መልስ 1
"""
    open_invalid = {
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": uri_invalid,
                "languageId": "gezelang",
                "version": 1,
                "text": invalid_code
            }
        }
    }
    resps_err = lsp_server.handle_message(open_invalid)
    assert len(resps_err) == 1
    diags = resps_err[0]["params"]["diagnostics"]
    assert len(diags) >= 1
    assert diags[0]["severity"] == 1
    assert "ስህተት" in diags[0]["message"] or "colon" in diags[0]["message"]


def test_lsp_completion(lsp_server):
    """Verify autocompletion returns Ethiopic keywords and user functions."""
    uri = "file:///workspace/app.amh"
    code = """ስራ ደምር(ሀ, ለ):
    መልስ ሀ + ለ

ውጤት = 10
"""
    lsp_server.handle_message({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {"textDocument": {"uri": uri, "text": code}}
    })

    comp_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/completion",
        "params": {
            "textDocument": {"uri": uri},
            "position": {"line": 4, "character": 0}
        }
    }
    resps = lsp_server.handle_message(comp_req)
    assert len(resps) == 1
    items = resps[0]["result"]["items"]

    # Check for keyword
    labels = {it["label"]: it for it in items}
    assert "ስራ" in labels
    assert labels["ስራ"]["kind"] == KIND_KEYWORD
    assert "def" in labels["ስራ"]["detail"]

    # Check for user function
    assert "ደምር" in labels
    assert labels["ደምር"]["kind"] == KIND_FUNCTION


def test_lsp_hover(lsp_server):
    """Verify hover returns rich markdown information for keywords and functions."""
    uri = "file:///workspace/hover_test.amh"
    code = """ስራ ሰላምታ(ስም):
    '''የሰላምታ ተግባር'''
    መልስ f"ሰላም {ስም}"
"""
    lsp_server.handle_message({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {"textDocument": {"uri": uri, "text": code}}
    })

    # Hover over keyword 'ስራ' at line 0, char 1
    hover_kw = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "textDocument/hover",
        "params": {
            "textDocument": {"uri": uri},
            "position": {"line": 0, "character": 1}
        }
    }
    resp = lsp_server.handle_message(hover_kw)[0]
    contents = resp["result"]["contents"]["value"]
    assert "ስራ" in contents
    assert "def" in contents

    # Hover over function name 'ሰላምታ' at line 0, char 5
    hover_fn = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "textDocument/hover",
        "params": {
            "textDocument": {"uri": uri},
            "position": {"line": 0, "character": 5}
        }
    }
    resp_fn = lsp_server.handle_message(hover_fn)[0]
    contents_fn = resp_fn["result"]["contents"]["value"]
    assert "ሰላምታ" in contents_fn
    assert "የሰላምታ ተግባር" in contents_fn


def test_lsp_definition(lsp_server):
    """Verify go-to-definition jumps to function location."""
    uri = "file:///workspace/def_test.amh"
    code = """ስራ ሒሳብ(ቁጥር):
    መልስ ቁጥር * 2

ውጤት = ሒሳብ(10)
"""
    lsp_server.handle_message({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {"textDocument": {"uri": uri, "text": code}}
    })

    # Request definition for 'ሒሳብ' at call site (line 3, char 8)
    def_req = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "textDocument/definition",
        "params": {
            "textDocument": {"uri": uri},
            "position": {"line": 3, "character": 8}
        }
    }
    resp = lsp_server.handle_message(def_req)[0]
    target = resp["result"]
    assert target is not None
    assert target["uri"] == uri
    # Function is defined on line 0
    assert target["range"]["start"]["line"] == 0


def test_lsp_document_symbols(lsp_server):
    """Verify document symbol outline extraction for functions and classes."""
    uri = "file:///workspace/symbols.amh"
    code = """ክፍለ እንስሳ:
    ስራ ጩኽ(እኔ):
        አሳይ("ድምፅ")

ስራ ዋና():
    አሳይ("ጅምር")
"""
    lsp_server.handle_message({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {"textDocument": {"uri": uri, "text": code}}
    })

    sym_req = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "textDocument/documentSymbol",
        "params": {"textDocument": {"uri": uri}}
    }
    resp = lsp_server.handle_message(sym_req)[0]
    symbols = resp["result"]
    names = {s["name"]: s for s in symbols}
    assert "እንስሳ" in names
    assert names["እንስሳ"]["kind"] == SYMBOL_CLASS
    assert "ዋና" in names
    assert names["ዋና"]["kind"] == SYMBOL_FUNCTION


def test_lsp_stdio_simulation(lsp_server):
    """Verify standard I/O streaming loop processes multiple requests and terminates on exit."""
    in_buf = io.BytesIO()
    out_buf = io.BytesIO()

    # Write initialize request followed by exit notification
    write_jsonrpc_message(in_buf, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    write_jsonrpc_message(in_buf, {"jsonrpc": "2.0", "method": "exit"})

    in_buf.seek(0)
    lsp_server.run_stdio(in_stream=in_buf, out_stream=out_buf)

    out_buf.seek(0)
    resp = read_jsonrpc_message(out_buf)
    assert resp is not None
    assert resp["id"] == 1
    assert "capabilities" in resp["result"]
