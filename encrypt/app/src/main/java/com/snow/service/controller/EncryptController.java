package com.snow.service.controller;
import com.alibaba.fastjson.JSON;
import com.vivo.security.jni.SecurityCryptor;
import com.yanzhenjie.andserver.annotation.Addition;
import com.yanzhenjie.andserver.annotation.CookieValue;
import com.yanzhenjie.andserver.annotation.FormPart;
import com.yanzhenjie.andserver.annotation.GetMapping;
import com.yanzhenjie.andserver.annotation.PathVariable;
import com.yanzhenjie.andserver.annotation.PostMapping;
import com.yanzhenjie.andserver.annotation.RequestBody;
import com.yanzhenjie.andserver.annotation.RequestMapping;
import com.yanzhenjie.andserver.annotation.RequestParam;
import com.yanzhenjie.andserver.annotation.RestController;
import com.yanzhenjie.andserver.http.HttpRequest;
import com.yanzhenjie.andserver.http.HttpResponse;
import com.yanzhenjie.andserver.http.cookie.Cookie;
import com.yanzhenjie.andserver.http.multipart.MultipartFile;
import com.yanzhenjie.andserver.http.session.Session;
import com.snow.service.component.LoginInterceptor;
import com.snow.service.model.UserInfo;
import com.snow.service.util.FileUtils;
import com.snow.service.util.Logger;
import com.yanzhenjie.andserver.util.MediaType;

import java.io.File;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping(path = "/encrypt")
class EncryptController {

    @GetMapping(path = "/vbase64encry",produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    String vbase64encry(HttpRequest request,HttpResponse response,@RequestParam(name = "str")String str)
    {
        if(str == null || str.length()==0)
        {
            return "Please input str value";
        }
        String result = "";
        try {
            result = new String(SecurityCryptor.nativeBase64Encrypt(str.getBytes("utf-8")));
        }catch (Exception e)
        {
            result = e.toString();
        }


        return result;
    }
    @GetMapping(path = "/vbase64decry",produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    String vbase64decry(HttpRequest request,HttpResponse response,@RequestParam(name = "str")String str)
    {
        if(str == null || str.length()==0)
        {
            return "Please input str value";
        }
        String result = "";
        try {
            result = new String(SecurityCryptor.nativeBase64Decrypt(str.getBytes("utf-8")));
        }catch (Exception e)
        {
            result = e.toString();
        }
        return result;
    }
}
