package com.snow.encrypt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.FileDescriptor;
import com.vivo.security.jni.SecurityCryptor;


public class MainActivity extends AppCompatActivity {

    private TextView textView_str = null;
    private EditText editText_str = null;
    private TextView textView_ret = null;
    private Button button_encry = null;
    private Button button_decry = null;

    public String str_ret = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editText_str = (EditText) findViewById(R.id.text_string);
        textView_ret = (TextView) findViewById(R.id.text_result);
        button_decry = (Button)findViewById(R.id.button_decry);
        button_encry = (Button)findViewById(R.id.button_encry);



        button_encry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                str_ret = encrypt_vivosgmain("hello world!");
                textView_ret.setText(str_ret);
            }
        });

        button_decry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SecurityCryptor securityCryptor = new SecurityCryptor();
                if(securityCryptor.isSuccess())
                    textView_ret.setText("load success.");
                else
                    textView_ret.setText("load failed.");
            }
        });
    }

    //加密
    public String encrypt_vivosgmain(String str)
    {
        try{
            String paramString = new String(SecurityCryptor.nativeBase64Encrypt(str.getBytes("utf-8")));
            return paramString;
        }catch (Exception e)
        {
            return e.getMessage();
        }

    }
}
