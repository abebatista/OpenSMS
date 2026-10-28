package in.daslearning.opensms;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class StopServiceReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        String serviceClass =
            intent.getStringExtra("service_class");

        if (serviceClass == null) {
            return;
        }

        Intent serviceIntent = new Intent();
        serviceIntent.setClassName(
            context.getPackageName(),
            serviceClass
        );

        context.stopService(serviceIntent);
    }
}
