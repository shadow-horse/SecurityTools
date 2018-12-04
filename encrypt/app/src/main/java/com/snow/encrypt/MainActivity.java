package com.snow.encrypt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.FileDescriptor;
import com.vivo.security.jni.SecurityCryptor;


public class MainActivity extends AppCompatActivity {

    private TextView textView_str = null;
    private EditText editText_str = null;
    private TextView textView_ret = null;
    private Button button_encry = null;
    private Button button_decry = null;

    public String str_ret = "";
    public String str_inp = "";

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
}
