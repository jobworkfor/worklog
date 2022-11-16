//
// Created by bob.shen on 4/19/16.
//

#ifndef ANDROID_6_0_HELLO_H
#define ANDROID_6_0_HELLO_H

#include <linux/cdev.h>
#include <linux/semaphore.h>

#define HELLO_DEVICE_NODE_NAME  "hello"
#define HELLO_DEVICE_FILE_NAME  "hello"
#define HELLO_DEVICE_PROC_NAME  "hello"
#define HELLO_DEVICE_CLASS_NAME "hello"

struct hello_android_dev {
    int val;
    struct semaphore sem;
    struct cdev dev;
};

#endif //ANDROID_6_0_HELLO_H
