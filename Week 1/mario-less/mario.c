#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Welcome to The Mario Bros Game! Now please write a number between 1 and 8 for height: ");
    }
    while (n < 1 || n > 8);

    int m = n;

    for (int i = 0 ; i < n ; i++)
    {
        m--;
        for (int j = 0 ; j < (m); j++)
        {
            printf(" ");
        }

        for (int p = 0 ; p < (n - m); p++)
        {
            printf("#");
        }

        printf("\n");
    }
}