#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <windows.h>


const char PROJECT_NAME[] = "Universal update Tool (C Edition)";
const char VERSION[] = "1.1";

const char FILE_T7Z[] = ".\\local\\7zip\\7z.exe";
const char FILE_PAK[] = ".\\resources\\cache\\update.pack";
const char FILE_EXE[] = "d3dxSkinManage.exe";



bool file_exists(const char *filename)
{
    return access(filename, F_OK) == 0;
}


void pause()
{
    sleep(100);
    // system("pause >nul");
}


int taskkill_imagename(const char *imagename) {
    char command[256];
    snprintf(command, sizeof(command), "taskkill /f /t /im %s 1>nul 2>nul", imagename);
    int answer = system(command);
    return answer;
}


int x7z_file(const char *packpath) {
    char command[512];
    snprintf(command, sizeof(command), "%s x -y -o. %s 1>nul 2>nul", FILE_T7Z, packpath);
    int answer = system(command);
    return answer;
}


void exception_exit(int code){
    pause();
    exit(code);
}


void step_check(void) {
    // 检查程序是否存在
    if (file_exists(FILE_EXE) != true) {
        printf("[ERROR] %s not exise.\n", FILE_EXE);
        exception_exit(1);
    }

    // 检查 7zip 是否存在
    if (file_exists(FILE_T7Z) != true) {
        printf("[ERROR] 7zip not found.\n");
        exception_exit(2);
    }
}


void step_stop(void) {
    int ans = taskkill_imagename(FILE_EXE);
    // printf("code: %d\n", ans);

    if (ans == 0) {
        return;

    } else {
    if (ans == 128) {
        printf("[WARN] %s not running.\n", FILE_EXE);

    } else {
    if (ans == 255) {
        printf("[ERROR] No administrator rights.\n");
        exception_exit(3);

    } else {
        printf("[WARN] Unknown return value.\n");

    }}}
}


void step_x7z(void) {
    if (file_exists(FILE_PAK) == true) {
        x7z_file(FILE_PAK);
        DeleteFile(FILE_PAK);
    }
}


void step_lanch(void) {
    char command[256];
    snprintf(command, sizeof(command), "start \"\" /B %s", FILE_EXE);
    system(command);
}


int main()
{
    printf("[INFO] %s\n", PROJECT_NAME);
    printf("[INFO] version %s\n", VERSION);
    printf("[INFO] check...\n");
    step_check();

    printf("[INFO] kill program process...\n");
    step_stop();

    printf("[INFO] release update pack...\n");
    step_x7z();

    printf("[INFO] starting program...\n");
    step_lanch();
    return 0;
}
