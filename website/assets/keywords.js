// keywords.js
const KEYWORDS = {
    'ስራ': 'def', 'ክፍለ': 'class', 'ከሆነ': 'if', 'ካልሆነ': 'else', 'ካልሆነከሆነ': 'elif',
    'እስከሆነ': 'while', 'ለእያንዳንዱ': 'for', 'ውስጥ': 'in', 'መልስ': 'return',
    'አሳይ': 'print', 'ጠይቅ': 'input', 'እና': 'and', 'ወይም': 'or', 'አይደለም': 'not',
    'እውነት': 'True', 'ሐሰት': 'False', 'ምንም': 'None', 'አምጣ': 'import',
    'ከ': 'from', 'እንደ': 'as', 'ሞክር': 'try', 'ስህተት': 'except', 'መጨረሻ': 'finally',
    'ጋር': 'with', 'አቋርጥ': 'break', 'ቀጥል': 'continue', 'ለጊዜው': 'pass',
    'አጭር': 'lambda', 'ርዝመት': 'len', 'ክልል': 'range', 'ዝርዝር': 'list',
    'መዝገብ': 'dict', 'ጽሑፍ': 'str', 'ቁጥር': 'int', 'ትክክለኛ': 'float',
    'ክፈት': 'open', 'እኔ': 'self'
};

function transpileToPreview(source) {
    let result = source;
    for (const [am, py] of Object.entries(KEYWORDS)) {
        // Ethiopic Unicode range aware word boundary
        const esc = am.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        result = result.replace(new RegExp(`(?<![\\u1200-\\u137F\\w])${esc}(?![\\u1200-\\u137F\\w])`, 'g'), py);
    }
    return result;
}
