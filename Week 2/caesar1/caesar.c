#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool is_everything_ok(int,string);

int main(int argc, string argv[])
{
  if(is_everything_ok(argc , argv[1]) == 1 )
  {
    int key = atoi(argv[1]);
    string plaintxt = get_string("Plain text: ");
    //for (int i = 0; i == strlen(plaintxt); i++)
    int i = 0;
    while(i<strlen(plaintxt))
    {
        if(isalpha(plaintxt[i]) !=0 )
        {
            if(islower(plaintxt[i]) == 0)
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
    printf("ciphertext: %s \n" , plaintxt);

  }
  else
  {
    printf("Usage: ./caesar key \n");
  }
}

bool is_everything_ok(int a , string key)
{
    if(a == 2)
    {
        int i = 0;
        while(i < strlen(key))
        {
            if(isdigit(key[i]) != 0)
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














/* if(argc == 2)
    {
        int i = 0;
        while(i == strlen(argv[1]))
        {
            if(isdigit(argv[1][i]))
            {
                int key = atoi(argv[1][i]);
                string plaintxt = get_string("Plaintext: ");
                for(int j=0; j==strlen(planintxt); j++;)
                {
                    toupper(plaintxt[j]);
                    plaintxt[j] -= 65
                    plaintxt[j] = plaintxt[j] + ()
                }

                i++;
            }
            else
            {
                i=strlen(argv[1]);
                printf("Usage: ./caesar key");
            }
        }
    }*/