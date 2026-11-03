@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title AGRO AI - Android APK Builder

echo ================================================================
echo  🌱 AGRO AI - Android Mobile APK Generator
echo ================================================================
echo.

rem Set Android SDK
set "ANDROID_HOME=C:\Users\praha\AppData\Local\Android\Sdk"
set "ANDROID_SDK_ROOT=%ANDROID_HOME%"

rem Find Java Runtime
if exist "C:\Program Files\Android\Android Studio5\jbr" (
    set "JAVA_HOME=C:\Program Files\Android\Android Studio5\jbr"
) else if exist "C:\Program Files\Android\Android Studio\jbr" (
    set "JAVA_HOME=C:\Program Files\Android\Android Studio\jbr"
) else if exist "C:\Program Files\Java\jdk-23" (
    set "JAVA_HOME=C:\Program Files\Java\jdk-23"
)

echo [1/4] Building React Frontend with Vite...
cd frontend
call npm.cmd run build
if errorlevel 1 (
    echo [ERROR] Frontend build failed.
    pause
    exit /b 1
)

echo.
echo [2/4] Syncing Web Assets with Android Platform...
call npx.cmd cap sync android
if errorlevel 1 (
    echo [ERROR] Capacitor sync failed.
    pause
    exit /b 1
)

echo.
echo [3/4] Compiling Android APK with Gradle...
cd android
call gradlew.bat assembleDebug
if errorlevel 1 (
    echo [ERROR] Gradle APK build failed.
    pause
    exit /b 1
)

echo.
echo [4/4] Finalizing APK Output...
cd /d "%~dp0"
if not exist "output\apk" mkdir "output\apk"
copy /y "frontend\android\app\build\outputs\apk\debug\app-debug.apk" "output\apk\AGRO_AI_Mobile.apk" >nul

echo.
echo ================================================================
echo  ✅ SUCCESS! Android APK generated successfully!
echo  📦 Location: %~dp0output\apk\AGRO_AI_Mobile.apk
echo ================================================================
echo.
pause

