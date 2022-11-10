#==============================================================================
# file: kaiser.sh
# author: bob
# version: 0.1
# describe:
#   library of bsbuild script
# global variable:
#   ${product}
#   ${variant}
#   ${vendor_variant}
#   ${build_thread}
#   ${factory_flag}
# eg.:
#   > n/a
#==============================================================================

#------------------------------------------------------------------------------
# func: _bsbuild_envsetup
# args: [1] => IN:product name for lunch. eg. missi, kaiser, qssi etc.
# describe: envsetup for current build
# eg.:
#   > _bsbuild_envsetup missi
#------------------------------------------------------------------------------
function _bsbuild_envsetup() {
    lunch ${product}-${variant}
}

function _bsbuild_build_all() {
    _bsbuild_envsetup
    _bsbuild_make
}

function _bsbuild_build_bootimage() {
    _bsbuild_envsetup
    _bsbuild_make bootimage
}

function _bsbuild_build_systemimage() {
    _bsbuild_envsetup
    _bsbuild_make systemimage
}

function _bsbuild_build_system_module() {
    local modules=$*
    if [ ! -n "${modules}" ]; then
        echo "modules is null, bsbuild stopped."
        return
    fi

    _bsbuild_envsetup
    _bsbuild_ninja -f out/combined-aosp_x86_64.ninja ${modules}
}
