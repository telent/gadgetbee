"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from rubicon.java import JavaClass, JavaInterface, JavaProxy
from rubicon.java.jni import java

LocationListener = JavaInterface("android/location/LocationListener")


class LocListener(LocationListener):
    def __init__(self):
        super().__init__()
        self._methods["hashCode"] = {tuple()}

    def onFlushComplete(self, code):
        print(f"{code} flush")
        return 0

    def onProviderDisabled(self, provider):
        print(f"{provider} disabled")
        return 0

    def onProviderEnabled(self, provider):
        print(f"{provider} enabled")
        return 0

    def onStatusChanged(self, status, extras, mystery):
        print(f"status {status} {extras} {mystery}")
        return 0

    def onLocationChanged(self, location):
        print(f"location {location}")
        if location is not None:
            # self.locationHolder.latitude = location.getLatitude()
            # self.locationHolder.longitude = location.getLongitude()
            print(location)
        return 0

    def hashCode(self):
        print("hash")
        return 1


class Gadgetbee(toga.App):

    LocationManager = JavaClass("android/location/LocationManager")

    def ensureLocationPermission(self, activity, code):
        ContextCompat = JavaClass('androidx/core/content/ContextCompat')
        ActivityCompat = JavaClass('androidx/core/app/ActivityCompat')
        Permissions = JavaClass('org/beeware/android/PermissionsKt')
        Manifest = JavaClass('android/Manifest')
        permission = JavaClass('android/Manifest$permission')
        GRANTED = JavaClass('android/content/pm/PackageManager').PERMISSION_GRANTED
        if ContextCompat.checkSelfPermission(activity, "android.permission.ACCESS_FINE_LOCATION") != GRANTED:
            perms = permission.ACCESS_FINE_LOCATION
            if ActivityCompat.shouldShowRequestPermissionRationale(activity,
                                                                   permission.ACCESS_FINE_LOCATION):
                Permissions.requestPermission(activity, perms, code)
            else:
                Permissions.requestPermission(activity, perms, code)

    def pollLocation(self):
        location = self.locationManager.getLastKnownLocation(self.LocationManager.GPS_PROVIDER)
        if location is not None:
            self.latitude = location.getLatitude()
            self.longitude = location.getLongitude()
            print(location)

    def startLocationReporting(self, context):
        global loclistener
        print("service", JavaClass("android/app/Service"))
        loc_service = JavaClass("android/content/Context").LOCATION_SERVICE
        print("loc constant", loc_service)
        t = context.getSystemService(loc_service)
        # NewGlobalRef used here to cast the Object to a LocationManager
        self.locationManager = self.LocationManager(__jni__=java.NewGlobalRef(t))
        self.locListener = LocListener()
        self.pollLocation()

        self.locationManager.requestLocationUpdates(self.LocationManager.GPS_PROVIDER,
                                                    1000, 1.0,
                                                    self.locListener)

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        Intent = JavaClass('android/content/Intent')
        Uri = JavaClass('android/net/Uri')
        activity = JavaClass('org/beeware/android/MainActivity').singletonThis
        name_label = toga.Label("HI", style=Pack(padding=(0, 5)))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)

        button = toga.Button(
            'Where am I?',
            on_press=self.say_hello,
            style=Pack(padding=5)
        )
        main_box.add(name_box)
        main_box.add(button)

        self.ensureLocationPermission(activity, 1)
        self.startLocationReporting(activity)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def say_hello(self, widget):
        self.pollLocation()
        print(self.locListener._methods)
        self.main_window.info_dialog(
            'Hi there!',
            f"lat {self.latitude} lon {self.longitude}"
        )


def main():
    return Gadgetbee()
