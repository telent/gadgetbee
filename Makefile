default:
	grep FINE_LOCATION gadgetbee/android/gradle/Gadgetbee/app/src/main/AndroidManifest.xml
	nix run nixos.python37Packages.pep8 -c pep8 --show-source --show-pep8 --max-line-length=120  gadgetbee/src/gadgetbee/app.py
	docker run -it -v `pwd`:/src  beeware bash -c "cd /src/gadgetbee && briefcase build android -u"
	v=gadgetbee/android/gradle/Gadgetbee/app/build/outputs/apk/debug/app-debug.apk && adb install -r $$v
	adb shell am start-activity net.telent.gadgetbee/org.beeware.android.MainActivity

debug:
	adb logcat -s MainActivity:* stdio:* Python:* DEBUG:*
