# Educational Archive for "Wristsaver v5.5"

*Note: This project is archived and no longer maintained. No additional documentation or installation support will be provided.*

*User font creation is a complex and time-consuming process, mainly for demonstration purposes.*

*This readme document was optimised with AI*.

<p style="text-align:right;"><a href="https://gggrv.github.io/something/2022/05/17/devinfo-wristsaver/">Homepage</a></p>

## Overview

| Item | Description |
| --- | --- |
| What is this? | A project saved in a `git` repository, hosted on GitHub. |
| What does it contain? | <ul><li>Python tools for printing handwritten documents.</li><li>Demo pseudofont for demonstration only.</li></ul> |
| Who is it for? | Beginner Python developers. |
| Project status | <ul><li>✔️ Functional and archived</li><li>😴 Not maintained</li></ul> |
| Why is it obsolete? | <ul><li>Code is obscure and rigid; meaningful changes require a full rewrite.</li><li>Font creation is manual and labor-intensive, not practical with modern ML tools.</li></ul> |
| Purpose | Educational archive with working code. |
| Name origin | It once helped save human wrists from repetitive strain. |

## Installation

This project is best used with [Visual Studio Code](https://code.visualstudio.com) (VS Code).

1. Clone this repository.
2. Open the folder in VS Code.
3. Set up Python environment:
   - Create virtual environment: `python -m venv .virtual_env`
   - Select the interpreter: VS Code Command Palette → "Python: Select Interpreter" → Enter path
4. Install dependencies:
   ```
   pip install setuptools
   pip install -r requirements.txt
   ```

## Printing a Handwritten Document

1. Open `step5_Printer.py`.
2. Scroll to the bottom.
3. Set the `my_font_folder` variable.
4. Run the script.

Output `.png` images (`1.png`, `2.png`, ...) will appear in the repository folder. You may post-process them with any image editor.

The example output with a fine-tuned font could be as follows (*please note that for privacy reasons the original output image, which was 2480x3500px and 300 dpi resolution, had to be cropped and severely scaled down*):

![Image with example output with fine-tuned font, severely scaled down for privacy reasons](./docs/severely_scaled_down_output_demo.png)

### Customizing Printed Text

1. Open `giant_lecture.html`.
2. Edit its contents (ensure tags are closed).
3. Use simple tag structure: headers, paragraphs, new lines only.

*Please note, that theoretically `wristsaver` can print in any language — any letter, number, text symbol, emoji, pictogram, word, phrase, anything. In order to achieve this in practice, the user needs to manually add each desired custom item into his font and provide appropriate metadata. The process will be described in further sections.*

### Customize output image size, resolution, etc

1. Open the `main.css` file.
2. Carefully edit its contents (make sure all tags are closed, etc).
3. Keep the values as simple as possible.

## Creating a User Font

A minimal demo font is included, sampled from the [Kaggle handwriting dataset](https://www.kaggle.com/datasets/landlord/handwriting-recognition?resource=download).

Please see the expected folder structure (some files are omitted):

```
■ cloned repository directory
├─■ fonts (root folder for all fonts)
│ ├─■ step0_raw_kaggle_test_images.zip
│ ├─■ step1_manually_split_kaggle_test_letters.zip
│ ├─■ step2kaggle_rem_bg_create_df.zip
│ ├─■ step3kaggle_write_image_width_and_height_to_df.zip
│ └─■ step4kaggle_Editor (folder with actual printable font)
├─■ step2_rem_bg_create_df.py
├─■ step3_write_image_width_and_height_to_df.py
├─■ step4_Editor.py
├─■ step5_Printer.py (already explained in the previous section)
└─■ step10_Marker.py
```

### Step 0 — Obtain Raw Image With Handwriting

1. Scan a handwritten page.
2. Create `fonts/my_font_0raw`.
3. Put a copy of the scanned image there.

### Step 1 — Split Image into Fragments

Fragments can be any shape or size. You can use any image editor to select and save regions.

1. Create `fonts/my_font_1split` and subfolders (e.g., `letters_lowercase`, `letters_uppercase`, `numbers`, etc.).
2. Place copies of the fragments in appropriate subfolders.

### Step 2 — Remove Backgrounds and Create Metadata

1. Duplicate `fonts/my_font_1split` as `fonts/my_font_2metadata`.
2. Open `step2_rem_bg_create_df.py` in Spyder.
3. Set `folder_with_letter_images` to `fonts/my_font_2metadata`.
4. Run the script.

Images will be updated with transparent backgrounds and `df.xls` metadata files will be created.

### Step 3 — Add Image Size Metadata

1. Duplicate `fonts/my_font_2metadata` as `fonts/my_font_3metadata`.
2. Open `step3_write_image_width_and_height_to_df.py` in Spyder.
3. Set `folder_with_letter_images` to `fonts/my_font_3metadata`.
4. Run the script.

The `df.xls` files will be edited inplace.

### Step 3.3 — Add Text Labels to Metadata

1. Duplicate the folder `fonts/my_font_3metadata`.
1. Rename it to be `fonts/my_font_printable`.
1. Open one `df.xls` in this folder with any supported editor.
2. Add new column named `text`.
3. Input the desired text (example: `t_uppercase.png` has text `T`, `a_version_slanted.png` has text `a`, `1.png` has text `1`, `smiley_face.png` has text `😊`, `word_the.png` has text `^`).

*Please note that only single-character symbols are supported. <sub>Probably. I don't remember.</sub>*

At this point, the font is usable, but results may need improvement.

### Step 4 — Adjust Metadata via GUI Editor

1. Open `step4_Editor.py` in Spyder.
2. Set `my_font_folder`.
3. Run the script.
4. Two GUI windows will appear:

![Two windows](./docs/stage4_1_window.jpg)

6. Click on any letter in the `GUI window with letters`.
7. The letter will become highlighted by red border, and the lines will appear:

![Screenshot of the clicked window](./docs/stage4_2_clicked_window.jpg)

8. Use `W`,`A`,`S`,`D` to adjust the letter's position relative to its neighbouring letters.
9. When satisfied, press `ENTER`
10. In the `Font Browser` GUI window press the `Save changes` button.
11. In the `Font Browser` GUI window press the `Re-render` button.
12. Choose another letter to edit.

*Press the <code>\`</code> key to toggle different editor modes: the "default" one and the "relative to the previous letter" one.*

![GIF with editing process](./docs/stage4_3_editing.gif)

After this, attempt to print the document via `step5_Printer.py` again, and see if the results are better.

*The user may further enhance the font by using the `step10_Marker.py` editor.*  
*The user may further enhance the font by manually adding the `previous letter` values into the `df.xls` files.*  

## License

The actual licenses are available at the beginning of each source code file; superficial overview:
- The `GUI` elements that rely on the `PyQt5` library are generally subject to GPL v3.
- Modules that don't rely on the `PyQt5` library are generally subject to Apache 2.0.

Any unmarked file is implied to be subject to Apache 2.0.
