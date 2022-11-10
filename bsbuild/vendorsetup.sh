#!/bin/bash

if [ "-${BASH_SOURCE[0]}" != "-" ]; then
    export BS_BUILD_ROOT=$(cd "$(dirname ${BASH_SOURCE[0]})";pwd)
fi
#------------------------------------------------------------------------------
# model: bsbuild_read_cookies
# args: NONE
# describe: load out/.bsbuild/cookies.txt and create vars for each config line
# example:
#   > _bsbuild_load_from_cookies
#------------------------------------------------------------------------------
function _bsbuild_load_from_cookies() {
    cookies_path=out/.bsbuild/cookies.txt
    while read p; do
      reSec='^\[(.*)\]$'
      reNV='[ ]*([^ ]*)+[ ]*=[ ]*(.*)'  #Remove spaces around name and spaces before value
      if [[ $p =~ $reSec ]]; then
          section=${BASH_REMATCH[1]}
      elif [[ $p =~ $reNV ]]; then
        sNm=${BASH_REMATCH[1]}
        sVa=${BASH_REMATCH[2]}
        eval "$(echo "$sNm"=\""$sVa"\")"
      fi
    done < $cookies_path

    if [ "${build_log}" = "yes" ]; then
        build_log_path="out/.bsbuild/bsbuild.log"
    else
        build_log_path=""
    fi
cat << EOF
 _         _           _ _     _
| |__  ___| |__  _   _(_) | __| |
| '_ \/ __| '_ \| | | | | |/ _' |
| |_) \__ \ |_) | |_| | | | (_| |
|_.__/|___/_.__/ \__,_|_|_|\__,_|
EOF
    echo ============================================
    echo "product           =${product}"
    echo "variant           =${variant}"
    echo "vendor_variant    =${vendor_variant}"
    echo "build_thread      =${build_thread}"
    echo "factory_flag      =${factory_flag}"
    echo "build_log         =${build_log}" [${build_log_path}]
    echo "build_script_entry=${build_script_entry}"
    echo ============================================
}

function _bsbuild_log() {
    echo "[bsbuild] $*"
}
#------------------------------------------------------------------------------
# model: bsbuild
# args: [1] => IN:action command
# describe: build android for convenience
# example:
#   > bsbuild
#------------------------------------------------------------------------------
function bsbuild() {
    PYTHONDONTWRITEBYTECODE=1 python3 ${BS_BUILD_ROOT}/bsbuild/__main__.py
    if [ $? -eq 0 ]; then
        local bsbuild_path=out/.bsbuild/bsbuild.sh
        chmod a+x ${bsbuild_path}
        source ${bsbuild_path}

        _bsbuild_load_from_cookies
        ${build_script_entry}
    fi
}


function _bsbuild_ninja() {
    if [ -n "${build_log_path}" ]; then
        echo "time prebuilts/build-tools/linux-x86/bin/ninja ${build_thread} $*  2>&1 | tee $T/${build_log_path}"
        time prebuilts/build-tools/linux-x86/bin/ninja ${build_thread} $*        2>&1 | tee $T/${build_log_path}
    else
        echo time prebuilts/build-tools/linux-x86/bin/ninja ${build_thread} $*
        time prebuilts/build-tools/linux-x86/bin/ninja ${build_thread} $*
    fi
}

function _bsbuild_make() {
    if [ -n "${build_log_path}" ]; then
        echo "make ${build_thread} $*  2>&1 | tee $T/${build_log_path}"
        make ${build_thread} $*        2>&1 | tee $T/${build_log_path}
    else
        echo make ${build_thread} $*
        make ${build_thread} $*
    fi
}

function _bsbuild_mibuild() {
    if [ -n "${build_log_path}" ]; then
        echo "./mibuild.sh ${build_thread} $*  2>&1 | tee $T/${build_log_path}"
        ./mibuild.sh ${build_thread} $*        2>&1 | tee $T/${build_log_path}
    else
        echo ./mibuild.sh ${build_thread} $*
        ./mibuild.sh ${build_thread} $*
    fi
}

function _bsbuild_build() {
    if [ -n "${build_log_path}" ]; then
        echo "./build.sh $* $param_1 2>&1 | tee $T/${build_log_path}"
        ./build.sh $* $param_1       2>&1 | tee $T/${build_log_path}
    else
        echo ./build.sh $* $param_1
        ./build.sh $* $param_1
    fi
}