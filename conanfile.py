#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, CMake, tools
from conans.errors import ConanException
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
    topics = ("conan", "elf", "fsf", "libelf", "object-file")
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "cmake/CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    _autotools = None
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os != "Linux":
            del self.options.shared
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d"
        source_url = "http://www.mr511.de/software"
        try:
            tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name, self.version), sha256=sha256)
        except ConanException:
            self.output.warn("Downloding libelf from mirror")
            mirror_url = "http://repository.timesys.com/buildsources/l/libelf/{0}-{1}/{0}-{1}.tar.gz"
            tools.get(mirror_url.format(self.name, self.version), sha256=sha256, overwrite=True)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _build_cmake(self):
        shutil.copyfile(os.path.join("cmake", "CMakeLists.txt"), os.path.join(self._source_subfolder, "CMakeLists.txt"))
        cmake = self._configure_cmake()
        cmake.build()

    def _package_cmake(self):
        cmake = self._configure_cmake()
        cmake.install()

    def _configure_autotools(self):
        if not self._autotools:
            args = None
            if self.settings.os == "Linux":
                args = ["--enable-shared={}".format("yes" if self.options.shared else "no")]
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(configure_dir=self._source_subfolder, args=args)
        return self._autotools

    def _build_autotools(self):
        autotools = self._configure_autotools()
        autotools.make()

    def _package_autotools(self):
        autotools = self._configure_autotools()
        autotools.install()
        shutil.rmtree(os.path.join(self.package_folder, "share"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, "lib", "locale"), ignore_errors=True)
        if self.settings.os == "Linux" and self.options.shared:
            os.remove(os.path.join(self.package_folder, "lib", "libelf.a"))

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "lib", "Makefile.in"),
                              "$(LINK_SHLIB)",
                              "$(LINK_SHLIB) $(LDFLAGS)")
        if self.settings.os == "Windows":
            self._build_cmake()
        else:
            self._build_autotools()

    def package(self):
        self.copy(pattern="COPYING.LIB", dst="licenses", src=self._source_subfolder)
        if self.settings.os == "Windows":
            self._package_cmake()
        else:
            self._package_autotools()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
