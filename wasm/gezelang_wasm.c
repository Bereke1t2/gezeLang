// gezelang_wasm.c — High-Performance WebAssembly Core for 10+ Ethiopic Dialects
#define WASM_EXPORT __attribute__((visibility("default")))

typedef struct {
    const char* native_kw;
    const char* py_kw;
} KwPair;

typedef struct {
    const char* lang_name;
    const KwPair* pairs;
    int count;
} LangTable;

static const KwPair pairs_amharic[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"ከሆነ", "if"},
    {"ካልሆነ", "else"},
    {"ካልሆነከሆነ", "elif"},
    {"እስከሆነ", "while"},
    {"ለእያንዳንዱ", "for"},
    {"ውስጥ", "in"},
    {"መልስ", "return"},
    {"አሳይ", "print"},
    {"ጠይቅ", "input"},
    {"እና", "and"},
    {"ወይም", "or"},
    {"አይደለም", "not"},
    {"እውነት", "True"},
    {"ሐሰት", "False"},
    {"ምንም", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"እንደ", "as"},
    {"ሞክር", "try"},
    {"ስህተት", "except"},
    {"መጨረሻ", "finally"},
    {"ጋር", "with"},
    {"አቋርጥ", "break"},
    {"ቀጥል", "continue"},
    {"ለጊዜው", "pass"},
    {"አጭር", "lambda"},
    {"ርዝመት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ትክክለኛ", "float"},
    {"ክፈት", "open"},
    {"እኔ", "self"},
};

static const KwPair pairs_amharic_gojjam[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"እንደሆን", "if"},
    {"ባይሆን", "else"},
    {"ካልሆነማ", "elif"},
    {"እስከሆነ", "while"},
    {"ለእያንዳንዱ", "for"},
    {"ውስጥ", "in"},
    {"መልስ", "return"},
    {"አሳይ", "print"},
    {"ጠይቅ", "input"},
    {"እና", "and"},
    {"ወይም", "or"},
    {"አይደልም", "not"},
    {"እውነት", "True"},
    {"ውሸት", "False"},
    {"ባዶ", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"እንደ", "as"},
    {"ሞክር", "try"},
    {"ስህተት", "except"},
    {"መጨረሻ", "finally"},
    {"ጋራ", "with"},
    {"አቋርጥ", "break"},
    {"ቀጥል", "continue"},
    {"ተወው", "pass"},
    {"አጭር", "lambda"},
    {"ርዝመት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ነጥብ", "float"},
    {"ክፈት", "open"},
    {"እኔ", "self"},
};

static const KwPair pairs_amharic_gondar[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"ቢሆን", "if"},
    {"ካልሆነ", "else"},
    {"ካልሆነስ", "elif"},
    {"እስካለ", "while"},
    {"ለእያንዳንዱ", "for"},
    {"ውስጥ", "in"},
    {"መልስ", "return"},
    {"አሰማ", "print"},
    {"ጠይቅ", "input"},
    {"እና", "and"},
    {"ወይም", "or"},
    {"አይደለም", "not"},
    {"እውነት", "True"},
    {"ሐሰት", "False"},
    {"ምንም", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"እንደ", "as"},
    {"ሞክር", "try"},
    {"ስህተት", "except"},
    {"መጨረሻ", "finally"},
    {"ጋር", "with"},
    {"ቁረጥ", "break"},
    {"ቀጥል", "continue"},
    {"ይደር", "pass"},
    {"አጭር", "lambda"},
    {"ርዝመት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ትክክለኛ", "float"},
    {"ክፈት", "open"},
    {"ራሴ", "self"},
};

static const KwPair pairs_amharic_shewa[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"ከሆነ", "if"},
    {"ካልሆነ", "else"},
    {"ካልሆነከሆነ", "elif"},
    {"እስከሆነ", "while"},
    {"ለእያንዳንዱ", "for"},
    {"ውስጥ", "in"},
    {"መልስ", "return"},
    {"አሳይ", "print"},
    {"ጠይቅ", "input"},
    {"እና", "and"},
    {"ወይም", "or"},
    {"አይደለም", "not"},
    {"እውነት", "True"},
    {"ሐሰት", "False"},
    {"ምንም", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"እንደ", "as"},
    {"ሞክር", "try"},
    {"ስህተት", "except"},
    {"መጨረሻ", "finally"},
    {"ጋር", "with"},
    {"አቋርጥ", "break"},
    {"ቀጥል", "continue"},
    {"እለፍ", "pass"},
    {"አጭር", "lambda"},
    {"ርዝመት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ትክክለኛ", "float"},
    {"ክፈት", "open"},
    {"እኔ", "self"},
};

