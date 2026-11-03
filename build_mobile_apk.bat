@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title AGRO AI - Android Mobile APK Builder

echo ================================================================
echo  🌱 AGRO AI - Standalone Mobile APK Generator
echo ================================================================
echo.

rem Set Java and Android SDK paths
set "JAVA_HOME=C:\Program Files\Java\jdk-23"
set "ANDROID_HOME=C:\Users\praha\AppData\Local\Android\Sdk"
set "ANDROID_SDK_ROOT=%ANDROID_HOME%"

echo [1/3] Building Mobile Web Assets...
cd mobile-app
call npm.cmd run build
if errorlevel 1 (
    echo [ERROR] Mobile build failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Syncing with Android Container...
call npx.cmd cap sync android
if errorlevel 1 (
    echo [ERROR] Capacitor sync failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Compiling Native Android APK with Gradle...
cd android
call gradlew.bat assembleDebug
if errorlevel 1 (
    echo [ERROR] Gradle APK build failed.
    pause
    exit /b 1
)

echo.
echo Finalizing APK output...
cd /d "%~dp0"
if not exist "output\apk" mkdir "output\apk"
copy /y "mobile-app\android\app\build\outputs\apk\debug\app-debug.apk" "output\apk\AGRO_AI_Mobile.apk" >nul

echo.
echo ================================================================
echo  ✅ SUCCESS! Android APK generated successfully!
echo  📦 File: %~dp0output\apk\AGRO_AI_Mobile.apk
echo ================================================================
echo.
pause

