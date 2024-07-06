#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sum = image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen;
            sum = sum / 3;
            int avrg = round(sum);
            image[i][j].rgbtBlue = avrg;
            image[i][j].rgbtRed = avrg;
            image[i][j].rgbtGreen = avrg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float originalRed = image[i][j].rgbtRed;
            float originalBlue = image[i][j].rgbtBlue;
            float originalGreen = image[i][j].rgbtGreen;

            double r = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            double g = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            double b = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            if (r > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = r;
            }

            if (g > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = g;
            }

            if (b > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = b;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; 2 * j < width; j++)
        {
            int tempr = image[i][j].rgbtRed;
            int tempg = image[i][j].rgbtGreen;
            int tempb = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtRed = tempr;

            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][width - 1 -j].rgbtGreen = tempg;

            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtBlue = tempb;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE color[height][width];

    color[0][0].rgbtRed = round((image[0][0].rgbtRed + image[0][1].rgbtRed + image[1][0].rgbtRed + image[1][1].rgbtRed) / 4.0);
    color[0][0].rgbtGreen = round((image[0][0].rgbtGreen + image[0][1].rgbtGreen + image[1][0].rgbtGreen + image[1][1].rgbtGreen) / 4.0);
    color[0][0].rgbtBlue = round((image[0][0].rgbtBlue + image[0][1].rgbtBlue + image[1][0].rgbtBlue + image[1][1].rgbtBlue) / 4.0);

    color[height - 1][0].rgbtRed = round((image[height - 1][0].rgbtRed + image[height - 1][1].rgbtRed + image[height - 2][0].rgbtRed + image[height - 2][1].rgbtRed) / 4.0);
    color[height - 1][0].rgbtGreen = round((image[height - 1][0].rgbtGreen + image[height - 1][1].rgbtGreen + image[height - 2][0].rgbtGreen + image[height - 2][1].rgbtGreen) / 4.0);
    color[height - 1][0].rgbtBlue = round((image[height - 1][0].rgbtBlue + image[height - 1][1].rgbtBlue + image[height - 2][0].rgbtBlue + image[height - 2][1].rgbtBlue) / 4.0);

    color[0][width - 1].rgbtRed = round((image[0][width - 1].rgbtRed + image[0][width - 2].rgbtRed + image[1][width - 1].rgbtRed + image[1][width - 2].rgbtRed) / 4.0);
    color[0][width - 1].rgbtGreen = round((image[0][width - 1].rgbtGreen + image[0][width - 2].rgbtGreen + image[1][width - 1].rgbtGreen + image[1][width - 2].rgbtGreen) / 4.0);
    color[0][width - 1].rgbtBlue = round((image[0][width - 1].rgbtBlue + image[0][width- 2].rgbtBlue + image[1][width - 1].rgbtBlue + image[1][width - 2].rgbtBlue) / 4.0);

    color[height - 1][width - 1].rgbtRed = round((image[height - 1][width - 1].rgbtRed + image[height - 1][width - 2].rgbtRed + image[height - 2][width - 1].rgbtRed + image[height - 2][width - 2].rgbtRed) / 4.0);
    color[height - 1][width - 1].rgbtGreen = round((image[height - 1][width - 1].rgbtGreen + image[height - 1][width - 2].rgbtGreen + image[height - 2][width - 1].rgbtGreen + image[height - 2][width - 2].rgbtGreen) / 4.0);
    color[height - 1][width - 1].rgbtBlue = round((image[height - 1][width - 1].rgbtBlue + image[height - 1][width- 2].rgbtBlue + image[height - 2][width - 1].rgbtBlue + image[height - 2][width - 2].rgbtBlue) / 4.0);

    //For the first row
    for (int j = 1; j < width - 1; j++)
    {
        color[0][j].rgbtRed = round((image[0][j - 1].rgbtRed + image[0][j].rgbtRed + image[0][j + 1].rgbtRed + image[1][j - 1].rgbtRed + image[1][j].rgbtRed + image[1][j + 1].rgbtRed) / 6.0);
        color[0][j].rgbtGreen = round((image[0][j - 1].rgbtGreen + image[0][j].rgbtGreen + image[0][j + 1].rgbtGreen + image[1][j - 1].rgbtGreen + image[1][j].rgbtGreen + image[1][j + 1].rgbtGreen) / 6.0);
        color[0][j].rgbtBlue = round((image[0][j - 1].rgbtBlue + image[0][j].rgbtBlue + image[0][j + 1].rgbtBlue + image[1][j - 1].rgbtBlue + image[1][j].rgbtBlue + image[1][j + 1].rgbtBlue) / 6.0);
    }

    //For the last row
    for (int j = 1; j < width - 1; j++)
    {
        color[height - 1][j].rgbtRed = round((image[height - 1][j - 1].rgbtRed + image[height - 1][j].rgbtRed + image[height - 1][j + 1].rgbtRed + image[height - 2][j - 1].rgbtRed + image[height - 2][j].rgbtRed + image[height - 2][j + 1].rgbtRed) / 6.0);
        color[height - 1][j].rgbtGreen = round((image[height - 1][j - 1].rgbtGreen + image[height - 1][j].rgbtGreen + image[height - 1][j + 1].rgbtGreen + image[height - 2][j - 1].rgbtGreen + image[height - 2][j].rgbtGreen + image[height - 2][j + 1].rgbtGreen) / 6.0);
        color[height - 1][j].rgbtBlue = round((image[height - 1][j - 1].rgbtBlue + image[height - 1][j].rgbtBlue + image[height - 1][j + 1].rgbtBlue + image[height - 2][j - 1].rgbtBlue + image[height - 2][j].rgbtBlue + image[height - 2][j + 1].rgbtBlue) / 6.0);
    }
    //Except the first and last rows
    for (int i = 1; i < height - 1; i++)
    {
        //For the first column
        color[i][0].rgbtRed = round((image[i - 1][0].rgbtRed + image[i + 1][0].rgbtRed + image[i][0].rgbtRed + image[i - 1][1].rgbtRed + image[i][1].rgbtRed + image[i + 1][1].rgbtRed) / 6.0);
        color[i][0].rgbtGreen = round((image[i - 1][0].rgbtGreen + image[i + 1][0].rgbtGreen + image[i][0].rgbtGreen + image[i - 1][1].rgbtGreen + image[i][1].rgbtGreen + image[i + 1][1].rgbtGreen) / 6.0);
        color[i][0].rgbtBlue = round((image[i - 1][0].rgbtBlue + image[i + 1][0].rgbtBlue + image[i][0].rgbtBlue + image[i - 1][1].rgbtBlue + image[i][1].rgbtBlue + image[i + 1][1].rgbtBlue) / 6.0);

        //For the last column
        color[i][width - 1].rgbtRed = round((image[i - 1][width - 1].rgbtRed + image[i + 1][width - 1].rgbtRed + image[i][width - 1].rgbtRed + image[i - 1][width - 2].rgbtRed + image[i][width - 2].rgbtRed + image[i + 1][width - 2].rgbtRed) / 6.0);
        color[i][width - 1].rgbtGreen = round((image[i - 1][width - 1].rgbtGreen + image[i + 1][width - 1].rgbtGreen + image[i][width - 1].rgbtGreen + image[i - 1][width - 2].rgbtGreen + image[i][width - 2].rgbtGreen + image[i + 1][width - 2].rgbtGreen) / 6.0);
        color[i][width - 1].rgbtBlue = round((image[i - 1][width - 1].rgbtBlue + image[i + 1][width - 1].rgbtBlue + image[i][width - 1].rgbtBlue + image[i - 1][width - 2].rgbtBlue + image[i][width - 2].rgbtBlue + image[i + 1][width - 2].rgbtBlue) / 6.0);

        //For the remained ones
        for(int j = 1; j < width - 1; j++)
        {
            color[i][j].rgbtRed = round((image[i - 1][j].rgbtRed + image[i + 1][j].rgbtRed + image[i][j].rgbtRed + image[i - 1][j - 1].rgbtRed + image[i][j - 1].rgbtRed + image[i + 1][j - 1].rgbtRed + image[i + 1][j + 1].rgbtRed + image[i - 1][j + 1].rgbtRed + image[i][j + 1].rgbtRed) / 9.0);
            color[i][j].rgbtGreen = round((image[i - 1][j].rgbtGreen + image[i + 1][j].rgbtGreen + image[i][j].rgbtGreen + image[i - 1][j - 1].rgbtGreen + image[i][j - 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen  + image[i - 1][j + 1].rgbtGreen + image[i][j + 1].rgbtGreen + image[i + 1][j + 1].rgbtGreen) / 9.0);
            color[i][j].rgbtBlue = round((image[i - 1][j].rgbtBlue + image[i + 1][j].rgbtBlue + image[i][j].rgbtBlue + image[i - 1][j - 1].rgbtBlue + image[i][j - 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue + image[i - 1][j + 1].rgbtBlue + image[i + 1][j + 1].rgbtBlue + image[i][j + 1].rgbtBlue) / 9.0);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = color[i][j].rgbtRed;
            image[i][j].rgbtGreen = color[i][j].rgbtGreen;
            image[i][j].rgbtBlue = color[i][j].rgbtBlue;

        }
    }
    return;
}
