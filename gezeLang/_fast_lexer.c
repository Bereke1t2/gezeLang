#include <string.h>
#include <stdlib.h>

// _fast_lexer.c — High-performance native tokenizer/transpiler for Ethiopic scripts
int fast_transpile_c(const char* src, int src_len, char* dst, int dst_max, 
                     const char** kws_native, const char** kws_py, int kw_count) {
    int i = 0, o = 0;
    while (i < src_len && o < dst_max - 64) {
        // Comment: # until newline
        if (src[i] == '#') {
            while (i < src_len && src[i] != '\n' && o < dst_max - 1) {
                dst[o++] = src[i++];
            }
            continue;
        }
        
        // F-strings: e.g. f'...' or f"..."
        if ((src[i] == 'f' || src[i] == 'F') && i + 1 < src_len && (src[i+1] == '"' || src[i+1] == '\'')) {
            dst[o++] = src[i++]; // 'f'
            char quote = src[i];
            dst[o++] = src[i++]; // quote
            int in_brace = 0;
            while (i < src_len && o < dst_max - 2) {
                if (src[i] == '{') { in_brace = 1; dst[o++] = src[i++]; continue; }
                if (src[i] == '}') { in_brace = 0; dst[o++] = src[i++]; continue; }
                if (!in_brace && src[i] == quote) {
                    dst[o++] = src[i++];
                    break;
                }
                if (in_brace) {
                    // Check word inside brace
                    unsigned char c = (unsigned char)src[i];
                    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_' || c >= 0x80) {
                        int w_start = i;
                        while (i < src_len) {
                            unsigned char uc = (unsigned char)src[i];
                            if ((uc >= 'a' && uc <= 'z') || (uc >= 'A' && uc <= 'Z') || (uc >= '0' && uc <= '9') || uc == '_' || uc >= 0x80) {
                                i++;
                            } else {
                                break;
                            }
                        }
                        int w_len = i - w_start;
                        int matched = 0;
                        for (int k = 0; k < kw_count; k++) {
                            if (strncmp(&src[w_start], kws_native[k], w_len) == 0 && kws_native[k][w_len] == '\0') {
                                const char* py = kws_py[k];
                                while (*py && o < dst_max - 1) dst[o++] = *py++;
                                matched = 1;
                                break;
                            }
                        }
                        if (!matched) {
                            for (int w = 0; w < w_len && o < dst_max - 1; w++) {
                                dst[o++] = src[w_start + w];
                            }
                        }
                        continue;
                    }
                }
                if (src[i] == '\\' && i + 1 < src_len) {
                    dst[o++] = src[i++];
                }
                dst[o++] = src[i++];
            }
            continue;
        }

        // Standard string literal
        if (src[i] == '"' || src[i] == '\'') {
            char quote = src[i];
            dst[o++] = src[i++];
            while (i < src_len && src[i] != quote && src[i] != '\n' && o < dst_max - 2) {
                if (src[i] == '\\' && i + 1 < src_len) {
                    dst[o++] = src[i++];
                }
                dst[o++] = src[i++];
            }
            if (i < src_len && src[i] == quote) dst[o++] = src[i++];
            continue;
        }
        
        // Match word
        unsigned char c = (unsigned char)src[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_' || c >= 0x80) {
            int w_start = i;
            while (i < src_len) {
                unsigned char uc = (unsigned char)src[i];
                if ((uc >= 'a' && uc <= 'z') || (uc >= 'A' && uc <= 'Z') || (uc >= '0' && uc <= '9') || uc == '_' || uc >= 0x80) {
                    i++;
                } else {
                    break;
                }
            }
            int w_len = i - w_start;
            // Check keywords
            int matched = 0;
            for (int k = 0; k < kw_count; k++) {
                if (strncmp(&src[w_start], kws_native[k], w_len) == 0 && kws_native[k][w_len] == '\0') {
                    const char* py = kws_py[k];
                    while (*py && o < dst_max - 1) dst[o++] = *py++;
                    matched = 1;
                    break;
                }
            }
            if (!matched) {
                for (int w = 0; w < w_len && o < dst_max - 1; w++) {
                    dst[o++] = src[w_start + w];
                }
            }
            continue;
        }
        
        dst[o++] = src[i++];
    }
    dst[o] = '\0';
    return o;
}
