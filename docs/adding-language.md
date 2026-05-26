# Adding a Language

GezeLang's Plugin Architecture makes it easy to add support for any language natively in just a few steps. Everything works purely via mapping configurations.

## Step 1: Create an Adapter Directory
Go to the `adapters` directory and create a new folder for the language.
```bash
mkdir -p adapters/oromo
```

## Step 2: Create keywords.json
Inside the new directory, create a `keywords.json` file spanning all keyword categories.
```json
{
    "definitions": {
        "def": "hojii",
        "class": "kutaa",
        "return": "deebisi",
        "lambda": "gabaabaa"
    }
}
```
Ensure that all 37 keys exist. You can duplicate from `adapters/amharic/keywords.json`.

## Step 3: Test and Integrate
Create a test case for your new language to ensure that your lexer picks up the right tokens. After completing the words mapping, run:
```bash
python translator.py --lang oromo test_file.ext
```

## Step 4: PR to Main Repository
We welcome contributions for Tigrinya, Guragigna, Somali and more! Make sure tests pass before opening a Pull Request.