static const KwPair pairs_amharic_wollo[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"ከሆነ", "if"},
    {"ካልሆነ", "else"},
    {"አለዚያም", "elif"},
    {"እስከሚሆን", "while"},
    {"ለእያንዳንዶ", "for"},
    {"ውስጥ", "in"},
    {"መልስ", "return"},
    {"አሳይ", "print"},
    {"ጠይቅ", "input"},
    {"ና", "and"},
    {"ወይ", "or"},
    {"አይደለም", "not"},
    {"እውነት", "True"},
    {"ሐሰት", "False"},
    {"ምንም", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"እንደ", "as"},
    {"ሞክር", "try"},
    {"ስህተት", "except"},
    {"ፍጻሜ", "finally"},
    {"ጋር", "with"},
    {"አቋርጥ", "break"},
    {"ቀጥል", "continue"},
    {"ይለፍ", "pass"},
    {"አጭር", "lambda"},
    {"ልክ", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ትክክለኛ", "float"},
    {"ክፈት", "open"},
    {"እኔ", "self"},
};

static const KwPair pairs_gamo[] = {
    {"ኦሶ", "def"},
    {"ክፍሊያ", "class"},
    {"ጊዲኮ", "if"},
    {"ጊዶንቶ", "else"},
    {"ዎይ_ጊዲኮ", "elif"},
    {"ጋካናስ", "while"},
    {"ኡባይስ", "for"},
    {"ጊዶን", "in"},
    {"ዛሮ", "return"},
    {"ቤሶ", "print"},
    {"ኦይቾ", "input"},
    {"ና", "and"},
    {"ዎይኮ", "or"},
    {"ጊዴና", "not"},
    {"ቱማ", "True"},
    {"ዎርዶ", "False"},
    {"ባይሲ", "None"},
    {"ኤሆ", "import"},
    {"ፔ", "from"},
    {"ማላ", "as"},
    {"ፓጮ", "try"},
    {"ባላ", "except"},
    {"ዉርሴታ", "finally"},
    {"ናራ", "with"},
    {"ቃንፆ", "break"},
    {"ሲንቴ", "continue"},
    {"አጎ", "pass"},
    {"ጉፃ", "lambda"},
    {"ጊሳ", "len"},
    {"ዛሪያ", "range"},
    {"ዛላ", "list"},
    {"ማክዛባ", "dict"},
    {"ፃፌታ", "str"},
    {"ፓይዶ", "int"},
    {"ላካ", "float"},
    {"ዶዮ", "open"},
    {"ባና", "self"},
};

static const KwPair pairs_geez[] = {
    {"ግበር", "def"},
    {"ማኅበር", "class"},
    {"ለእመ", "if"},
    {"ወእመአኮ", "else"},
    {"ወእመ", "elif"},
    {"እስከ", "while"},
    {"ለለ", "for"},
    {"ውስ Otto", "in"},
    {"ውስተ", "in"},
    {"አግብእ", "return"},
    {"አይድዕ", "print"},
    {"ሰአል", "input"},
    {"ወ", "and"},
    {"አው", "or"},
    {"ኢኮነ", "not"},
    {"ጽድቅ", "True"},
    {"ሐሰት", "False"},
    {"አልቦ", "None"},
    {"አምጽእ", "import"},
    {"እም", "from"},
    {"ከመ", "as"},
    {"ፈትን", "try"},
    {"ስሕተት", "except"},
    {"ተፍጻሜት", "finally"},
    {"ምስለ", "with"},
    {"በትር", "break"},
    {"ጽናዕ", "continue"},
    {"ኅድግ", "pass"},
    {"ኅጹር", "lambda"},
    {"ንዋኅ", "len"},
    {"ወሰን", "range"},
    {"ሰሌዳ", "list"},
    {"መዝገብ", "dict"},
    {"ጽሕፈት", "str"},
    {"ኍልቈ", "int"},
    {"ኅብስት", "float"},
    {"ክሥት", "open"},
    {"ኪያየ", "self"},
};

