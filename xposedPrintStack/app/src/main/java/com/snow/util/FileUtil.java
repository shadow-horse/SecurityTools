package com.snow.util;

import android.os.Environment;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.OutputStreamWriter;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;

/**
 * 文件操作类
 */
public class FileUtil {

    public static void writeToFile(String data,FileType ft)
    {
        data = data + "\r\n";
        try{
            String absolutePath = Environment.getExternalStorageDirectory().getAbsolutePath()+Config.P_ROOT+"/"+Config.SP_PACKAGE;
            boolean append =  true;
            if(ft!=null)
            {
                switch (ft)
                {
                    case ACTIVITY:
                        absolutePath += Config.ACTIVITY;
                        break;
                    case LOADCLASS:
                        absolutePath += Config.LOADCLASS;
                        break;
                    case ONCLICK:
                        absolutePath += Config.ONCLICK;
                        break;
                    default:

                }
                File file = new File(absolutePath);
                if (!file.exists()) {

                    File path = new File(String.valueOf(file.getParentFile()));
                    path.setReadable(true, false);
                    path.setExecutable(true, false);
                    path.setWritable(true, false);

                    path.mkdirs();
                    path.setReadable(true, false);
                    path.setExecutable(true, false);
                    path.setWritable(true, false);

                    file.createNewFile();

                    file.setReadable(true, false);
                    file.setExecutable(true, false);
                    file.setWritable(true, false);

                }

                FileOutputStream fos = new FileOutputStream(file,append);
                OutputStreamWriter osw = new OutputStreamWriter(fos);
                osw.write(data);
                osw.close();
                fos.close();

            }
        }catch (Exception e)
        {
            e.printStackTrace();
        }

    }

    public static String readFromFile(FileType ft)
    {
        String data="";
        try{

            String absolutePath = Environment.getExternalStorageDirectory().getAbsolutePath()+Config.P_ROOT+"/"+Config.SP_PACKAGE;
            if(ft!=null) {
                switch (ft) {
                    case ACTIVITY:
                        absolutePath += Config.ACTIVITY;
                        break;
                    case LOADCLASS:
                        absolutePath += Config.LOADCLASS;
                        break;
                    case ONCLICK:
                        absolutePath += Config.ONCLICK;
                        break;
                    default:

                }

                data = "FilePath:"+absolutePath+"\r\n";

                File file = new File(absolutePath);
                String text ="";
                if(file.exists())
                {
                    if (file.length() > 1048576) {
                        RandomAccessFile aFile = new RandomAccessFile(absolutePath, "r");
                        FileChannel inChannel = aFile.getChannel();
                        ByteBuffer buffer = ByteBuffer.allocate(1048576); //1MB
                        while (inChannel.read(buffer) > 0) {
                            buffer.flip();

                            String charsetName = "UTF-8";
                            CharBuffer cb = Charset.forName(charsetName).decode(buffer);
                            text = cb.toString();

                            buffer.clear();
                        }
                        inChannel.close();
                        aFile.close();

                    } else {
                        FileInputStream f = new FileInputStream(absolutePath);
                        FileChannel ch = f.getChannel();
                        MappedByteBuffer mbb = ch.map(FileChannel.MapMode.READ_ONLY, 0L, ch.size());

                        while (mbb.hasRemaining()) {
                            String charsetName = "UTF-8";
                            CharBuffer cb = Charset.forName(charsetName).decode(mbb);
                            text = cb.toString();
                        }
                    }
                    data = data + text;
                }else{
                    data = data + "File does not exist.\r\n";
                }
            }

        }catch (Exception e){
            e.printStackTrace();
            data = "Read files occur exception.\r\n";
        }

        return data;
    }

    public static String deleteFiles()
    {
        String strlog ="";
        String absolutePath = Environment.getExternalStorageDirectory().getAbsolutePath()+Config.P_ROOT+"/"+Config.SP_PACKAGE;
        File fileDir = new File(absolutePath);
        if(fileDir.isDirectory())
        {
            File files[] = fileDir.listFiles();
            if(files != null)
            {
                for (File file:files)
                {
                    strlog =strlog + "Delete file "+file.getAbsolutePath() + "\r\n";
                    file.delete();
                }
            }
        }
        return strlog;
    }

}
