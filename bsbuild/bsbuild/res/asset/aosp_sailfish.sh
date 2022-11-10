function _bsbuild_envsetup() {
    lunch ${product}-${variant}
}

function _bsbuild_build_all() {
    _bsbuild_envsetup
    _bsbuild_make
}

function _bsbuild_build_otapackage() {
    _bsbuild_envsetup
    _bsbuild_make otapackage
}

function _bsbuild_build_bootimage() {
    _bsbuild_envsetup
    _bsbuild_make bootimage
}

function _bsbuild_build_systemimage() {
    _bsbuild_envsetup
    _bsbuild_make systemimage
}

function _bsbuild_build_vendorimage() {
    _bsbuild_envsetup
    _bsbuild_make vendorimage
}

function _bsbuild_build_module() {
    local modules=$*
    if [ ! -n "${modules}" ]; then
        echo "modules is null, bsbuild stopped."
        return
    fi

    _bsbuild_envsetup
    _bsbuild_ninja -f out/combined-${product}.ninja ${modules}
}
