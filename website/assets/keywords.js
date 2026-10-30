// keywords.js — Multi-Dialect WebAssembly & Transpiler Engine for 10+ Ethiopic Dialects
var GEZELANG_DIALECTS = {
  "amharic": {
    "id": 0,
    "label": "አማርኛ (Amharic - Standard)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "ከሆነ": "if",
      "ካልሆነ": "else",
      "ካልሆነከሆነ": "elif",
      "እስከሆነ": "while",
      "ለእያንዳንዱ": "for",
      "ውስጥ": "in",
      "መልስ": "return",
      "አሳይ": "print",
      "ጠይቅ": "input",
      "እና": "and",
      "ወይም": "or",
      "አይደለም": "not",
      "እውነት": "True",
      "ሐሰት": "False",
      "ምንም": "None",
      "አምጣ": "import",
      "ከ": "from",
      "እንደ": "as",
      "ሞክር": "try",
      "ስህተት": "except",
      "መጨረሻ": "finally",
      "ጋር": "with",
      "አቋርጥ": "break",
      "ቀጥል": "continue",
      "ለጊዜው": "pass",
      "አጭር": "lambda",
      "ርዝመት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ትክክለኛ": "float",
      "ክፈት": "open",
      "እኔ": "self"
    }
  },
  "amharic_gojjam": {
    "id": 1,
    "label": "የጎጃም አማርኛ (Gojjami Amharic)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "እንደሆን": "if",
      "ባይሆን": "else",
      "ካልሆነማ": "elif",
      "እስከሆነ": "while",
      "ለእያንዳንዱ": "for",
      "ውስጥ": "in",
      "መልስ": "return",
      "አሳይ": "print",
      "ጠይቅ": "input",
      "እና": "and",
      "ወይም": "or",
      "አይደልም": "not",
      "እውነት": "True",
      "ውሸት": "False",
      "ባዶ": "None",
      "አምጣ": "import",
      "ከ": "from",
      "እንደ": "as",
      "ሞክር": "try",
      "ስህተት": "except",
      "መጨረሻ": "finally",
      "ጋራ": "with",
      "አቋርጥ": "break",
      "ቀጥል": "continue",
      "ተወው": "pass",
      "አጭር": "lambda",
      "ርዝመት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ነጥብ": "float",
      "ክፈት": "open",
      "እኔ": "self"
    }
  },
  "amharic_gondar": {
    "id": 2,
    "label": "የጎንደር አማርኛ (Gondari Amharic)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "ቢሆን": "if",
      "ካልሆነ": "else",
      "ካልሆነስ": "elif",
      "እስካለ": "while",
      "ለእያንዳንዱ": "for",
      "ውስጥ": "in",
      "መልስ": "return",
      "አሰማ": "print",
      "ጠይቅ": "input",
      "እና": "and",
      "ወይም": "or",
      "አይደለም": "not",
      "እውነት": "True",
      "ሐሰት": "False",
      "ምንም": "None",
      "አምጣ": "import",
      "ከ": "from",
      "እንደ": "as",
      "ሞክር": "try",
      "ስህተት": "except",
      "መጨረሻ": "finally",
      "ጋር": "with",
      "ቁረጥ": "break",
      "ቀጥል": "continue",
      "ይደር": "pass",
      "አጭር": "lambda",
      "ርዝመት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ትክክለኛ": "float",
      "ክፈት": "open",
      "ራሴ": "self"
    }
  },
  "amharic_shewa": {
    "id": 3,
    "label": "የሸዋ አማርኛ (Shewa Amharic)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "ከሆነ": "if",
      "ካልሆነ": "else",
      "ካልሆነከሆነ": "elif",
      "እስከሆነ": "while",
      "ለእያንዳንዱ": "for",
      "ውስጥ": "in",
      "መልስ": "return",
      "አሳይ": "print",
      "ጠይቅ": "input",
      "እና": "and",
      "ወይም": "or",
      "አይደለም": "not",
      "እውነት": "True",
      "ሐሰት": "False",
      "ምንም": "None",
      "አምጣ": "import",
      "ከ": "from",
      "እንደ": "as",
      "ሞክር": "try",
      "ስህተት": "except",
      "መጨረሻ": "finally",
      "ጋር": "with",
      "አቋርጥ": "break",
      "ቀጥል": "continue",
      "እለፍ": "pass",
      "አጭር": "lambda",
      "ርዝመት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ትክክለኛ": "float",
      "ክፈት": "open",
      "እኔ": "self"
    }
  },
  "amharic_wollo": {
    "id": 4,
    "label": "የወሎ አማርኛ (Wollo Amharic)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "ከሆነ": "if",
      "ካልሆነ": "else",
      "አለዚያም": "elif",
      "እስከሚሆን": "while",
      "ለእያንዳንዶ": "for",
      "ውስጥ": "in",
      "መልስ": "return",
      "አሳይ": "print",
      "ጠይቅ": "input",
      "ና": "and",
      "ወይ": "or",
      "አይደለም": "not",
      "እውነት": "True",
      "ሐሰት": "False",
      "ምንም": "None",
      "አምጣ": "import",
      "ከ": "from",
      "እንደ": "as",
      "ሞክር": "try",
      "ስህተት": "except",
      "ፍጻሜ": "finally",
      "ጋር": "with",
      "አቋርጥ": "break",
      "ቀጥል": "continue",
      "ይለፍ": "pass",
      "አጭር": "lambda",
      "ልክ": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ትክክለኛ": "float",
      "ክፈት": "open",
      "እኔ": "self"
    }
  },
  "gamo": {
    "id": 5,
    "label": "ጋሞ (Gamo)",
    "keywords": {
      "ኦሶ": "def",
      "ክፍሊያ": "class",
      "ጊዲኮ": "if",
      "ጊዶንቶ": "else",
      "ዎይ_ጊዲኮ": "elif",
      "ጋካናስ": "while",
      "ኡባይስ": "for",
      "ጊዶን": "in",
      "ዛሮ": "return",
      "ቤሶ": "print",
      "ኦይቾ": "input",
      "ና": "and",
      "ዎይኮ": "or",
      "ጊዴና": "not",
      "ቱማ": "True",
      "ዎርዶ": "False",
      "ባይሲ": "None",
      "ኤሆ": "import",
      "ፔ": "from",
      "ማላ": "as",
      "ፓጮ": "try",
      "ባላ": "except",
      "ዉርሴታ": "finally",
      "ናራ": "with",
      "ቃንፆ": "break",
      "ሲንቴ": "continue",
      "አጎ": "pass",
      "ጉፃ": "lambda",
      "ጊሳ": "len",
      "ዛሪያ": "range",
      "ዛላ": "list",
      "ማክዛባ": "dict",
      "ፃፌታ": "str",
      "ፓይዶ": "int",
      "ላካ": "float",
      "ዶዮ": "open",
      "ባና": "self"
    }
  },
  "geez": {
    "id": 6,
    "label": "ግዕዝ (Classical Ge'ez)",
    "keywords": {
      "ግበር": "def",
      "ማኅበር": "class",
      "ለእመ": "if",
      "ወእመአኮ": "else",
      "ወእመ": "elif",
      "እስከ": "while",
      "ለለ": "for",
      "ውስ Otto": "in",
      "ውስተ": "in",
      "አግብእ": "return",
      "አይድዕ": "print",
      "ሰአል": "input",
      "ወ": "and",
      "አው": "or",
      "ኢኮነ": "not",
      "ጽድቅ": "True",
      "ሐሰት": "False",
      "አልቦ": "None",
      "አምጽእ": "import",
      "እም": "from",
      "ከመ": "as",
      "ፈትን": "try",
      "ስሕተት": "except",
      "ተፍጻሜት": "finally",
      "ምስለ": "with",
      "በትር": "break",
      "ጽናዕ": "continue",
      "ኅድግ": "pass",
      "ኅጹር": "lambda",
      "ንዋኅ": "len",
      "ወሰን": "range",
      "ሰሌዳ": "list",
      "መዝገብ": "dict",
      "ጽሕፈት": "str",
      "ኍልቈ": "int",
      "ኅብስት": "float",
      "ክሥት": "open",
      "ኪያየ": "self"
    }
  },
  "gofa": {
    "id": 7,
    "label": "ጎፋ (Gofa)",
    "keywords": {
      "ኦሶ": "def",
      "ክፍሊያ": "class",
      "ጊዲኮ": "if",
      "ጊዶናሽቲን": "else",
      "ዎይ_ጊዲኮ": "elif",
      "ጋካናው": "while",
      "ኡባስ": "for",
      "ጊዶን": "in",
      "ዛሮ": "return",
      "ቤሶ": "print",
      "ኦይቾ": "input",
      "ኔ": "and",
      "ዎይኮ": "or",
      "ጊዴና": "not",
      "ቱማ": "True",
      "ዎርዶ": "False",
      "ባዋ": "None",
      "ኤሆ": "import",
      "ፔ": "from",
      "ማላ": "as",
      "ፓጮ": "try",
      "ባላ": "except",
      "ዉርሴታ": "finally",
      "ናራ": "with",
      "ቃንፆ": "break",
      "ሲንቴ": "continue",
      "አጎ": "pass",
      "ጉፃ": "lambda",
      "ጊሳ": "len",
      "ዛሪያ": "range",
      "ዛላ": "list",
      "ማክዛባ": "dict",
      "ፃፌታ": "str",
      "ፓይዶ": "int",
      "ላካ": "float",
      "ዶዮ": "open",
      "ባና": "self"
    }
  },
  "gurage": {
    "id": 8,
    "label": "ጉራጊኛ (Gurage - Sebat Bet)",
    "keywords": {
      "ኤፐ": "def",
      "ክፍለ": "class",
      "ተኾነ": "if",
      "አንኾነ": "else",
      "ወይ_ተኾነ": "elif",
      "እስካረ": "while",
      "ለኤያንዳንድ": "for",
      "ውስጠ": "in",
      "አገፓ": "return",
      "አዠ": "print",
      "ጠየቀ": "input",
      "ተ": "and",
      "ወይ": "or",
      "አንኾነም": "not",
      "ኤውነት": "True",
      "ሀሰት": "False",
      "ባዶ": "None",
      "አምጣ": "import",
      "ከ": "from",
      "ከማ": "as",
      "ሞከረ": "try",
      "ስህተት": "except",
      "ተጨረሻ": "finally",
      "ጋር": "with",
      "አቋርጥ": "break",
      "ዠመረ": "continue",
      "እለፍ": "pass",
      "አጭር": "lambda",
      "ቁመት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቁጥር": "int",
      "ልክ": "float",
      "ክፈት": "open",
      "አውዴ": "self"
    }
  },
  "hadiyya": {
    "id": 9,
    "label": "ሀዲያ (Hadiyya)",
    "keywords": {
      "ማሮ": "def",
      "ክፍሊ": "class",
      "ዬንኮ": "if",
      "ዬኔቤሲ": "else",
      "ዎይ_ዬንኮ": "elif",
      "ጊዶ": "while",
      "ኡልጋ": "for",
      "ጊዶን": "in",
      "ጋሎ": "return",
      "ላፎ": "print",
      "ሺጎ": "input",
      "ና": "and",
      "ዎይ": "or",
      "ዬላንቾ": "not",
      "ሁላ": "True",
      "ሶቤ": "False",
      "ቤሲ": "None",
      "ኤቤሲ": "import",
      "ኔ": "from",
      "ጎይ": "as",
      "ፌጦ": "try",
      "ባላ": "except",
      "ጉፋንቾ": "finally",
      "ታን": "with",
      "ቆጶ": "break",
      "ሶኦዶ": "continue",
      "አጋ": "pass",
      "ጉፋ": "lambda",
      "ቁጶ": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "ኪታባ": "dict",
      "ቂጣባ": "str",
      "ሂዳ": "int",
      "ላካ": "float",
      "ፋኖ": "open",
      "ጊጋ": "self"
    }
  },
  "harari": {
    "id": 10,
    "label": "ሐረሪ (Harari - Gey Sinan)",
    "keywords": {
      "አሻ": "def",
      "ክፍለ": "class",
      "ኸነጊር": "if",
      "አልኸነጊር": "else",
      "ወይ_ኸነጊር": "elif",
      "ዛለችቃሽ": "while",
      "ኩሉሌ": "for",
      "ኡስጢ": "in",
      "አግበኣ": "return",
      "አግነያ": "print",
      "ጠየቃ": "input",
      "ዋ": "and",
      "ወላ": "or",
      "አልኸነም": "not",
      "ሐቅ": "True",
      "ሐሰት": "False",
      "አልባን": "None",
      "አምጣኣ": "import",
      "ቤ": "from",
      "ኩት": "as",
      "ፈተና": "try",
      "ስሕተት": "except",
      "መጨረሻ": "finally",
      "ባሕ": "with",
      "አቋርጣ": "break",
      "ሔዳ": "continue",
      "ሐደጋ": "pass",
      "ሐጭር": "lambda",
      "ርዝመት": "len",
      "ወሰን": "range",
      "ዝርዝር": "list",
      "ኪታብ": "dict",
      "ኪታበት": "str",
      "ቁጥሪ": "int",
      "ልክ": "float",
      "ከፈታ": "open",
      "ሩሕ": "self"
    }
  },
  "oromo": {
    "id": 11,
    "label": "Afaan Oromoo",
    "keywords": {
      "hojii": "def",
      "gosa": "class",
      "yoo": "if",
      "yoo_miti": "else",
      "yookaan": "elif",
      "yeroo": "while",
      "hanga": "for",
      "keessa": "in",
      "deebi": "return",
      "agarsiisi": "print",
      "gaafadhu": "input",
      "fi": "and",
      "yookaan_lama": "or",
      "miti": "not",
      "Dhugaa": "True",
      "Sobaa": "False",
      "Wanti_hin_jirre": "None",
      "fidi": "import",
      "irra": "from",
      "akka": "as",
      "yaali": "try",
      "dogoggora": "except",
      "dhuma": "finally",
      "waliin": "with",
      "addaan_kut": "break",
      "itti_fufuu": "continue",
      "dabarsi": "pass",
      "lakkoofsa": "range",
      "dheerina": "len",
      "tarree": "list",
      "of": "self"
    }
  },
  "silte": {
    "id": 12,
    "label": "ስልጤ (Silt'e)",
    "keywords": {
      "ሻረ": "def",
      "ክፍለ": "class",
      "ቢሆን": "if",
      "ካልሆነ": "else",
      "ወይቢሆን": "elif",
      "እስካለ": "while",
      "ለኩሊም": "for",
      "ውስጠ": "in",
      "መለሰ": "return",
      "አባላ": "print",
      "ጠየቀ": "input",
      "ተ": "and",
      "ወላ": "or",
      "አደለም": "not",
      "ሐቅ": "True",
      "ሐሰት": "False",
      "ዬለ": "None",
      "አምጣ": "import",
      "ከ": "from",
      "ገሬ": "as",
      "ፈተነ": "try",
      "ስህተት": "except",
      "አኺር": "finally",
      "ጋር": "with",
      "አቋርጥ": "break",
      "ሄደ": "continue",
      "ተወው": "pass",
      "ቁርጥ": "lambda",
      "ርዝመት": "len",
      "ደረት": "range",
      "ደብተር": "list",
      "መዝገብ": "dict",
      "ጽሕፈት": "str",
      "ቁጥር": "int",
      "ልክ": "float",
      "ፈተሐ": "open",
      "ኡፍኔ": "self"
    }
  },
  "tigrinya": {
    "id": 13,
    "label": "ትግርኛ (Tigrinya)",
    "keywords": {
      "ስራ": "def",
      "ክፍለ": "class",
      "እንተድኣ": "if",
      "እንተዘይኮይኑ": "else",
      "ወይ_እንተድኣ": "elif",
      "ክሳብ": "while",
      "ንነፍሲ_ወከፍ": "for",
      "ኣብ_ውሽጢ": "in",
      "መልስ": "return",
      "ኣርእይ": "print",
      "ሕተት": "input",
      "ን": "and",
      "ወይ": "or",
      "ኣይኮነን": "not",
      "ሓቂ": "True",
      "ሓሶት": "False",
      "ዋላ_ሓንቲ": "None",
      "ኣምጽእ": "import",
      "ካብ": "from",
      "ከም": "as",
      "ፈትን": "try",
      "ጌጋ": "except",
      "መወዳእታ": "finally",
      "ምስ": "with",
      "ኣቋርጽ": "break",
      "ቀጽል": "continue",
      "ሕለፍ": "pass",
      "ሓጺር": "lambda",
      "ንውሓት": "len",
      "ክልል": "range",
      "ዝርዝር": "list",
      "መዝገብ": "dict",
      "ጽሑፍ": "str",
      "ቍጽሪ": "int",
      "ልክዕ": "float",
      "ክፈት": "open",
      "ባዕለይ": "self"
    }
  },
  "wolaytta": {
    "id": 14,
    "label": "ወላይታ (Wolaytta)",
    "keywords": {
      "ኦሶ": "def",
      "ክፍሊያ": "class",
      "ጊዲኮ": "if",
      "ጊዶናሽቲን": "else",
      "ወይ_ጊዲኮ": "elif",
      "ጋካናው": "while",
      "ሁበንቶሲ": "for",
      "ጊዶን": "in",
      "ዛሮ": "return",
      "ቤሶ": "print",
      "ኦይቾ": "input",
      "ኤራ": "and",
      "ዎይኮ": "or",
      "ጊዴና": "not",
      "ቱማ": "True",
      "ዎርዶ": "False",
      "ባዋ": "None",
      "ኤሆ": "import",
      "ፔ": "from",
      "ማላ": "as",
      "ፓጮ": "try",
      "ባላ": "except",
      "ዉርሴታ": "finally",
      "ናራ": "with",
      "ቃንፆ": "break",
      "ሲንቴ": "continue",
      "አጎ": "pass",
      "ቃንፃ": "lambda",
      "ጊሳ": "len",
      "ዛሪያ": "range",
      "ዛላ": "list",
      "ማክዛባ": "dict",
      "ፃፌታ": "str",
      "ፓይዶ": "int",
      "ላካ": "float",
      "ዶዮ": "open",
      "ባና": "self"
    }
  }
};
var GEZELANG_EXAMPLES = {
  "amharic": "# ሰላም ዓለም በአማርኛ\nስራ ሰላም(ስም):\n    አሳይ(f'ሰላም፣ {ስም}!')\n    መልስ እውነት\n\nሰላም('ቻሉ')",
  "amharic_gojjam": "# የጎጃም አማርኛ\nስራ ሰላም(ስም):\n    አሳይ(f'ደህና ነሽ ወይ፣ {ስም}!')\n    መልስ እውነት\n\nሰላም('አበበ')",
  "tigrinya": "# ትግርኛ\nስራ ሰላም(ስም):\n    ኣርእይ(f'ሰላም፣ {ስም}!')\n    መልስ ሓቂ\n\nሰላም('ዮናስ')",
  "geez": "# ግዕዝ (Classical Ethiopic)\nግበር ሰላም(ስም):\n    አይድዕ(f'ሰላም ለከ፣ {ስም}!')\n    አግብእ ጽድቅ\n\nሰላም('ዳዊት')",
  "gurage": "# ጉራጊኛ\nኤፐ ሰላም(ስም):\n    አዠ(f'ሰላም፣ {ስም}!')\n    አገፓ ኤውነት\n\nሰላም('ብርሃኑ')",
  "wolaytta": "# ወላይታ\nኦሶ ሰላም(ሱማ):\n    ቤሶ(f'ሳሮ፣ {ሱማ}!')\n    ዛሮ ቱማ\n\nሰላም('ማርቆስ')",
  "silte": "# ስልጤ\nሻረ ሰላም(ስም):\n    አባላ(f'ሰላም፣ {ስም}!')\n    መለሰ ሐቅ\n\nሰላም('አሊ')",
  "harari": "# ሐረሪ\nአሻ ሰላም(ስም):\n    አግነያ(f'አማን፣ {ስም}!')\n    አግበኣ ሐቅ\n\nሰላም('አህመድ')"
};
var GEZELANG_WASM_B64 = "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swDhjIrhiLMA4YuL4YiLX+GIk+GKleGJsgDhiIHhiaDhipXhibbhiLIA4Ymj4Yut4YiyAOGKpOGJpOGIsgDhi6zhipThiaThiLIA4YiI4Yql4Yur4YqV4Yuz4YqV4YuxAOGKpeGKleGLsADhiIThi7AA4YuN4Yi14YmwAOGImOGIiOGIsADhjZPhjK4A4Yu24YuuAOGLjuGLrV/hjIrhi7Lhiq4A4YuI4YutX+GMiuGLsuGKrgDhi47hi63hiq4A4YuI4Yql4YiY4Yqg4YquAOGLjuGLrV/hi6zhipXhiq4A4Yub4YiuAOGIm+GIrgDhiqDhiLPhi60A4Yqj4Yit4Yql4YutAOGMjuGLrQDhi47hi60A4YuI4YutAOGJo+GLleGIiOGLrQDhiI3hiq0A4YiT4Yy64YitAOGKoOGKuuGIrQDhioXhjLnhiK0A4Ymg4Ym14YitAOGLreGLsOGIrQDhi7DhiaXhibDhiK0A4Yqg4Yyt4YitAOGIkOGMreGIrQDhiJ7hiq3hiK0A4YmB4Yyl4YitAOGMjeGJoOGIrQDhiJvhioXhiaDhiK0A4Yud4Yit4Yud4YitAOGMi+GIrQDhiqDhiI3hirjhipDhjIrhiK0A4YuI4YutX+GKuOGKkOGMiuGIrQDhjIjhiKwA4Yub4Yiq4YurAOGKoOGMjeGKkOGLqwDhiq3hjY3hiIrhi6sA4YiL4YqrAOGIteGIqwDhiqThiKsA4YqT4YirAOGMi+GIqwDhiY3hjL3hiKoA4YmB4Yyl4YiqAOGKquGLq+GLqADhiqXhiLXhiqgA4Yi74YioAOGKpeGIteGKq+GIqADhiJ7hiqjhiKgA4Yug4YiY4YioAOGNjOGMpgDhiqDhiI3hiaYA4YuN4Yi14YylAOGKoOGJi+GIreGMpQDhiYHhiK3hjKUA4YmB4Yio4YylAOGKo+GIneGMveGKpQDhiqDhiJ3hjL3hiqUA4Yqg4YyN4Yml4YqlAOGKquGJs+GJpQDhiq3hiLPhiaUA4Yqr4YmlAOGKkOGMpeGJpQDhiJjhi53hjIjhiaUA4Yi24YmkAOGKoOGJi+GIreGMowDhiqDhiJ3hjKMA4YuI4YutX+GKpeGKleGJsOGLteGKowDhiqDhiJ3hjKPhiqMA4Yqg4YyN4Ymg4YqjAOGKquGJs+GJowDhiYLhjKPhiaMA4Yib4Yqt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AQCSAwEAqAwBAGYKAQCOCwEAUAcBAGYLAQDqCgEAWgwBANIBAQBzDAEAlgoBAIkMAQBJBgEAWAsBAHQFAQDuCwEAAgUBAIYLAQAECQEAIgsBAMUBAQBfCwEAUwQBACYLAQDUBAEARAwBALsFAQACDAEAhQMBAF8MAQDbCQEAewsBAMgFAQAtDQEAHgIBAOILAQDtAQEAlAwBAHsEAQBTCwEAKAYBAHALAQBmAgEAiQsBAKYEAQBsCwEAQgQBAHULAQBLCQEA3QsBAJAIAQBMDAEAAAAAAAAAAAA0BQEAVgwBAKoKAQCACwEAWgYBAFMMAQDGCAEAbgwBAFMGAQBRDAEADQYBAI4MAQBxCQEAjQsBAKUGAQDaCwEArgIBAM8LAQATBAEAagsBALsBAQBCCwEAcwgBAKgMAQAuBAEAjgsBACcIAQBmCwEADAsBAFoMAQChAQEAcwwBACMDAQCJDAEA3AUBAFgLAQAXBgEA7gsBAOsGAQCGCwEA7AcBACILAQA5CgEAXwsBAPgCAQAmCwEAigIBAEQMAQDYAAEAAgwBAOUJAQBfDAEApgkBAHsLAQBJBAEALQ0BADUCAQDiCwEAAwoBAJQMAQDHBAEAUwsBACgGAQBwCwEAiAkBAIkLAQBQBQEAbAsBAM4HAQB1CwEAXAIBAN0LAQA1BAEATAwBAAAAAAAAAAAAcwEBAFYMAQAgBQEAgAsBAMYDAQBTDAEA/QcBAG4MAQC/AwEAUQwBAM4JAQCODAEANAMBAI0LAQDiBwEA2gsBAPsDAQDPCwEAegEBAGoLAQC0AAEAQgsBADsFAQCoDAEA0AMBAI4LAQCkCAEAZgsBAHcHAQBaDAEALgEBAHMMAQBHCgEAiQwBAMUKAQBYCwEAhQgBAO4LAQBfCgEAhgsBAKADAQAiCwEAUQoBAF8LAQDrAgEAJgsBAEIFAQBEDAEAuwoBAAIMAQDCAgEAXwwBAGMJAQB7CwEA8QoBAC0NAQAcAwEA4gsBAAkFAQCUDAEAWAoBAFMLAQCYBgEAcAsBAAgDAQCJCwEAJAEBAGwLAQAtBQEAdQsBAKcDAQDdCwEAvwgBAEwMAQAA3QEEbmFtZQAODWdlemVsYW5nLndhc20BpQEIABFfX3dhc21fY2FsbF9jdG9ycwEVd2FzbV9nZXRfaW5wdXRfYnVmZmVyAhZ3YXNtX2dldF9vdXRwdXRfYnVmZmVyAxN3YXNtX2dldF9vdXRwdXRfbGVuBBZ3YXNtX2dldF9kaWFsZWN0X2NvdW50BRV3YXNtX2dldF9kaWFsZWN0X25hbWUGDndhc21fdHJhbnNwaWxlBwx3YXNtX3ZlcnNpb24HEgEAD19fc3RhY2tfcG9pbnRlcgkKAQAHLnJvZGF0YQAmCXByb2R1Y2VycwEMcHJvY2Vzc2VkLWJ5AQVjbGFuZwYyMi4xLjgAlAEPdGFyZ2V0X2ZlYXR1cmVzCCsLYnVsay1tZW1vcnkrD2J1bGstbWVtb3J5LW9wdCsWY2FsbC1pbmRpcmVjdC1vdmVybG9uZysKbXVsdGl2YWx1ZSsPbXV0YWJsZS1nbG9iYWxzKxNub250cmFwcGluZy1mcHRvaW50Kw9yZWZlcmVuY2UtdHlwZXMrCHNpZ24tZXh0";
var KEYWORDS = GEZELANG_DIALECTS['amharic'].keywords;

