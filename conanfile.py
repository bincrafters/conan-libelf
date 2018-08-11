#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil


class LibelfConan(ConanFile):
    name = "libelf"
    version = "0.8.13"
    description = "ELF object file access library"
    url = "https://github.com/bincrafters/conan-libelf"
    homepage = "https://directory.fsf.org/wiki/Libelf"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-2.0"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    autotools = None
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Macos":
            del self.options.shared

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "http://www.mr511.de/software"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_autotools(self):
        if not self.autotools:
            args = None
            if self.settings.os != "Macos":
                args = ['--enable-shared={}'.format('yes' if self.options.shared else 'no')]
            self.autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self.autotools.configure(configure_dir=self.source_subfolder, args=args)
        return self.autotools

    def build(self):
        autotools = self.configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING.LIB", dst="licenses", src=self.source_subfolder)
        autotools = self.configure_autotools()
        autotools.install()
        shutil.rmtree(os.path.join(self.package_folder, "share"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, "lib", "locale"), ignore_errors=True)
        if self.settings.os == "Linux" and self.options.shared:
            os.remove(os.path.join(self.package_folder, "lib", "libelf.a"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
