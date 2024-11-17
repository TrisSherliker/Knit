# Knit
 
Instead of reading charts throughout your whole project, type them out once into and convert them into written knitting patterns: Knitting charts -> written patterns for Aran jumpers. Convert transcribed knitting charts into written pattern instructions in various formats. 
 
Useful, Not smart. It's very much hacked together code, with a regrettable mess at the end - but there comes a point when you want to put down the screen and pick up the needles.

![NOsmall](https://github.com/user-attachments/assets/50edd357-8049-4d57-970b-d6a33037aebb)

# Why?

I **really hate** knitting from charts, but I want to knit an  Aran jumper. Those patterns are *made* from charts though, in repeating panels against each other. They typically have different row-lengths so that they repeat at different intervals along the jumper -- meaning you have to spend a lot of time keeping track of which row you're knitting from on each of charts A B, C D, E, F etc. 

Headache.

On the other hand, I enjoy (a) learning to code and (b) using the correct format for the job. 

# How and What?

Input: 
 You have to transcribe the pattern yourself, but only once! See `example_pattern.py` for how to do that, and save your transcription as a .py file. This will be your pattern module.

Run `python3 pattern-printer.py example_pattern.py' (replace example_pattern.py with the filename of your pattern module.)

The program will calculate how many rows you need to account for all repeats, or allow you to select a smaller number.

Outputs as: 

- Row by row instructions in the following formats:
   - Plain text (markdown)
   - PDF A4 
   - eBook (for e-readers, one chapter per row)
   - html
     
- A table of instructions (one row per row) in the following formats:
   - Plain text (markdown)
   - PDF A3
   - html

## Stitch dictionary

The program also allows you, optionally, to enter a dictionary (or key) to the abbreviations used, allowing you to selet your own abbreviations. It's generally better to avoid special characters like `\` and `|`, as this is not well handled by the script in all conversions.


 # Example outputs

Ebook, for Boox, kindles and similar e-readers:

![ebook-output-page](https://github.com/user-attachments/assets/542e49fd-1d3f-4637-af1b-acc872b25e29)

PDF tables, by the magic of LaTeX with Pandoc:

![pattern-pdf-table](https://github.com/user-attachments/assets/11959131-f8a8-4baa-9501-5ade9c20ed82)

HTML:

![html_table](https://github.com/user-attachments/assets/521f4556-8f78-4485-ab4b-c80ba55ce86d)

Plain text:

![pattern-plain](https://github.com/user-attachments/assets/f6de78d4-58bb-4e6a-bade-b35fe2fb23df)

Stitch dictionary:
![stitch_dict](https://github.com/user-attachments/assets/53071454-2fac-4452-b32c-bcf387a61c16)