var wasmInstance = null;
var wasmReady = false;

// Initialize native WebAssembly Core
async function initGezeLangWasm() {
    try {
        let wasmBytes;
        if (typeof window !== 'undefined' && window.fetch && location.protocol.startsWith('http')) {
            try {
                const resp = await fetch('assets/gezelang.wasm');
                if (resp.ok) {
                    const buf = await resp.arrayBuffer();
                    wasmBytes = new Uint8Array(buf);
                }
            } catch (e) {
                // fallback to inline base64
            }
        }
        if (!wasmBytes) {
            const binaryString = atob(GEZELANG_WASM_B64);
            wasmBytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                wasmBytes[i] = binaryString.charCodeAt(i);
            }
        }
        const wasmModule = await WebAssembly.instantiate(wasmBytes.buffer);
        wasmInstance = wasmModule.instance;
        wasmReady = true;
        console.log(`[GezeLang] WebAssembly Transpiler v${wasmInstance.exports.wasm_version()} loaded with ${wasmInstance.exports.wasm_get_dialect_count()} Ethiopic dialects!`);
        if (typeof onWasmLoaded === 'function') onWasmLoaded();
        return true;
    } catch (err) {
        console.warn('[GezeLang] WebAssembly initialization warning, falling back to JS scanner:', err);
        wasmReady = false;
        return false;
    }
}

