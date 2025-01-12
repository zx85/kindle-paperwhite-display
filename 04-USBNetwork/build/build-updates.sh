#!/bin/bash -e
#
# $Id: build-updates.sh 19282 2023-10-31 00:10:35Z NiLuJe $
#

HACKNAME="usbnet"
HACKDIR="USBNetwork"
PKGNAME="${HACKNAME}"
PKGVER="0.22.N"

# Setup KindleTool packaging metadata flags to avoid cluttering the invocations
PKGREV="$(svnversion -c .. | awk '{print $NF}' FS=':' | tr -d 'P')"
KT_PM_FLAGS=( "-xPackageName=${HACKDIR}" "-xPackageVersion=${PKGVER}-r${PKGREV}" "-xPackageAuthor=NiLuJe" "-xPackageMaintainer=NiLuJe" "-X" )

# We need kindletool (https://github.com/NiLuJe/KindleTool) in $PATH
if (( $(kindletool version | wc -l) == 1 )) ; then
	HAS_KINDLETOOL="true"
fi

if [[ "${HAS_KINDLETOOL}" != "true" ]] ; then
	echo "You need KindleTool (https://github.com/NiLuJe/KindleTool) to build this package."
	exit 1
fi

# We also need GNU tar
if [[ "$(uname -s)" == "Darwin" ]] ; then
	TAR_BIN="gtar"
else
	TAR_BIN="tar"
fi
if ! ${TAR_BIN} --version | grep -q "GNU tar" ; then
	echo "You need GNU tar to build this package."
	exit 1
fi

# Go away if we don't have the PW2 tree checked out for the A9 binaries...
if [[ ! -d "../../../PW2_Hacks" ]] ; then
	echo "Skipping USBNetwork build, we're missing the A9 binaries (from the PW2_Hacks tree)"
	exit 1
fi

# Go away if we don't have the USBNetwork tree for the legacy version checked out...
if [[ ! -d "../../../Hacks/USBNetwork" ]] ; then
	echo "Skipping USBNetwork build, we're missing the KUAL extension (from the Hacks tree)"
	exit 1
fi

# Pickup our common stuff... We leave it in our staging wd so it ends up in the source package.
if [[ ! -d "../../Common" ]] ; then
	echo "The tree isn't checked out in full, missing the Common directory..."
	exit 1
fi
# LibOTAUtils 5
ln -f ../../Common/lib/libotautils5 ./libotautils5
# XZ Utils
ln -f ../../Common/bin/xzdec ./xzdec
# LibKH 5
for common_lib in libkh5 ; do
	ln -f ../../Common/lib/${common_lib} ../src/${HACKNAME}/bin/${common_lib}
done

# Make sure we bundle our KUAL extension...
cp -avf ../../../Hacks/USBNetwork/src/extensions ../src/


## Install

# Archive custom directory
export XZ_DEFAULTS="-T 0"
${TAR_BIN} --hard-dereference --owner root --group root --exclude-vcs -cvJf ${HACKNAME}.tar.xz ../src/${HACKNAME} ../src/extensions

# Copy the script to our working directory, to avoid storing crappy paths in the update package
ln -f ../src/install.sh ./
ln -f ../src/usbnet.conf ./
ln -f ../src/usbnet-preinit.conf ./

# Build the install package (Touch & PaperWhite)
kindletool create ota2 "${KT_PM_FLAGS[@]}" -d touch -d paperwhite libotautils5 install.sh ${HACKNAME}.tar.xz xzdec usbnet-preinit.conf usbnet.conf Update_${PKGNAME}_${PKGVER}_install_touch_pw.bin

# Remove the Touch & PaperWhite archive
rm -f ./${HACKNAME}.tar.xz

