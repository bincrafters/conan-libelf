#include <stdio.h>
#include <stdlib.h>

#include <fcntl.h>
#include <unistd.h>

#include "libelf.h"

int main(int argc , char **argv) {
    int fd;
    Elf *e;
    const char *k;
    Elf_Kind  ek;

    if (elf_version(EV_CURRENT) ==  EV_NONE) {
        printf("ELF library initialization failed: %s\n", elf_errmsg ( -1));
        return EXIT_FAILURE;
    }

#ifdef _WIN32
    return EXIT_SUCCESS;
#endif

    if ((fd = open(argv[0], O_RDONLY , 0)) < 0) {
        printf("open %s failed\n", argv [0]);
        return EXIT_FAILURE;
    }

    if ((e = elf_begin(fd, ELF_C_READ, NULL)) == NULL) {
        printf("elf_begin () failed: %s.\n", elf_errmsg ( -1));
        return EXIT_FAILURE;
    }

    ek = elf_kind(e);

    switch (ek) {
        case  ELF_K_AR:
            k = "ar(1) archive";
            break;
        case  ELF_K_ELF:
            k = "elf object";
            break;
        case  ELF_K_NONE:
            k = "data";
            break;
        default:
            k = "unrecognized";
    }

    printf("%s: %s\n", argv[0], k);
    elf_end(e);

    close(fd);

    return EXIT_SUCCESS;
}
