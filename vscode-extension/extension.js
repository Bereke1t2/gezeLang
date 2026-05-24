const vscode = require('vscode');

const KEYWORDS = {
    'ስራ': { py: 'def', desc: 'ተግባር መፍጠሪያ — Define a function' },
    'ክፍለ': { py: 'class', desc: 'ክፍል መፍጠሪያ — Define a class' },
    'ከሆነ': { py: 'if', desc: 'ሁኔታ መፈተሻ — Conditional if' },
    'ካልሆነ': { py: 'else', desc: 'አማራጭ መንገድ — Conditional else' },
    'ካልሆነከሆነ': { py: 'elif', desc: 'ተጨማሪ ሁኔታ መፈተሻ — Conditional elif' },
    'እስከሆነ': { py: 'while', desc: 'እስከተወሰነ ጊዜ የሚቀጥል ሉፕ — While loop' },
    'ለእያንዳንዱ': { py: 'for', desc: 'የሚደጋገም ሉፕ — For loop' },
    'ውስጥ': { py: 'in', desc: 'በውስጥ መገኘቱን ማረጋገጫ — In operator / Membership' },
    'መልስ': { py: 'return', desc: 'ውጤት መመለሻ — Return a value' },
    'አሳይ': { py: 'print', desc: 'ስክሪን ላይ ማሳያ — Print to screen' },
    'ጠይቅ': { py: 'input', desc: 'ከተጠቃሚ መረጃ መቀበያ — Get user input' },
    'እና': { py: 'and', desc: 'ሎጂካል እና — Logical AND' },
    'ወይም': { py: 'or', desc: 'ሎጂካል ወይም — Logical OR' },
    'አይደለም': { py: 'not', desc: 'የሎጂክ ተቃራኒ — Logical NOT' },
    'እውነት': { py: 'True', desc: 'እውነተኛ እሴት — Boolean True' },
    'ሐሰት': { py: 'False', desc: 'ሐሰተኛ እሴት — Boolean False' },
    'ምንም': { py: 'None', desc: 'ምንም እሴት የሌለው — Null value / None' },
    'አምጣ': { py: 'import', desc: 'ሞጁል ማምጫ — Import a module' },
    'ከ': { py: 'from', desc: 'ከሞጁል ውስጥ መምረጫ — Import from module' },
    'እንደ': { py: 'as', desc: 'በሌላ ስም መጠቀም — Alias (as)' },
    'ሞክር': { py: 'try', desc: 'ሊሳሳት የሚችል ኮድ መሞከሪያ — Try block' },
    'ስህተት': { py: 'except', desc: 'ስህተት ሲገኝ የሚሰራ — Exception handler' },
    'መጨረሻ': { py: 'finally', desc: 'በማንኛውም ሁኔታ የሚሰራ — Finally block' },
    'ጋር': { py: 'with', desc: 'አውድ አስተዳዳሪ — Context manager / With block' },
    'አቋርጥ': { py: 'break', desc: 'ሉፕ ማቋረጫ — Break out of loop' },
    'ቀጥል': { py: 'continue', desc: 'ወደሚቀጥለው ሉፕ መዝለያ — Continue immediately to next loop iteration' },
    'ለጊዜው': { py: 'pass', desc: 'ምንም የማያደርግ ማለፊያ — Placeholder / No-op (pass)' },
    'አጭር': { py: 'lambda', desc: 'ስም አልባ ተግባር — Anonymous lambda function' },
    'ርዝመት': { py: 'len', desc: 'የነገር ርዝመት መለኪያ — Get length of item' },
    'ክልል': { py: 'range', desc: 'የቁጥር ክልል መፍጠሪያ — Generate number range' },
    'ዝርዝር': { py: 'list', desc: 'ዝርዝር መፍጠሪያ — List data structure' },
    'መዝገብ': { py: 'dict', desc: 'መዝገበ-ቃላት መፍጠሪያ — Dictionary data structure' },
    'ጽሑፍ': { py: 'str', desc: 'ጽሑፍ (ስትሪንግ) — String data type' },
    'ቁጥር': { py: 'int', desc: 'ሙሉ ቁጥር — Integer data type' },
    'ትክክለኛ': { py: 'float', desc: 'ተንሳፋፊ/ነጥብ ቁጥር — Float/decimal data type' },
    'ክፈት': { py: 'open', desc: 'ፋይል መክፈቻ — Open a file' },
    'እኔ': { py: 'self', desc: 'የክፍል/ነገር ማጣቀሻ — Self instance reference' }
};

function activate(context) {
    // Hover Provider
    let hoverDisposable = vscode.languages.registerHoverProvider('amharicscript', {
        provideHover(document, position, token) {
            const wordRange = document.getWordRangeAtPosition(position, /[\u1200-\u137F][\u1200-\u137Fa-zA-Z0-9_]*/);
            if (!wordRange) return null;

            const word = document.getText(wordRange);
            const kw = KEYWORDS[word];
            if (kw) {
                const md = new vscode.MarkdownString();
                md.appendMarkdown(`**AmharicScript** — ቋልፍ ቃል (Keyword)\n\n`);
                md.appendMarkdown(`| Python | Meaning |\n`);
                md.appendMarkdown(`|---|---|\n`);
                md.appendMarkdown(`| \`${kw.py}\` | ${kw.desc} |\n`);
                return new vscode.Hover(md, wordRange);
            }
        }
    });

    // Run Command
    let runDisposable = vscode.commands.registerCommand('amharicscript.runFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('First open an AmharicScript (.amh) file!');
            return;
        }

        const document = editor.document;
        if (document.isDirty) {
            await document.save();
        }

        const config = vscode.workspace.getConfiguration('amharicscript');
        const pythonPath = config.get('pythonPath') || 'python';
        const translatorPath = config.get('translatorPath') || 'translator.py';
        const filepath = document.fileName;

        let terminal = vscode.window.terminals.find(t => t.name === 'AmharicScript');
        if (!terminal) {
            terminal = vscode.window.createTerminal('AmharicScript');
        }
        terminal.show();
        terminal.sendText(`clear`);
        terminal.sendText(`"${pythonPath}" "${translatorPath}" "${filepath}"`);
    });

    // Emit Python Command
    let emitDisposable = vscode.commands.registerCommand('amharicscript.emitPython', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const document = editor.document;
        if (document.isDirty) {
            await document.save();
        }

        const config = vscode.workspace.getConfiguration('amharicscript');
        const pythonPath = config.get('pythonPath') || 'python';
        const translatorPath = config.get('translatorPath') || 'translator.py';
        const filepath = document.fileName;

        let terminal = vscode.window.terminals.find(t => t.name === 'AmharicScript');
        if (!terminal) {
            terminal = vscode.window.createTerminal('AmharicScript');
        }
        terminal.show();
        terminal.sendText(`"${pythonPath}" "${translatorPath}" "${filepath}" --emit`);
    });

    context.subscriptions.push(hoverDisposable, runDisposable, emitDisposable);
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
};
