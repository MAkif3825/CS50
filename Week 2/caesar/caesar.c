#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool is_everything_ok(int, string);

int main(int argc, string argv[])
{
    //Start of everything
    if (is_everything_ok(argc, argv[1]) == 1)
    {
        int key = atoi(argv[1]);
        //Take string from user
        string plaintxt = get_string("Plain text: ");
        //for (int i = 0; i == strlen(plaintxt); i++)
        int i = 0;
        //start proccess
        while (i < strlen(plaintxt))
        {
            //check letter
            if (isalpha(plaintxt[i]) != 0)
            {
                //chech upper or lower case
                if (islower(plaintxt[i]) == 0)
                {
                    //Upper
                    plaintxt[i] -= 65;
                    plaintxt[i] = (plaintxt[i] + key) % 26;
                    plaintxt[i] += 65;
                    i++;
                }
                else
                {
                    //Lower
                    plaintxt[i] -= 97;
                    plaintxt[i] = (plaintxt[i] + key) % 26;
                    plaintxt[i] += 97;
                    i++;
                }
            }
            else
            {
                i++;
            }
        }
        printf("ciphertext: %s\n", plaintxt);

    }
    else
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
}

//checking everything
bool is_everything_ok(int a, string key)
{
    if (a == 2)
    {
        int i = 0;
        while (i < strlen(key))
        {
            //check digit or not
            if (isdigit(key[i]) != 0)
            {
                i++;
            }
            else
            {
                i = strlen(key);
                return 0;
            }
        }
        return 1;
    }
    else
    {
        return 0;
    }
}