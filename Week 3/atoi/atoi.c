#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int

    printf("%i\n", convert(input));
}

int convert(string input)
{
    // TODO
    int i = strlen(input) - 1;
    if (i == 0)
    {
        input[i] -= 48;
        return input[i];
    }
    int number = input[i] -= 48;
    input[i] = input[i + 1];
    number += 10 * convert(input);
    return number + input[i];
}