static const KwPair pairs_gofa[] = {
    {"ኦሶ", "def"},
    {"ክፍሊያ", "class"},
    {"ጊዲኮ", "if"},
    {"ጊዶናሽቲን", "else"},
    {"ዎይ_ጊዲኮ", "elif"},
    {"ጋካናው", "while"},
    {"ኡባስ", "for"},
    {"ጊዶን", "in"},
    {"ዛሮ", "return"},
    {"ቤሶ", "print"},
    {"ኦይቾ", "input"},
    {"ኔ", "and"},
    {"ዎይኮ", "or"},
    {"ጊዴና", "not"},
    {"ቱማ", "True"},
    {"ዎርዶ", "False"},
    {"ባዋ", "None"},
    {"ኤሆ", "import"},
    {"ፔ", "from"},
    {"ማላ", "as"},
    {"ፓጮ", "try"},
    {"ባላ", "except"},
    {"ዉርሴታ", "finally"},
    {"ናራ", "with"},
    {"ቃንፆ", "break"},
    {"ሲንቴ", "continue"},
    {"አጎ", "pass"},
    {"ጉፃ", "lambda"},
    {"ጊሳ", "len"},
    {"ዛሪያ", "range"},
    {"ዛላ", "list"},
    {"ማክዛባ", "dict"},
    {"ፃፌታ", "str"},
    {"ፓይዶ", "int"},
    {"ላካ", "float"},
    {"ዶዮ", "open"},
    {"ባና", "self"},
};

static const KwPair pairs_gurage[] = {
    {"ኤፐ", "def"},
    {"ክፍለ", "class"},
    {"ተኾነ", "if"},
    {"አንኾነ", "else"},
    {"ወይ_ተኾነ", "elif"},
    {"እስካረ", "while"},
    {"ለኤያንዳንድ", "for"},
    {"ውስጠ", "in"},
    {"አገፓ", "return"},
    {"አዠ", "print"},
    {"ጠየቀ", "input"},
    {"ተ", "and"},
    {"ወይ", "or"},
    {"አንኾነም", "not"},
    {"ኤውነት", "True"},
    {"ሀሰት", "False"},
    {"ባዶ", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"ከማ", "as"},
    {"ሞከረ", "try"},
    {"ስህተት", "except"},
    {"ተጨረሻ", "finally"},
    {"ጋር", "with"},
    {"አቋርጥ", "break"},
    {"ዠመረ", "continue"},
    {"እለፍ", "pass"},
    {"አጭር", "lambda"},
    {"ቁመት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቁጥር", "int"},
    {"ልክ", "float"},
    {"ክፈት", "open"},
    {"አውዴ", "self"},
};

static const KwPair pairs_hadiyya[] = {
    {"ማሮ", "def"},
    {"ክፍሊ", "class"},
    {"ዬንኮ", "if"},
    {"ዬኔቤሲ", "else"},
    {"ዎይ_ዬንኮ", "elif"},
    {"ጊዶ", "while"},
    {"ኡልጋ", "for"},
    {"ጊዶን", "in"},
    {"ጋሎ", "return"},
    {"ላፎ", "print"},
    {"ሺጎ", "input"},
    {"ና", "and"},
    {"ዎይ", "or"},
    {"ዬላንቾ", "not"},
    {"ሁላ", "True"},
    {"ሶቤ", "False"},
    {"ቤሲ", "None"},
    {"ኤቤሲ", "import"},
    {"ኔ", "from"},
    {"ጎይ", "as"},
    {"ፌጦ", "try"},
    {"ባላ", "except"},
    {"ጉፋንቾ", "finally"},
    {"ታን", "with"},
    {"ቆጶ", "break"},
    {"ሶኦዶ", "continue"},
    {"አጋ", "pass"},
    {"ጉፋ", "lambda"},
    {"ቁጶ", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"ኪታባ", "dict"},
    {"ቂጣባ", "str"},
    {"ሂዳ", "int"},
    {"ላካ", "float"},
    {"ፋኖ", "open"},
    {"ጊጋ", "self"},
};

