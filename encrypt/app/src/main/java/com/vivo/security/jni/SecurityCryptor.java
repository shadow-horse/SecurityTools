package com.vivo.security.jni;

import android.content.Context;
import android.widget.TableRow;

import java.io.FileDescriptor;

public class SecurityCryptor
{
    static boolean  isFlag = true;
    static
    {
        try
        {
            System.loadLibrary("vivosgmain");
        }
        catch (Throwable localThrowable)
        {
            isFlag = false;
        }
    }

    public boolean isSuccess()
    {
        return isFlag;
    }

    public static native byte[] nativeAesEncrypt(byte[] paramArrayOfByte, int paramInt);

    public static native byte[] nativeBase64Decrypt(byte[] paramArrayOfByte);

    public static native byte[] nativeBase64Encrypt(byte[] paramArrayOfByte);

    public static native int nativeSecurityInit(Context paramContext, FileDescriptor paramFileDescriptor, long paramLong1, long paramLong2);

    public static native long nativeWaveStringNet(String paramString);
}
