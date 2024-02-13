# Cat Gippity

Cat Gippity is a Linux utility for improved prompting.

For optimum results from AI, it's best to give the model the entire context of your project, and use delimiters to help it parse the content. You also want to use very clear proompts to explicitly instruct the model to do your bidding.

However, copying all your project files' contents, delimiting manually, and pasting into ChatGPT or a similar API is time consuming. Also, you won't know you're going to exceed the token limit until you do.

## Solution

Cat Gippity solves these issues for you.

Run the script from your project root folder and select the files to include. The token count is dynamically updated.

Run the script from your project folder and choose to add on a pre-proompt:

![Cat Gippity first screen - choose a prompt](./cat-gpty-choose-prompt.png)

- Error checking
- Security vulnerability assessment
- Improve memory and time complexity
- Add comments and create documentation
- Add requirements to your project e.g. new component
- Help to resolve error messages

Select the files you want to include in the message.

![Cat Gippity second screen - choose files](./cat-gpty.png)

The contents of your project are named, delimited with tripe backticks and concatenated together, then exported to a file and copied to your clipboard.

You get the optimum context from your project with only a couple of key presses.

Pro tip: iterate! Checking again only takes a few more seconds and helps prevent innacurate results. Why not have it review your code for bugs, then check it again for vulnerabilities?

## Getting started

tbc
