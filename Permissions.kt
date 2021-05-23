package org.beeware.android

import android.app.Activity
import androidx.core.app.ActivityCompat

fun requestPermission(activity : Activity, permission : String, requestCode : Int) {
    return ActivityCompat.requestPermissions(activity, arrayOf(permission), requestCode);
}
