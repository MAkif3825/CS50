// Implements a dictionary's functionality(something in order not to let codespaces be deleted)

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 27 * 27 * 27;
int word_number;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // IT CAN BE NEEDED TO CHANGE IT TO POINTER
    //node *check = malloc(sizeof(node));
    // TODO
    //check = table[hash(word)];
    node *check = table[hash(word)];
    //if (hash(word) == 5211)
    //{
    //    printf("done");
    //}
    if (check == NULL)
    {
        return false;
    }
    while (check->next != NULL)
    {
        if (strcasecmp(word, check->word) == 0)
        {

            return true;
        }
        // printf("%s \n", check->word);
        check = check->next;
    }
    if (strcasecmp(word, check->word) == 0)
    {

        return true;
    }


    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

    // TODO: Improve this hash function
    // Make letters bigger and check punctuations
    int letters[3];
    int hash_code = 0;
    for (int i = 0; i < 3; i++)
    {
        if (isalpha(word[i]))
        {
            letters[i] = (tolower(word[i]) - 'a') * pow(27, 2 - i);
            hash_code += letters[i];
        }
        else if (word[i] == '\0')
        {
            i = 3;
        }
        else
        {
            letters[i] = 26 * pow(27, 2 - i);
            hash_code += letters[i];
        }


    }
    //printf("%i", hash_code);
    return hash_code;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //Open file
    FILE *f = fopen(dictionary, "r");
    if (f == NULL)
    {
        printf("cannot connected to the dictionary.");
        return false;
    }

    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Reading
    //node *last = NULL;
    node *temp = NULL;
    char *w = malloc((sizeof(char) * LENGTH) + 1);
    while (fscanf(f, "%s", w) != EOF)
    {

        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Error.");
            free(w);
            return false;
        }
        unsigned int hash_number = hash(w);

        //if (hash(w) == 5211)
        //{
        //    printf("done.");
        //}
        strcpy(new_node->word, w);
        new_node->next = NULL;

        if (table[hash_number] == NULL)
        {
            table[hash_number] = new_node;
            word_number++;

        }
        else
        {
            temp = table[hash_number];
            table[hash_number] = new_node;
            new_node->next = temp;

            word_number++;
        }

    }

    //node *cursor = table[5211];
    //while(cursor->next != NULL)
    // {
    // printf("%s \n", cursor->word);
    //cursor = cursor->next;
    //printf("%s \n", cursor->word);
    //}
    //return false;
    //free(tmp);
    free(w);
    fclose(f);
    //free(temp);
    return true;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_number;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *cursor = NULL;
    node *tmp = NULL;

    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = cursor;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }

    }

    return true;
}
