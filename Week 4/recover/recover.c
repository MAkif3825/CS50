#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
//Open the file
    string file = argv[1];
    FILE *f = fopen(file, "r");
    if (f == NULL)
    {
        //Quit if NULL returns
        printf("File cannot open.");
        return 1;
    }

//Define new type
    typedef uint8_t BYTE;


//Allocate memory for buffer
    BYTE *buffer = malloc(512);
    if (buffer == NULL)
    {
        //Quit if NULL returns
        printf("Error.");
        return 2;
    }

    char isim[13];

    int i = 0;
    FILE *e = NULL;

    while (fread(buffer, 1, 512, f) == 512)
    {
        //Check if it is a beggining of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //Check if it is a first file
            if (i == 0)
            {
                //Open the first file
                sprintf(isim, "%03i.jpg", i);
                FILE *img1 = fopen(isim, "w");
                printf("%s \n", isim);
                //Write the data on it
                fwrite(buffer, 512, 1, img1);
                e = img1;
                i++;
            }
            else
            {
                fclose(e);

                //Open another
                sprintf(isim, "%03i.jpg", i);
                FILE *img2 = fopen(isim, "w");
                printf("%s \n", isim);
                //Write data on it
                fwrite(buffer, 512, 1, img2);
                e = img2;
                i++;
            }

        }
        else if (i != 0)
        {
            fwrite(buffer, 512, 1, e);
        }

    }

    free(buffer);
    if (e != NULL)
    {
        fclose(e);
    }

    fclose(f);

}

