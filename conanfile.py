#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, CMake, tools
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
    exports_sources = ["CMakeLists.txt", "cmake/CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    autotools = None
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

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

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build_cmake(self):
        shutil.copyfile(os.path.join("cmake", "CMakeLists.txt"), os.path.join(self.source_subfolder, "CMakeLists.txt"))
        shutil.move(os.path.join(self.source_subfolder, "lib", "sys_elf.h.w32"), os.path.join(self.source_subfolder, "lib", "sys_elf.h"))
        cmake = self.configure_cmake()
        cmake.build()

    def package_cmake(self):
        cmake = self.configure_cmake()
        cmake.install()

    def configure_autotools(self):
        if not self.autotools:
            args = None
            if self.settings.os != "Macos":
                args = ['--enable-shared={}'.format('yes' if self.options.shared else 'no')]
            self.autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self.autotools.configure(configure_dir=self.source_subfolder, args=args)
        return self.autotools

    def build_autotools(self):
        autotools = self.configure_autotools()
        autotools.make()

    def package_autotools(self):
        autotools = self.configure_autotools()
        autotools.install()
        shutil.rmtree(os.path.join(self.package_folder, "share"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, "lib", "locale"), ignore_errors=True)
        if self.settings.os == "Linux" and self.options.shared:
            os.remove(os.path.join(self.package_folder, "lib", "libelf.a"))

    def build(self):
        if self.settings.os == "Windows":
            self.build_cmake()
        else:
            self.build_autotools()

    def package(self):
        self.copy(pattern="COPYING.LIB", dst="licenses", src=self.source_subfolder)
        if self.settings.os == "Windows":
            self.package_cmake()
        else:
            self.package_autotools()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
