/**
 *  Xposed的入口类
 *  2018.09.23
 */
package com.snow.xposed.HookClass;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

public class MainXposed implements IXposedHookLoadPackage{

    public final static String TAG = "MainXposed";
    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        //Log打印加载的App package
        XposedBridge.log(TAG+"|"+"LoadPackageName:"+lpparam.packageName);
    }
}