static const KwPair pairs_harari[] = {
    {"አሻ", "def"},
    {"ክፍለ", "class"},
    {"ኸነጊር", "if"},
    {"አልኸነጊር", "else"},
    {"ወይ_ኸነጊር", "elif"},
    {"ዛለችቃሽ", "while"},
    {"ኩሉሌ", "for"},
    {"ኡስጢ", "in"},
    {"አግበኣ", "return"},
    {"አግነያ", "print"},
    {"ጠየቃ", "input"},
    {"ዋ", "and"},
    {"ወላ", "or"},
    {"አልኸነም", "not"},
    {"ሐቅ", "True"},
    {"ሐሰት", "False"},
    {"አልባን", "None"},
    {"አምጣኣ", "import"},
    {"ቤ", "from"},
    {"ኩት", "as"},
    {"ፈተና", "try"},
    {"ስሕተት", "except"},
    {"መጨረሻ", "finally"},
    {"ባሕ", "with"},
    {"አቋርጣ", "break"},
    {"ሔዳ", "continue"},
    {"ሐደጋ", "pass"},
    {"ሐጭር", "lambda"},
    {"ርዝመት", "len"},
    {"ወሰን", "range"},
    {"ዝርዝር", "list"},
    {"ኪታብ", "dict"},
    {"ኪታበት", "str"},
    {"ቁጥሪ", "int"},
    {"ልክ", "float"},
    {"ከፈታ", "open"},
    {"ሩሕ", "self"},
};

static const KwPair pairs_oromo[] = {
    {"hojii", "def"},
    {"gosa", "class"},
    {"yoo", "if"},
    {"yoo_miti", "else"},
    {"yookaan", "elif"},
    {"yeroo", "while"},
    {"hanga", "for"},
    {"keessa", "in"},
    {"deebi", "return"},
    {"agarsiisi", "print"},
    {"gaafadhu", "input"},
    {"fi", "and"},
    {"yookaan_lama", "or"},
    {"miti", "not"},
    {"Dhugaa", "True"},
    {"Sobaa", "False"},
    {"Wanti_hin_jirre", "None"},
    {"fidi", "import"},
    {"irra", "from"},
    {"akka", "as"},
    {"yaali", "try"},
    {"dogoggora", "except"},
    {"dhuma", "finally"},
    {"waliin", "with"},
    {"addaan_kut", "break"},
    {"itti_fufuu", "continue"},
    {"dabarsi", "pass"},
    {"lakkoofsa", "range"},
    {"dheerina", "len"},
    {"tarree", "list"},
    {"of", "self"},
};

static const KwPair pairs_silte[] = {
    {"ሻረ", "def"},
    {"ክፍለ", "class"},
    {"ቢሆን", "if"},
    {"ካልሆነ", "else"},
    {"ወይቢሆን", "elif"},
    {"እስካለ", "while"},
    {"ለኩሊም", "for"},
    {"ውስጠ", "in"},
    {"መለሰ", "return"},
    {"አባላ", "print"},
    {"ጠየቀ", "input"},
    {"ተ", "and"},
    {"ወላ", "or"},
    {"አደለም", "not"},
    {"ሐቅ", "True"},
    {"ሐሰት", "False"},
    {"ዬለ", "None"},
    {"አምጣ", "import"},
    {"ከ", "from"},
    {"ገሬ", "as"},
    {"ፈተነ", "try"},
    {"ስህተት", "except"},
    {"አኺር", "finally"},
    {"ጋር", "with"},
    {"አቋርጥ", "break"},
    {"ሄደ", "continue"},
    {"ተወው", "pass"},
    {"ቁርጥ", "lambda"},
    {"ርዝመት", "len"},
    {"ደረት", "range"},
    {"ደብተር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሕፈት", "str"},
    {"ቁጥር", "int"},
    {"ልክ", "float"},
    {"ፈተሐ", "open"},
    {"ኡፍኔ", "self"},
};

static const KwPair pairs_tigrinya[] = {
    {"ስራ", "def"},
    {"ክፍለ", "class"},
    {"እንተድኣ", "if"},
    {"እንተዘይኮይኑ", "else"},
    {"ወይ_እንተድኣ", "elif"},
    {"ክሳብ", "while"},
    {"ንነፍሲ_ወከፍ", "for"},
    {"ኣብ_ውሽጢ", "in"},
    {"መልስ", "return"},
    {"ኣርእይ", "print"},
    {"ሕተት", "input"},
    {"ን", "and"},
    {"ወይ", "or"},
    {"ኣይኮነን", "not"},
    {"ሓቂ", "True"},
    {"ሓሶት", "False"},
    {"ዋላ_ሓንቲ", "None"},
    {"ኣምጽእ", "import"},
    {"ካብ", "from"},
    {"ከም", "as"},
    {"ፈትን", "try"},
    {"ጌጋ", "except"},
    {"መወዳእታ", "finally"},
    {"ምስ", "with"},
    {"ኣቋርጽ", "break"},
    {"ቀጽል", "continue"},
    {"ሕለፍ", "pass"},
    {"ሓጺር", "lambda"},
    {"ንውሓት", "len"},
    {"ክልል", "range"},
    {"ዝርዝር", "list"},
    {"መዝገብ", "dict"},
    {"ጽሑፍ", "str"},
    {"ቍጽሪ", "int"},
    {"ልክዕ", "float"},
    {"ክፈት", "open"},
    {"ባዕለይ", "self"},
};

