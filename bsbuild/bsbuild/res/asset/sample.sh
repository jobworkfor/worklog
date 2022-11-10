function _bsbuild_envsetup() {
    local lunch_product=$1

    export SKIP_DOWNLOAD_DECOUPLED_APPS=true
    export SKIP_DOWNLOAD_VENDOR_GOOGLE_APPS=true
    export SKIP_DOWNLOAD_CUST_APPS=true
    export XMS_BULDER_DISABLED=true
    export DISABLE_XIAOMI_SIGNER=true
    export BUILD_TARGET_PRODUCT=${product}
    export DISABLE_XIAOMI_SEC_SIGNER=true

    # check if factory build
    if [ "${factory_flag}" = "yes" ]; then
        export FACTORY_BUILD=1
    else
        export FACTORY_BUILD=0
    fi

    lunch ${lunch_product}-${variant}
    deploy ${vendor_variant}
}

function _bsbuild_build_all() {
    _bsbuild_envsetup ${product}
    _bsbuild_build dist
}

function _bsbuild_build_bootimage() {
    _bsbuild_envsetup ${product}
    _bsbuild_make bootimage
}

function _bsbuild_build_systemimage() {
    _bsbuild_envsetup qssi
    _bsbuild_make systemimage
}

function _bsbuild_build_vendorimage() {
    _bsbuild_envsetup ${product}
    _bsbuild_make
}

function _bsbuild_build_system_module() {
    local modules=$*
    if [ ! -n "${modules}" ]; then
        _bsbuild_log "modules is null, bsbuild stopped."
        return
    fi

    _bsbuild_envsetup qssi
    _bsbuild_ninja -f out/combined-qssi.ninja ${modules}
}

function _bsbuild_build_vendor_module() {
    local modules=$*
    if [ ! -n "${modules}" ]; then
        _bsbuild_log "modules is null, bsbuild stopped."
        return
    fi

    _bsbuild_envsetup ${product}
    _bsbuild_ninja -f out/combined-penrose.ninja ${modules}
}

