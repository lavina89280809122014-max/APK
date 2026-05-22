[app]
title = Phone Camera
package.name = phonecamera
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.3.0,flask,zeroconf

orientation = portrait
fullscreen = 1

android.permissions = CAMERA,INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 29