static const KwPair pairs_wolaytta[] = {
    {"ኦሶ", "def"},
    {"ክፍሊያ", "class"},
    {"ጊዲኮ", "if"},
    {"ጊዶናሽቲን", "else"},
    {"ወይ_ጊዲኮ", "elif"},
    {"ጋካናው", "while"},
    {"ሁበንቶሲ", "for"},
    {"ጊዶን", "in"},
    {"ዛሮ", "return"},
    {"ቤሶ", "print"},
    {"ኦይቾ", "input"},
    {"ኤራ", "and"},
    {"ዎይኮ", "or"},
    {"ጊዴና", "not"},
    {"ቱማ", "True"},
    {"ዎርዶ", "False"},
    {"ባዋ", "None"},
    {"ኤሆ", "import"},
    {"ፔ", "from"},
    {"ማላ", "as"},
    {"ፓጮ", "try"},
    {"ባላ", "except"},
    {"ዉርሴታ", "finally"},
    {"ናራ", "with"},
    {"ቃንፆ", "break"},
    {"ሲንቴ", "continue"},
    {"አጎ", "pass"},
    {"ቃንፃ", "lambda"},
    {"ጊሳ", "len"},
    {"ዛሪያ", "range"},
    {"ዛላ", "list"},
    {"ማክዛባ", "dict"},
    {"ፃፌታ", "str"},
    {"ፓይዶ", "int"},
    {"ላካ", "float"},
    {"ዶዮ", "open"},
    {"ባና", "self"},
};

static const LangTable LANG_TABLES[] = {
    {"amharic", pairs_amharic, sizeof(pairs_amharic) / sizeof(KwPair)},
    {"amharic_gojjam", pairs_amharic_gojjam, sizeof(pairs_amharic_gojjam) / sizeof(KwPair)},
    {"amharic_gondar", pairs_amharic_gondar, sizeof(pairs_amharic_gondar) / sizeof(KwPair)},
    {"amharic_shewa", pairs_amharic_shewa, sizeof(pairs_amharic_shewa) / sizeof(KwPair)},
    {"amharic_wollo", pairs_amharic_wollo, sizeof(pairs_amharic_wollo) / sizeof(KwPair)},
    {"gamo", pairs_gamo, sizeof(pairs_gamo) / sizeof(KwPair)},
    {"geez", pairs_geez, sizeof(pairs_geez) / sizeof(KwPair)},
    {"gofa", pairs_gofa, sizeof(pairs_gofa) / sizeof(KwPair)},
    {"gurage", pairs_gurage, sizeof(pairs_gurage) / sizeof(KwPair)},
    {"hadiyya", pairs_hadiyya, sizeof(pairs_hadiyya) / sizeof(KwPair)},
    {"harari", pairs_harari, sizeof(pairs_harari) / sizeof(KwPair)},
    {"oromo", pairs_oromo, sizeof(pairs_oromo) / sizeof(KwPair)},
    {"silte", pairs_silte, sizeof(pairs_silte) / sizeof(KwPair)},
    {"tigrinya", pairs_tigrinya, sizeof(pairs_tigrinya) / sizeof(KwPair)},
    {"wolaytta", pairs_wolaytta, sizeof(pairs_wolaytta) / sizeof(KwPair)},
};

#define NUM_LANGS 15


static char g_input[512 * 1024];
static char g_output[1024 * 1024];
static int g_output_len = 0;

WASM_EXPORT
char* wasm_get_input_buffer() {
    return g_input;
}

WASM_EXPORT
char* wasm_get_output_buffer() {
    return g_output;
}

WASM_EXPORT
int wasm_get_output_len() {
    return g_output_len;
}

