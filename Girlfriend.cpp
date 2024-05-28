#include <cstdlib>

int main(){
    system("powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File src\\run.ps1");
    return 0;
}