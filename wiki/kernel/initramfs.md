



### 构造 rootfs.img

rootfs可以自定义里面的文件，这个工作量比较大。幸运的是ubuntu为我们提供了现成打包文件。下载文件（注意cpu架构）：http://cdimage.ubuntu.com/cdimage/ubuntu-base/releases/20.04/release/ubuntu-base-20.04.2-base-arm64.tar.gz 。该压缩包只包含了文件，并不是rootfs镜像，需要自己创建一个 ext4 的镜像文件，然后将压缩包中的文件拷贝到镜像文件即可。

创建一个1G大小的空白文件：

````bash
bob@bob-desktop:~/work$ dd if=/dev/zero of=rootfs.img bs=1024 count=1M
记录了1048576+0 的读入
记录了1048576+0 的写出
1073741824字节（1.1 GB，1.0 GiB）已复制，2.97299 s，361 MB/s
````

将空白文件格式化成ext4格式的镜像文件

````bash
bob@bob-desktop:~/work$ mkfs.ext4 -F -L linuxroot rootfs.img
mke2fs 1.45.5 (07-Jan-2020)
丢弃设备块： 完成                            
创建含有 262144 个块（每块 4k）和 65536 个inode的文件系统
文件系统UUID：bf6f390c-c17c-4206-b877-bdd69054a399
超级块的备份存储于下列块： 
	32768, 98304, 163840, 229376

正在分配组表： 完成                            
正在写入inode表： 完成                            
创建日志（8192 个块） 完成
写入超级块和文件系统账户统计信息： 已完成
````

挂载该镜像：

````bash
bob@bob-desktop:~/work$ sudo mkdir /mnt/image
bob@bob-desktop:~/work$ sudo mount -o loop rootfs.img /mnt/image/
bob@bob-desktop:~/work$ sudo tar zxvf ubuntu-base-20.04.2-base-arm64.tar.gz -C /mnt/image/
bob@bob-desktop:~/work$ ll /mnt/image/
总用量 84
drwxr-xr-x 18 root root  4096 4月  27 17:35 ./
drwxr-xr-x  3 root root  4096 4月  27 17:33 ../
lrwxrwxrwx  1 root root     7 2月   1 19:02 bin -> usr/bin/
drwxr-xr-x  2 root root  4096 4月  15  2020 boot/
drwxr-xr-x  2 root root  4096 2月   1 19:25 dev/
drwxr-xr-x 30 root root  4096 2月   1 19:25 etc/
drwxr-xr-x  2 root root  4096 4月  15  2020 home/
lrwxrwxrwx  1 root root     7 2月   1 19:02 lib -> usr/lib/
drwx------  2 root root 16384 4月  27 17:32 lost+found/
drwxr-xr-x  2 root root  4096 2月   1 19:02 media/
drwxr-xr-x  2 root root  4096 2月   1 19:02 mnt/
drwxr-xr-x  2 root root  4096 2月   1 19:02 opt/
drwxr-xr-x  2 root root  4096 4月  15  2020 proc/
drwx------  2 root root  4096 2月   1 19:25 root/
drwxr-xr-x  4 root root  4096 2月   1 19:02 run/
lrwxrwxrwx  1 root root     8 2月   1 19:02 sbin -> usr/sbin/
drwxr-xr-x  2 root root  4096 2月   1 19:02 srv/
drwxr-xr-x  2 root root  4096 4月  15  2020 sys/
drwxrwxrwt  2 root root  4096 2月   1 19:25 tmp/
drwxr-xr-x 10 root root  4096 2月   1 19:02 usr/
drwxr-xr-x 11 root root  4096 2月   1 19:25 var/
````

取消挂载：

````bash
bob@bob-desktop:~/work$ sudo umount -f /mnt/image 
````



````bash
mkinitramfs -o ./initramfs-$(uname -r)

bob@bob-desktop:~/work/initramfs-5.8.0-50$ cpio -idv < ../initramfs-5.8.0-50-generic 

qemu-system-x86_64 -m 1024M -smp 4 -kernel ./linux-5.12/arch/x86/boot/bzImage -append "root=/dev/sda console=ttyS0 init=/sbin/init nokaslr" -hda rootfs.img
qemu-system-x86_64 -m 1024M -smp 4 -kernel ./linux-5.12/arch/x86/boot/bzImage -append "root=/dev/sda console=ttyS0 init=/sbin/init nokaslr" -initrd initramfs-5.8.0-50-generic
qemu-system-x86_64 -m 1024M -smp 4 -kernel ./linux-5.12/arch/x86/boot/bzImage -append "root=/dev/sda console=ttyS0 nokaslr" -initrd busybox-1.33.0/build/initramfs-busybox-x86.cpio.gz
````



````bash
MKINITRAMFS(8)							mkinitramfs manual						    MKINITRAMFS(8)

