#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int countletters(string);
int countwords(string);
int countsentences(string);

int main(void)
{
    //Take text from user
    string txt = get_string("Text: ");
    //They must be float because we divide sth to sth
    //count letters
    float letter = countletters(txt);
    //Count words
    float word = countwords(txt);
    //Count sentences
    float sentence = countsentences(txt);
    //They are some formulas
    float aletter = letter * 100 / word;
    float asentence = sentence * 100 / word;

    float index = (0.0588 * aletter) - (0.296 * asentence) - 15.8;
    //  int round(long index);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int)round(index));
        // printf("Grade %i\n" ,index);
    }

    /*
    printf("Letter: %i \n" , letter);
    printf("Word: %i \n" , word);
    printf("Sentence: %i \n" , sentence);
    */
}

int countletters(string txt)
{
    int j = 0;
    int letter = 0;
    while (j < strlen(txt))
    {
        //control for letters
        if (isalpha(txt[j]) != 0)
        {
            letter++;
            j++;
        }
        else
        {
            j++;
        }
    }
    return letter;
}


int countwords(string txt)
{
    int i = 0;
    int word = 0;
    //check if starts with space
    if (txt[0] == 32)
    {
        i++;
    }
    while (i < strlen(txt))
    {
        //control due to double space
        if (txt[i] == 32)
        {
            if (txt[i + 1] == 32)
            {
                i++;
            }
            else
            {
                word++;
                i++;
            }
        }
        else
        {
            i++;
        }
    }
    if (txt[i] != 32)
    {
        word++;
    }

    return word;
}

int countsentences(string txt)
{
    int i = 0;
    int sentence = 0;
    while (i < strlen(txt))
    {
        //recognize the punctuations
        if (txt[i] == 46 || txt[i] == 63 || txt[i] == 33)
        {
            sentence++;
            i++;
        }
        else
        {
            i++;
        }
    }
    return sentence;
}