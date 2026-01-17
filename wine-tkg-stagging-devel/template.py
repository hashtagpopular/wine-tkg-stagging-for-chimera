pkgname = "wine-tkg-stagging"
pkgver = "11.0.10" # Updated to latest stable as of Jan 2026
pkgrel = 0
archs = ["aarch64", "x86_64"]
build_style = "gnu_configure"
configure_args = [
    "--disable-tests",
    "--enable-tools",
    "--enable-win64",
    "--without-ldap",        # From your Alpine script
    "--without-oss",         # From your Alpine script
    "--disable-winemenubuilder", # From your Alpine script
   # "--disable-win16",       # From your Alpine script
]
make_install_args = [
    "STRIP=true",
    "STRIPPROG=true",
]
hostmakedepends = [
    "automake",
    "bison",
    "flex",
    "perl",
    "pkgconf",
    "python",
]
# Combined dependencies from both your Alpine script and existing Chimera template
makedepends = [
    "alsa-lib-devel",
    "cups-devel",
    "dbus-devel",
    "ffmpeg-devel",
    "fontconfig-devel",
    "freetype-devel",
    "gettext",
    "gnutls-devel",
    "gst-plugins-base-devel",
    "libgphoto2-devel",
    "libpcap-devel",
    "libpulse-devel",
    "libusb-devel",
    "libxcomposite-devel",
    "libxcursor-devel",
    "libxi-devel",
    "libxinerama-devel",
    "libxrandr-devel",
    "libxrender-devel",
    "mesa-devel",
    "ncurses-devel",
    "ocl-icd-devel",
    "pcsc-lite-devel",
    "samba-devel",
    "sane-backends-devel",
    "sdl2-compat-devel",
    "udisks-devel",
    "v4l-utils-devel",
    "vulkan-loader-devel",
    "wayland-devel",
]
depends = ["libxrandr"]
pkgdesc = "Compatibility layer for running Windows programs on Linux"
subdesc = "Wine with TkG and Staging patches for musl (Chimera Linux)"
license = "LGPL-2.1-or-later"
url = "https://github.com/Kron4ek/wine-tkg"

# Using Kron4ek's wine-tkg source which contains pre-patched staging-tkg source
source = f"https://github.com/Kron4ek/wine-tkg/archive/refs/tags/11.0.tar.gz"
sha256 = "f6a6f75cda4383612fd22681224518e1fc48cb3f24eb65241eab1afa5c297950"
tool_flags = {
    "CFLAGS": [
        "-march=znver3",
        "-mtune=znver3",
        "-O3",
  #      "-flto=thin",
    ],
    "CXXFLAGS": [
        "-march=znver3",
        "-mtune=znver3",
        "-O3",
       # "-flto=thin",
    ]
  #  "LDFLAGS": ["-flto=thin"],
}
#def init_configure(self):
    # To fix the "relocation R_X86_64_32 out of range" error:
    # We must ensure the preloader is NOT built with LTO.
    # We use the Wine build system's own variables to force no-LTO for the loader.
  #  self.make_env["loader_LDFLAGS"] = "-fno-lto -Wl,-no-pie"
   # self.make_env["preloader_LDFLAGS"] = "-fno-lto -Wl,-no-pie"
# Hardening remains disabled as per your original template for loader compatibility
hardening = ["!int", "!var-init"]
options = ["!lto", "!check"]

match self.profile().arch:
    case "x86_64":
        configure_args += ["--enable-archs=x86_64,"]

def pre_configure(self):
    # From your Alpine script: trigger Wine's internal generators before configure
#self.do("python3", "dlls/winevulkan/make_vulkan")
 #   self.do("./tools/make_requests")
    self.do("./tools/make_specfiles")
    self.do("autoreconf", "-f")

def post_install(self):
    self.install_link("usr/bin/wine64", "wine")

def _(self):
    self.depends += [f"{pkgname}={pkgver}-r{pkgrel}"]
    # llvm-strip/objcopy cannot handle windows .a's
    self.nostrip_files = [
        "usr/lib/wine/*-*/*.a",
    ]
    return self.default_devel(
        extra=[
            "usr/bin/function_grep.pl",
            "usr/bin/widl",
            "usr/bin/winebuild",
            "usr/bin/winecpp",
            "usr/bin/winedbg",
            "usr/bin/winedump",
            "usr/bin/wineg++",
            "usr/bin/winegcc",
            "usr/bin/winemaker",
            "usr/bin/wmc",
            "usr/bin/wrc",
            "usr/lib/wine/*-*/*.a",
        ]
    )
