# A hyper-simple zero-pressure typing game/trainer
This was written a year ago as a personal project and is very likely to not represent my programming style today
<hr/>

### Features:
- Colour-codes characters for their current state
  - `Green` for untyped, `Dark green` for correct, `Red` for incorrect character and `White` for incorrect space.
- Takes text files with a word on each line as input for practice.
- Can select left, right, or both handed practice.
  - Displays word count for the above options.

### Ideas:
- Add extra commands to better control the script (eg; exit, reload, main menu)
- Cleaner system for handling typos (currently displays only the mistyped letter)
- Bigger text (if that's even possible in python xd)

### Known issues:
- Line wrapping causes a new line of incoming words to be printed every time a character is typed if there are enough large oncoming words.
  - To work around this, just make the window wider.

### Images:

File selection:
![](https://i.imgur.com/VxjaBwb.png)

Typing:
![](https://i.imgur.com/uiENvw8.png)
