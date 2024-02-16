# Cat Gippity

Turbocharge your software development workflows by leveraging the power of AI.

When seeking coding help from AI models like GPT-4, you want to:

1. Give the model as much _relevant_ context as possible without exceeding the token limit.
2. Name your files and use delimiters to help the AI understand the content.
3. Explicitly instruct the model with clear and unambiguous prompts.

However, copying your project files, naming them, and delimiting them manually, is time consuming.

Also, you won't know you're going to exceed the token limit until you do:

<p align="center">
  <img src="./assets/chatgpt-token-error.png" alt="ChatGPT exceeded token limit error message" title="ChatGPT exceeded token limit error message" width="75%">
</p>

## ⚡ The Solution ⚡

Cat Gippity solves these issues for you.

Run the script from your project folder and choose to add on a pre-prompt:

<p align="center">
  <img src="./assets/cat-gpty-choose-prompt.png" alt="Cat Gippity first screen - choose a prompt" title="Cat Gippity first screen - choose a prompt">
</p>

Select the files you want to include. The token count is dynamically updated:

<p align="center">
  <img src="./assets/cat-gpty-choose-files.png" alt="Cat Gippity second screen - choose files" title="Cat Gippity second screen - choose files">
</p>

The contents of your project files are individually named, delimited, and concatenated together, then copied to your clipboard.

You get the optimum context from your project with only a few key presses. 🚀🚀

Remember to paste in your requirements or error messages if you chose 5. or 6:

<p align="center">
<img src="./assets/chatgpt-placeholder.png" alt="ChatGPT window with placeholder text showing" title="ChatGPT window with placeholder text showing">
</p>

<p align="center">
  <img src="./assets/chatgpt-with-error.png" alt="ChatGPT window with error message pasted into prompt" title="ChatGPT window with error message pasted into prompt">
</p>

💡 Pro tip: iterate! It pays to have the AI check its answers. You can also combine prompts - first review your code for bugs, then again for vulnerabilities, and so on.

## Getting started

NOTE: this is an early release. It was developed on WSL Ubuntu and has been tested on Kali.

1. Start by running this command to install the script using curl.

```bash
curl -L "https://github.com/angusgee/cat-gpty/releases/tag/v0.1.0-alpha/catgpty" -o /tmp/catgpty
```

2. Next, move the program into your /usr/local/bin directory - or anywhere else you please:

```bash
sudo mv /tmp/catgpty /usr/local/bin/catgpty
```

3. Finally, give the script executable permissions:

```bash
sudo chmod +x /usr/local/bin/catgpty
```

Now you can run Chat Gippity from any folder:

```bash
catgpty
```

## Known issues

### Clipboard not working on Kali

- as a Kali user, if I follow the instructions, the program runs, and outputs a prompts\*.txt file.
- but the prompt is not copied to the clipboard.