// High-performance real-time transpile via WebAssembly
function transpileWithWasm(source, dialectKey) {
    if (!wasmReady || !wasmInstance) {
        return transpileWithJS(source, dialectKey);
    }
    try {
        const exports = wasmInstance.exports;
        const dialectInfo = GEZELANG_DIALECTS[dialectKey] || GEZELANG_DIALECTS['amharic'];
        const langId = dialectInfo.id;
        
        const encoder = new TextEncoder();
        const inputBytes = encoder.encode(source);
        
        const inPtr = exports.wasm_get_input_buffer();
        const mem = new Uint8Array(exports.memory.buffer);
        mem.set(inputBytes, inPtr);
        
        const outLen = exports.wasm_transpile(inputBytes.length, langId);
        const outPtr = exports.wasm_get_output_buffer();
        const outBytes = new Uint8Array(exports.memory.buffer, outPtr, outLen);
        
        const decoder = new TextDecoder('utf-8');
        return decoder.decode(outBytes);
    } catch (err) {
        console.warn('WASM execution error, falling back to JS:', err);
        return transpileWithJS(source, dialectKey);
    }
}

// JS scanner fallback
function transpileWithJS(source, dialectKey) {
    const dialect = GEZELANG_DIALECTS[dialectKey] || GEZELANG_DIALECTS['amharic'];
    const keywords = dialect.keywords;
    
    // Scan tokens and substitute keywords
    let result = source;
    for (const [kw, py] of Object.entries(keywords)) {
        const esc = kw.replace(/[/.*+?^${}()|[\]\\]/g, '\\$&');
        result = result.replace(new RegExp(`(?<![\\u1200-\\u137F\\w])${esc}(?![\\u1200-\\u137F\\w])`, 'g'), py);
    }
    return result;
}

