# Debug app problems

## App crash with kivymd 2.x

- Debug steps

```bash
adb logcat -c
adb logcat -b crash -v threadtime

adb shell getprop ro.build.version.release
adb shell getprop ro.product.manufacturer
adb shell getprop ro.product.model
```

- Check the service logs

```bash
adb shell ps | grep opensms

adb logcat --pid=1234 # change the pid as shown above
```
