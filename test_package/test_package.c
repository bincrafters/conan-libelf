#include  <err.h>
#include  <fcntl.h>
#include  <libelf.h>
#include  <stdio.h>
#include  <stdlib.h>
#include  <unistd.h>

int main(int argc , char **argv) {
    int fd;
    Elf *e;
    char *k;
    Elf_Kind  ek;

    if (elf_version(EV_CURRENT) ==  EV_NONE)
        errx(EXIT_FAILURE , "ELF library initialization failed: %s", elf_errmsg ( -1));

    if ((fd = open(argv[0], O_RDONLY , 0)) < 0)
        err(EXIT_FAILURE , "open %s failed", argv [0]);

    if ((e = elf_begin(fd, ELF_C_READ, NULL)) == NULL)
        errx(EXIT_FAILURE , "elf_begin () failed: %s.", elf_errmsg ( -1));

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

    (void) printf("%s: %s\n", argv[0], k);
    (void) elf_end(e);
    (void) close(fd);

    return EXIT_SUCCESS;
}
