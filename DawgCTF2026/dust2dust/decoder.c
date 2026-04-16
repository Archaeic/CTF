#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void append_mem(char **buf, size_t *len, size_t *cap,
                       const char *src, size_t n) {
    if (*len + n + 1 > *cap) {
        size_t newcap = (*cap == 0) ? 128 : *cap;
        while (newcap < *len + n + 1) newcap *= 2;

        char *tmp = realloc(*buf, newcap);
        if (!tmp) {
            perror("realloc");
            exit(1);
        }
        *buf = tmp;
        *cap = newcap;
    }

    memcpy(*buf + *len, src, n);
    *len += n;
    (*buf)[*len] = '\0';
}

static void decode_char(unsigned char c, char top[4], char bot[4]) {
    unsigned char v = c - 0x20;   // reverse of: c = 0x20 + bin

    top[0] = ((v >> 5) & 1) ? '1' : '0';
    top[1] = ((v >> 4) & 1) ? '1' : '0';
    top[2] = ((v >> 3) & 1) ? '1' : '0';
    top[3] = '\0';

    bot[0] = ((v >> 2) & 1) ? '1' : '0';
    bot[1] = ((v >> 1) & 1) ? '1' : '0';
    bot[2] = ((v >> 0) & 1) ? '1' : '0';
    bot[3] = '\0';
}

static void flush_pair(FILE *out, char **top, size_t *tlen,
                       char **bot, size_t *blen) {
    if (*tlen == 0 && *blen == 0) return;

    fprintf(out, "%s\n%s\n", *top ? *top : "", *bot ? *bot : "");

    *tlen = 0;
    *blen = 0;
    if (*top) (*top)[0] = '\0';
    if (*bot) (*bot)[0] = '\0';
}

int main(void) {
    FILE *in = fopen("output.txt", "rb");
    FILE *out = fopen("input.txt", "wb");

    if (!in) {
        perror("fopen output.txt");
        return 1;
    }
    if (!out) {
        perror("fopen input.txt");
        fclose(in);
        return 1;
    }

    char *top = NULL, *bot = NULL;
    size_t tlen = 0, blen = 0;
    size_t tcap = 0, bcap = 0;

    int ch;
    while ((ch = fgetc(in)) != EOF) {
        if (ch == '~') {
            flush_pair(out, &top, &tlen, &bot, &blen);
            break;
        }

        if (ch == '}') {
            flush_pair(out, &top, &tlen, &bot, &blen);
            continue;
        }

        if ((unsigned char)ch < 0x20 || (unsigned char)ch > 0x5f) {
            fprintf(stderr, "Invalid encoded byte: 0x%02X\n", (unsigned char)ch);
            fclose(in);
            fclose(out);
            free(top);
            free(bot);
            return 1;
        }

        char a[4], b[4];
        decode_char((unsigned char)ch, a, b);

        append_mem(&top, &tlen, &tcap, a, 3);
        append_mem(&bot, &blen, &bcap, b, 3);
    }

    free(top);
    free(bot);
    fclose(in);
    fclose(out);
    return 0;
}
