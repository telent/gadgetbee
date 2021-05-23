MANIFEST=gadgetbee/android/gradle/Gadgetbee/app/src/main/AndroidManifest.xml
PERMISSIONS_KT=gadgetbee/android/gradle/Gadgetbee/app/src/main/java/org/beeware/android/Permissions.kt

XML=$(shell nix-build '<nixpkgs>' -A xmlstarlet)/bin/xml

$(PERMISSIONS_KT): Permissions.kt
	cp $< $@

default: $(PERMISSIONS_KT)
	grep FINE_LOCATION $(MANIFEST) || ( $(XML) ed -s //manifest -t elem -n uses-permission  < $(MANIFEST) | $(XML) ed -s '//manifest/uses-permission[not(@android:name)]' --type attr -n android:name -v android.permission.ACCESS_FINE_LOCATION > $$ && mv $$ $(MANIFEST))
	nix run nixos.python37Packages.pep8 -c pep8 --show-source --show-pep8 --max-line-length=120  gadgetbee/src/gadgetbee/app.py
	docker run -it -v `pwd`:/src  beeware bash -c "cd /src/gadgetbee && briefcase build android -u"
	v=gadgetbee/android/gradle/Gadgetbee/app/build/outputs/apk/debug/app-debug.apk && adb install -r $$v
	adb shell am start-activity net.telent.gadgetbee/org.beeware.android.MainActivity

debug:
	adb logcat -s MainActivity:* stdio:* Python:* DEBUG:*
