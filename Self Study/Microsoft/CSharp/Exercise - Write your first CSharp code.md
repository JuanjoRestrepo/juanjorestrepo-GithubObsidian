### Hello World
---
```C#
Console.WriteLine("Hello World!");
```

### What to do if you get an error message
---
For example, if you were to incorrectly enter a lower-case `c` in the word `console` like so:
```C#
console.WriteLine("Hello World!");

//(1,1): error CS0103: The name 'console' does not exist in the current context
```

The first part `(1,1)` indicates the line and column where the error occurred.

Similarly, if you used single-quotation marks (`'`) to surround the literal string `Hello World!` like so:
```C#
Console.WriteLine('Hello World!');
//(1,19): error CS1012: Too many characters in character literal
```

Again, in line 1, character 19 points to the culprit. You can use the message as a clue as you investigate the problem. But what does the error message mean? What exactly is a "character literal?" Later, you'll learn more about literals of various data types (including character literals). For now, be careful when you're entering code.

### Common mistakes new programmers make:
---
- Entering lower-case letters instead of capitalizing `C` in `Console`, or the letters `W` or `L` in `WriteLine`.
- Entering a comma instead of a period between `Console` and `WriteLine`.
- Forgetting to use double-quotation marks, or using single-quotation marks to surround the phrase `Hello World!`.
- Forgetting a semi-colon at the end of the command.

You can create a code comment by prefixing a line of code with two forward slashes `//`.

```C#
// Console.WriteLine("Hello World!");
```

Add new lines of code to match the following code snippet:
```C#
Console.Write("Congratulations!");
Console.Write(" ");
Console.Write("You wrote your first lines of code.");

// Output:
// Congratulations! You wrote your first lines of code.
```

### The difference between Console.Write and Console.WriteLine
---
The three new lines of code you added demonstrated the difference between the [Console.WriteLine()](https://learn.microsoft.com/en-us/dotnet/api/system.console.writeline#system-console-writeline) and [Console.Write](https://learn.microsoft.com/en-us/dotnet/api/system.console.write) methods.

To print an entire message to the output console, you used the first technique, `Console.WriteLine()`. At the end of the line, it added a line feed similar to how to create a new line of text by pressing Enter or Return.

To print to the output console, but without adding a line feed at the end, you used the second technique, `Console.Write()`. So, the next call to `Console.Write()` prints another message to the same line.