WASM_EXPORT
int wasm_get_dialect_count() {
    return NUM_LANGS;
}

WASM_EXPORT
const char* wasm_get_dialect_name(int id) {
    if (id >= 0 && id < NUM_LANGS) {
        return LANG_TABLES[id].lang_name;
    }
    return "";
}

static int str_equals(const char* a, int a_len, const char* b) {
    int i = 0;
    while (i < a_len && b[i]) {
        if (a[i] != b[i]) return 0;
        i++;
    }
    return (i == a_len && b[i] == '\0');
}

static const char* lookup_keyword(int lang_id, const char* word, int word_len) {
    if (lang_id < 0 || lang_id >= NUM_LANGS) lang_id = 0;
    const LangTable* table = &LANG_TABLES[lang_id];
    for (int i = 0; i < table->count; i++) {
        if (str_equals(word, word_len, table->pairs[i].native_kw)) {
            return table->pairs[i].py_kw;
        }
    }
    return 0;
}

static int is_word_char(unsigned char c) {
    // Alphanumeric + underscore + all non-ASCII (UTF-8 multi-byte characters like Ethiopic)
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || (c == '_') || (c >= 0x80);
}

WASM_EXPORT
int wasm_transpile(int input_len, int lang_id) {
    if (input_len > sizeof(g_input) - 1) input_len = sizeof(g_input) - 1;
    g_input[input_len] = '\0';
    
    int in_idx = 0;
    int out_idx = 0;
    int max_out = sizeof(g_output) - 1;
    
    while (in_idx < input_len && out_idx < max_out - 100) {
        // Comments: # ... newline
        if (g_input[in_idx] == '#') {
            while (in_idx < input_len && g_input[in_idx] != '\n' && out_idx < max_out) {
                g_output[out_idx++] = g_input[in_idx++];
            }
            continue;
        }
        
        // Triple quotes or single quotes
        if (g_input[in_idx] == '"' || g_input[in_idx] == '\'') {
            char quote = g_input[in_idx];
            int is_triple = 0;
            if (in_idx + 2 < input_len && g_input[in_idx+1] == quote && g_input[in_idx+2] == quote) {
                is_triple = 1;
                g_output[out_idx++] = g_input[in_idx++];
                g_output[out_idx++] = g_input[in_idx++];
                g_output[out_idx++] = g_input[in_idx++];
            } else {
                g_output[out_idx++] = g_input[in_idx++];
            }
            
            while (in_idx < input_len && out_idx < max_out) {
                if (g_input[in_idx] == '\\' && in_idx + 1 < input_len) {
                    g_output[out_idx++] = g_input[in_idx++];
                    g_output[out_idx++] = g_input[in_idx++];
                    continue;
                }
                if (is_triple) {
                    if (in_idx + 2 < input_len && g_input[in_idx] == quote && g_input[in_idx+1] == quote && g_input[in_idx+2] == quote) {
                        g_output[out_idx++] = g_input[in_idx++];
                        g_output[out_idx++] = g_input[in_idx++];
                        g_output[out_idx++] = g_input[in_idx++];
                        break;
                    }
                } else {
                    if (g_input[in_idx] == quote || g_input[in_idx] == '\n') {
                        if (g_input[in_idx] == quote) g_output[out_idx++] = g_input[in_idx++];
                        break;
                    }
                }
                g_output[out_idx++] = g_input[in_idx++];
            }
            continue;
        }
        
        // Identifier / Word scanning
        if (is_word_char((unsigned char)g_input[in_idx])) {
            int word_start = in_idx;
            while (in_idx < input_len && is_word_char((unsigned char)g_input[in_idx])) {
                in_idx++;
            }
            int word_len = in_idx - word_start;
            const char* py_kw = lookup_keyword(lang_id, &g_input[word_start], word_len);
            if (py_kw) {
                while (*py_kw && out_idx < max_out) {
                    g_output[out_idx++] = *py_kw++;
                }
            } else {
                for (int w = 0; w < word_len && out_idx < max_out; w++) {
                    g_output[out_idx++] = g_input[word_start + w];
                }
            }
            continue;
        }
        
        // Other characters (operators, whitespace, delimiters)
        g_output[out_idx++] = g_input[in_idx++];
    }
    
    g_output[out_idx] = '\0';
    g_output_len = out_idx;
    return out_idx;
}

WASM_EXPORT
int wasm_version() {
    return 200; // v2.0
}
