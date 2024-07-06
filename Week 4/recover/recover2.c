#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int write(int* a, int i);

int main(int argc, char *argv[])
{
 FILE *f = fopen(argv[1] , "r");
 if(f == NULL)
 {
    printf("File cannot open.");
    return 1;
 }

fseek(f, 0, SEEK_END);
long file_size = ftell(f);
fseek(f, 0, SEEK_SET);

long how_many_512 = file_size / 512;
typedef uint8_t BYTE;

BYTE (*buffer)[how_many_512][512] = malloc(how_many_512 * 512);

fread(buffer, 512, how_many_512, f);

int i = 0;
int k = 1;

 while (i < how_many_512)
{

    if (*buffer[i][0] == 0xff && *buffer[i][1] == 0xd8 && *buffer[i][2] == 0xff && (*buffer[i][3] & 0xf0) == 0xe0 )
    {

        char* a =  malloc(sizeof(char) * 8);
        sprintf(a, "%03i.jpg", 3);
        FILE *img = fopen(a, "w");
        write(img, i);
    }

}

int write(int* , int i)
{
    do
    {
        //fwrite();
    }while(*buffer[i][0] == 0xff && *buffer[i][1] == 0xd8 && *buffer[i][2] == 0xff && (*buffer[i][3] & 0xf0) == 0xe0);

}
}