function transpileToPreview(source, dialectKey = 'amharic') {
    return transpileWithWasm(source, dialectKey);
}

// Reverse Transpiler: Python -> Ethiopic script for selected dialect
function transpilePythonToEthiopic(pySource, dialectKey = 'amharic') {
    const dialect = GEZELANG_DIALECTS[dialectKey] || GEZELANG_DIALECTS['amharic'];
    const kws = dialect.keywords;
    const inverted = {};
    for (const [ethKw, pyKw] of Object.entries(kws)) {
        inverted[pyKw] = ethKw;
    }

    // Token pattern: string literals, comments, and Python identifier/keyword words
    const tokenPattern = /("""[\s\S]*?"""|'''[\s\S]*?'''|f?"(?:\\.|[^"\\])*"|f?'(?:\\.|[^'\\])*'|#[^\n]*|\b[a-zA-Z_]\w*\b)/g;

    return pySource.replace(tokenPattern, (match) => {
        if (match.startsWith('#') || match.startsWith('"') || match.startsWith("'") || match.startsWith('f"') || match.startsWith("f'")) {
            return match;
        }
        return inverted[match] || match;
    });
}

// Attach to globalThis / window
if (typeof globalThis !== 'undefined') {
    globalThis.GEZELANG_DIALECTS = GEZELANG_DIALECTS;
    globalThis.GEZELANG_EXAMPLES = GEZELANG_EXAMPLES;
    globalThis.transpileToPreview = transpileToPreview;
    globalThis.transpileWithWasm = transpileWithWasm;
    globalThis.transpilePythonToEthiopic = transpilePythonToEthiopic;
    globalThis.initGezeLangWasm = initGezeLangWasm;
}

// Auto-initialize WASM when loaded
if (typeof window !== 'undefined') {
    initGezeLangWasm();
}