NAME

       mkinitramfs - low-level tool for generating an initramfs image

SYNOPSIS

       mkinitramfs [-c compress] [-d confdir] [-k] -o outfile [-r root] [-v] [version]

       mkinitramfs [--supported-host-version= hversion]

       mkinitramfs [--supported-target-version= tversion]

DESCRIPTION

       The  mkinitramfs  script  generates an initramfs image.	The initramfs is a compressed cpio archive. The archive can be used on a different
       box of the same arch with the corresponding Linux kernel.  mkinitramfs is meant for advanced usage.  On	your  local  box  update-initramfs
       calls  mkinitramfs  with the relevant parameters.  update-initramfs keeps sha1sum of generated initramfs. It takes care to generate backups
       and eventually runs the bootloader.

       At boot time, the kernel unpacks that archive into RAM disk, mounts and uses it as initial root file system. All finding of the root device
       happens in this early userspace.

OPTIONS

	-c  compress
	      Override the COMPRESS setting in initramfs.conf.

	-d  confdir
	      Set an alternate configuration directory.

	-k    Keep the temporary directory used to make the image.

	-o  outfile
	      Write the image to outfile.

	-r  root
	      Override the ROOT setting in initramfs.conf.

	-v    Set the verbose mode output.

	version
	      Set the kernel version of the initramfs image (defaults to the running kernel).

       --supported-host-version=hversion
	      This option queries if mkinitramfs can create ramdisks on a running kernel of version hversion.

       --supported-target-version=tversion
	      This option queries if mkinitramfs can create ramdisks for kernel version tversion.

ENVIRONMENT

       mkinitramfs  honours the TMPDIR environment variable. If set, it uses subdirectories in the given directory to create its temporary working
       directories. Else it uses /tmp as default value for that purpose. The given directory should be on a filesystem which allows the  execution
       of files stored there, i.e.  should not be mounted with the noexec mount option.

FILES

       /etc/initramfs-tools/initramfs.conf
	      The default configuration file for the script. See initramfs.conf(5) for a description of the available configuration parameter.

       /etc/initramfs-tools/modules
	      Specified  modules  will be put in the generated image and loaded when the system boots. The format - one per line - is identical to
	      that of /etc/modules, which is described in modules(5).

       /etc/initramfs-tools/conf.d
	      The conf.d directory allows one to hardcode bootargs at initramfs build time via config snippets. This allows one  to  set  ROOT	or
	      RESUME.  This is especially useful for bootloaders, which do not pass an root bootarg.

       /etc/initramfs-tools/DSDT.aml
	      If this file exists, it will be appended to the initramfs in a way that causes it to be loaded by ACPI.

EXAMPLES

       Create an initramfs for current running kernel:

       mkinitramfs -o ~/tmp/initramfs-$(uname -r)

       Create an initramfs for specific kernel and keep builddirs:

       mkinitramfs -k -o ~/tmp/initramfs-2.6.21-686 2.6.21-686

       Debug initramfs creation (check out written logfile)

       sh -x mkinitramfs -o ~/tmp/initramfs-$(uname -r) 2> ~/tmp/log

AUTHOR

       The initramfs-tools are written by Maximilian Attems <maks@debian.org>, Jeff Bailey <jbailey@raspberryginger.com> and numerous others.

SEE ALSO

	initramfs.conf(5), initramfs-tools(8), update-initramfs(8).
````



















## FAQ

# [How to modify initrd initial ramdisk of Ubuntu 18.10 Cosmic Cuttlefish](https://askubuntu.com/questions/1094854/how-to-modify-initrd-initial-ramdisk-of-ubuntu-18-10-cosmic-cuttlefish)

I tried to extract the initrd `casper/initrd` of Ubuntu 18.10 and got an unexpected result. I did not see the root filesystem and files, but just a folder named `kernel`.

#### What I have done

Firstly I tried to know if I should decompress the initrd or just extract the archive directly, so I issued this command:

```
$ file initrd
initrd: ASCII cpio archive (SVR4 with no CRC)
```

#### What I got

According to the output, it should be an cpio archive and I used `cpio` to extract the archive.

```
$ cpio -id < initrd 
56 blocks
$ ls
initrd  kernel
```

If I went to have a look of the directory `kernel`, I got

```
kernel/
└── x86
    └── microcode
        └── AuthenticAMD.bin

2 directories, 1 file
```

#### What I expect

There should be files and folders like `init`, `etc`, `usr`, and so on. For example:

```
bin  conf  cryptroot  etc  init  lib  lib64  run  sbin  scripts  usr  var
```

### Answer

I figure out the initrd of Ubuntu 18.10 is archived in a different way from the previous releases. In the previous releases the initrd is usually a lzma (or gzip for much earlier releases) compressed cpio archive. The initrd of 18.10 is an archive composed of several binary files in different formats.

