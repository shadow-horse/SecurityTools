package com.snow.xposedprintstack;

import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.snow.util.FileType;
import com.snow.util.FileUtil;

public class MainActivity extends AppCompatActivity {

    public Button b_activity;
    public Button b_onclick;
    public Button b_class;
    public Button b_clear;

    public TextView t_showlog;

    public Handler logHandler;
    public boolean isReadinglog = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        b_activity = findViewById(R.id.b_activity);
        b_onclick = findViewById(R.id.b_onclick);
        b_class = findViewById(R.id.b_class);
        b_clear = findViewById(R.id.b_clear);
        t_showlog = findViewById(R.id.t_showlog);

        logHandler = new myHandler();

        b_activity.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isReadinglog)
                {
                    Toast.makeText(MainActivity.this,"Please Waite,Log is Reading now.",Toast.LENGTH_SHORT).show();
                    return;
                }
                isReadinglog = true;
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String str = FileUtil.readFromFile(FileType.ACTIVITY);
                        Message msg = new Message();
                        msg.obj = str;
                        logHandler.sendMessage(msg);
                    }
                }).start();
            }
        });

        b_class.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isReadinglog)
                {
                    Toast.makeText(MainActivity.this,"Please Waite,Log is Reading now.",Toast.LENGTH_SHORT).show();
                    return;
                }
                isReadinglog = true;
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String str = FileUtil.readFromFile(FileType.LOADCLASS);
                        Message msg = new Message();
                        msg.obj = str;
                        logHandler.sendMessage(msg);
                    }
                }).start();
            }
        });

        b_onclick.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isReadinglog)
                {
                    Toast.makeText(MainActivity.this,"Please Waite,Log is Reading now.",Toast.LENGTH_SHORT).show();
                    return;
                }
                isReadinglog = true;
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String str = FileUtil.readFromFile(FileType.ONCLICK);
                        Message msg = new Message();
                        msg.obj = str;
                        logHandler.sendMessage(msg);
                    }
                }).start();
            }
        });


        b_clear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isReadinglog)
                {
                    Toast.makeText(MainActivity.this,"Please Waite,Log is Reading now.",Toast.LENGTH_SHORT).show();
                    return;
                }
                isReadinglog = true;
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String str = FileUtil.readFromFile(FileType.CLEAR);
                        Message msg = new Message();
                        msg.obj = str;
                        logHandler.sendMessage(msg);
                    }
                }).start();
            }
        });



    }

    //显示Log
    class myHandler extends Handler{
        @Override
        public void handleMessage(Message msg)
        {
            t_showlog.setText((String)msg.obj);
            isReadinglog = false;
        }
    }


}
