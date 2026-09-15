[app]
title = VideoGrab
package.name = videograb
package.domain = org.videograb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# Kivy 2.3.1 کے ساتھ مطابقت رکھنے والا لازمی ورژن
requirements = python3==3.13.9,hostpython3==3.13.9,kivy==2.3.1,pyjnius,android,certifi,charset-normalizer,idna,urllib3,requests,mutagen,yt-dlp,setuptools

orientation = portrait
fullscreen = 0

# Android 5.0 (API 21) سے لے کر جدید اینڈرائیڈ تک سپورٹ
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

# پرانے اینڈرائیڈ کے لیے لازمی اجازتیں
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO

android.allow_backup = True
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