To dive into the archive, you may need `binwalk` (or other similar tools. You could get `binwalk` by `sudo apt install binwalk`). Once you get `binwalk`, issue the command `binwalk initrd`:

```
$ binwalk initrd

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ASCII cpio archive (SVR4 with no CRC), file name: ".", file name length: "0x00000002", file size: "0x00000000"
112           0x70            ASCII cpio archive (SVR4 with no CRC), file name: "kernel", file name length: "0x00000007", file size: "0x00000000"
232           0xE8            ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86", file name length: "0x0000000B", file size: "0x00000000"
356           0x164           ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode", file name length: "0x00000015", file size: "0x00000000"
488           0x1E8           ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode/AuthenticAMD.bin", file name length: "0x00000026", file size: "0x00006B2A"
28072         0x6DA8          ASCII cpio archive (SVR4 with no CRC), file name: "TRAILER!!!", file name length: "0x0000000B", file size: "0x00000000"
28672         0x7000          ASCII cpio archive (SVR4 with no CRC), file name: "kernel", file name length: "0x00000007", file size: "0x00000000"
28792         0x7078          ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86", file name length: "0x0000000B", file size: "0x00000000"
28916         0x70F4          ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode", file name length: "0x00000015", file size: "0x00000000"
29048         0x7178          ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode/.enuineIntel.align.0123456789abc", file name length: "0x00000036", file size: "0x00000000"
29212         0x721C          ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode/GenuineIntel.bin", file name length: "0x00000026", file size: "0x00180C00"
1605296       0x187EB0        ASCII cpio archive (SVR4 with no CRC), file name: "TRAILER!!!", file name length: "0x0000000B", file size: "0x00000000"
1605632       0x188000        LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: -1 bytes
```

You could see there are two microcode binary files and a LZMA compressed data file. The latter is what we want: the lzma compressed initrd.

Let's get the lzma compressed initrd by

>   dd if=initrd bs=1605632 skip=1 | unlzma -c | cpio -id

You will get the expected files mentioned in the questions. Edit the files you want to change. Use the following commands to repack the binary files:

>   find | cpio -H newc -o | lzma -c > initrd.partial.lz

And finally concatenate the microcode files and your new initrd (initrd.partial.lz) by

```
dd if=initrd of=initrd.microcode bs=512 count=3136
cat initrd.microcode initrd.partial.lz > initrd.new
```

Now rename `initrd.new` to be `initrd` and put it back to `casper/initrd`. You could boot your live system with your new initrd.

My answer is inspired by this post https://unix.stackexchange.com/questions/163346/why-is-it-that-my-initrd-only-has-one-directory-namely-kernel



\-----

The cpio block skip method given doesn't work reliably. That's because the initrd images I was getting myself didn't have both archives concatenated on a 512 byte boundary.

Instead, do this:

```
apt-get install binwalk
legolas [mc]# binwalk initrd.img 
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ASCII cpio archive (SVR4 with no CRC), file name: "kernel", file name length: "0x00000007", file size: "0x00000000"
120           0x78            ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86", file name length: "0x0000000B", file size: "0x00000000"
244           0xF4            ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode", file name length: "0x00000015", file size: "0x00000000"
376           0x178           ASCII cpio archive (SVR4 with no CRC), file name: "kernel/x86/microcode/GenuineIntel.bin", file name length: "0x00000026", file size: "0x00005000"
21004         0x520C          ASCII cpio archive (SVR4 with no CRC), file name: "TRAILER!!!", file name length: "0x0000000B", file size: "0x00000000"
21136         0x5290          gzip compressed data, from Unix, last modified: Sat Feb 28 09:46:24 2015
```

Use the last number (21136) which is not on a 512 byte boundary for me:

```
legolas [mc]# dd if=initrd.img bs=21136 skip=1 | gunzip | cpio -tdv | head
drwxr-xr-x   1 root     root            0 Feb 28 09:46 .
drwxr-xr-x   1 root     root            0 Feb 28 09:46 bin
-rwxr-xr-x   1 root     root       554424 Dec 17  2011 bin/busybox
lrwxrwxrwx   1 root     root            7 Feb 28 09:46 bin/sh -> busybox
-rwxr-xr-x   1 root     root       111288 Sep 23  2011 bin/loadkeys
-rwxr-xr-x   1 root     root         2800 Aug 19  2013 bin/cat
-rwxr-xr-x   1 root     root          856 Aug 19  2013 bin/chroot
-rwxr-xr-x   1 root     root         5224 Aug 19  2013 bin/cpio
-rwxr-xr-x   1 root     root         3936 Aug 19  2013 bin/dd
-rwxr-xr-x   1 root     root          984 Aug 19  2013 bin/dmesg
```