# Build the PaperWhite 2 archive...
${TAR_BIN} --hard-dereference --owner root --group root --exclude-vcs -cvf ${HACKNAME}.tar ../src/${HACKNAME} ../src/extensions
# Delete A8 binaries
KINDLE_MODEL_BINARIES="bin/busybox bin/dropbearmulti bin/htop bin/kindletool bin/kindle_usbnet_addr bin/lsof bin/mosh-client bin/mosh-server bin/rsync bin/scp bin/sftp bin/ssh bin/ssh-add bin/ssh-agent bin/sshfs bin/ssh-keygen bin/ssh-keyscan lib/libcrypto.so.1.1 lib/libssl.so.1.1 libexec/sftp-server libexec/ssh-keysign libexec/ssh-pkcs11-helper libexec/ssh-sk-helper sbin/sshd bin/fbgrab bin/strace bin/eu-nm bin/eu-objdump bin/eu-readelf bin/eu-strings bin/ltrace lib/libasm.so.1 lib/libdw.so.1 lib/libelf.so.1 lib/libz.so.1 lib/libpng16.so.16 lib/libncurses.so.6 lib/libtinfo.so.6 lib/libncursesw.so.6 lib/libtinfow.so.6 lib/libunwind-arm.so.8 lib/libunwind-ptrace.so.0 lib/libunwind.so.8 bin/nano bin/zsh lib/libmagic.so.1 lib/libpcre.so.1 lib/libpcreposix.so.0"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/zsh/attr.so lib/zsh/cap.so lib/zsh/clone.so lib/zsh/compctl.so lib/zsh/complete.so lib/zsh/complist.so lib/zsh/computil.so lib/zsh/curses.so lib/zsh/datetime.so lib/zsh/deltochar.so lib/zsh/example.so lib/zsh/files.so lib/zsh/langinfo.so lib/zsh/mapfile.so lib/zsh/mathfunc.so lib/zsh/nearcolor.so lib/zsh/newuser.so lib/zsh/parameter.so lib/zsh/pcre.so lib/zsh/regex.so lib/zsh/rlimits.so lib/zsh/sched.so lib/zsh/stat.so lib/zsh/system.so lib/zsh/termcap.so lib/zsh/terminfo.so lib/zsh/zftp.so lib/zsh/zleparameter.so lib/zsh/zle.so lib/zsh/zprof.so lib/zsh/zpty.so lib/zsh/zselect.so lib/zsh/zutil.so lib/zsh/net/socket.so lib/zsh/net/tcp.so lib/zsh/param/private.so"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/b2sum bin/dircolors bin/ag lib/libevent-2.1.so.7 lib/libevent_core-2.1.so.7 lib/libevent_extra-2.1.so.7 lib/libevent_openssl-2.1.so.7 lib/libevent_pthreads-2.1.so.7 bin/tmux bin/gdb bin/gdbserver bin/objdump bin/gprof bin/fbink bin/fbdepth"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/curl lib/libcurl.so.4 bin/evtest lib/libevdev.so.2 bin/evemu-describe bin/evemu-device bin/evemu-event bin/evemu-play bin/evemu-record lib/libevemu.so.3"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/scanelf lib/libpcre2-8.so.0 lib/libpcre2-posix.so.3 bin/less bin/lessecho bin/lesskey"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/libbfd-2.37.so lib/libctf-nobfd.so.0 lib/libctf.so.0 lib/libopcodes-2.37.so"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/libsmartcols.so.1 lib/libmount.so.1 lib/libblkid.so.1 sbin/blkid bin/lsblk bin/choom bin/lsipc bin/lslocks"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/jq"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/libexpat.so.1 lib/libzstd.so.1 lib/liblz4.so.1 lib/libarchive.so.13 bin/bsdtar"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/libxxhash.so.0"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/libreadline.so.8"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/openssl"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/lftp"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/tree"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/file"
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} bin/dtc"
for my_bin in ${KINDLE_MODEL_BINARIES} ; do
	${TAR_BIN} --delete -vf ${HACKNAME}.tar src/${HACKNAME}/${my_bin}
done
# Those are PW2-only...
KINDLE_MODEL_BINARIES="${KINDLE_MODEL_BINARIES} lib/traceevent/plugins/plugin_cfg80211.so lib/traceevent/plugins/plugin_function.so lib/traceevent/plugins/plugin_hrtimer.so lib/traceevent/plugins/plugin_jbd2.so lib/traceevent/plugins/plugin_kmem.so lib/traceevent/plugins/plugin_kvm.so lib/traceevent/plugins/plugin_mac80211.so lib/traceevent/plugins/plugin_sched_switch.so lib/traceevent/plugins/plugin_scsi.so lib/traceevent/plugins/plugin_xen.so lib/traceevent/plugins/plugin_futex.so lib/traceevent/plugins/plugin_tlb.so"
# Append A9 binaries
for my_bin in ${KINDLE_MODEL_BINARIES} ; do
	${TAR_BIN} --hard-dereference --owner root --group root --transform "s,^PW2_Hacks/${HACKDIR}/,,S" --show-transformed-names -rvf ${HACKNAME}.tar ../../../PW2_Hacks/${HACKDIR}/src/${HACKNAME}/${my_bin}
done
# xz it...
xz ${HACKNAME}.tar

# Speaking of, we need our own xzdec binary, too!
ln -f ../../../PW2_Hacks/Common/bin/xzdec ./xzdec

# Build the install package (>= Wario)
kindletool create ota2 "${KT_PM_FLAGS[@]}" -d paperwhite2 -d basic -d voyage -d paperwhite3 -d oasis -d basic2 -d oasis2 -d paperwhite4 -d basic3 -d oasis3 -d paperwhite5 -d basic4 -d scribe libotautils5 install.sh ${HACKNAME}.tar.xz xzdec usbnet-preinit.conf usbnet.conf Update_${PKGNAME}_${PKGVER}_install_pw2_and_up.bin

## Uninstall
# Copy the script to our working directory, to avoid storing crappy paths in the update package
ln -f ../src/uninstall.sh ./

# Build the uninstall package
kindletool create ota2 "${KT_PM_FLAGS[@]}" -d kindle5 libotautils5 uninstall.sh Update_${PKGNAME}_${PKGVER}_uninstall.bin

## Cleanup
# Remove package specific temp stuff
rm -f ./install.sh ./uninstall.sh ./${HACKNAME}.tar.xz ./xzdec ./usbnet-preinit.conf ./usbnet.conf

# Move our updates
mv -f *.bin ../
