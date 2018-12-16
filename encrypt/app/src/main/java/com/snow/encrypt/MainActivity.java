package com.snow.encrypt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.FileDescriptor;

import com.snow.service.ServerManager;
import com.vivo.security.jni.SecurityCryptor;


public class MainActivity extends AppCompatActivity {

    private ServerManager mServerManager;

    private TextView textView_str = null;
    private EditText editText_str = null;
    private TextView textView_ret = null;
    private Button button_encry = null;
    private Button button_decry = null;

    private Button button_start = null;
    private Button button_stop = null;

    public String str_ret = "";
    public String str_inp = "";

    public String mRootUrl = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editText_str = (EditText) findViewById(R.id.text_string);
        textView_ret = (TextView) findViewById(R.id.text_result);
        button_decry = (Button)findViewById(R.id.button_decry);
        button_encry = (Button)findViewById(R.id.button_encry);

        button_start = (Button)findViewById(R.id.button_start);
        button_stop = (Button)findViewById(R.id.button_stop);

        button_encry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                str_inp = editText_str.getText().toString();
                if(str_inp.length() <= 0)
                {
                    Toast.makeText(MainActivity.this,"Please input valid string",Toast.LENGTH_SHORT).show();
                    return;
                }
                str_ret = encrypt_vivosgmain(str_inp);
                textView_ret.setText(str_ret);

            }
        });

        button_decry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                str_inp = editText_str.getText().toString();
                if(str_inp.length() <= 0)
                {
                    Toast.makeText(MainActivity.this,"There is null to decrypt.",Toast.LENGTH_SHORT).show();
                    return;
                }
                str_ret = decrypt_vivosgmain(str_inp);
                textView_ret.setText(str_ret);
            }
        });

        //start事件监听
        button_start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startServer();
            }
        });
        //stop事件监听
        button_stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopServer();
            }
        });

        //run in a service
        mServerManager = new ServerManager(this);
        mServerManager.register();
    }


    //启动AndServer
    public void startServer()
    {
        textView_ret.setText("start click...");
        mServerManager.startServer();
    }

    //关闭AndServer
    public void stopServer()
    {
        mServerManager.stopServer();
    }

    //加密
    public String encrypt_vivosgmain(String str)
    {
        try{
            String paramString = new String(SecurityCryptor.nativeBase64Encrypt(str.getBytes("utf-8")));
            return paramString;
        }catch (Exception e)
        {
            e.printStackTrace();
            return "encryption exception";
        }

    }
    //解密
    public String decrypt_vivosgmain(String str)
    {
        try{
            String paramString = new String (SecurityCryptor.nativeBase64Decrypt(str.getBytes("utf-8")));
            return paramString;
        }catch (Exception e)
        {
            e.printStackTrace();
            return "decryption exception";
        }
    }

    //Register broadcast
    public void onServerStart(String ip)
    {
        button_start.setVisibility(View.GONE);
        button_stop.setVisibility(View.VISIBLE);

        if(!TextUtils.isEmpty(ip))
        {
            mRootUrl = "http://"+ip+":8080/";
            textView_ret.setText(mRootUrl);
        } else {
            mRootUrl = null;
            textView_ret.setText("error occurs, ip is null.");
        }
    }

    public void onServerError(String message)
    {
        mRootUrl = null;
        button_start.setVisibility(View.VISIBLE);
        button_stop.setVisibility(View.VISIBLE);
        textView_ret.setText(message);
    }

    public void onServerStop()
    {
        mRootUrl = null;
        button_stop.setVisibility(View.GONE);
        button_start.setVisibility(View.VISIBLE);
        textView_ret.setText("Server stoped.");
    }
}
