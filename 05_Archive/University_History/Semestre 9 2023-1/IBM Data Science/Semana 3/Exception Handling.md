
## Try... Except...Else...Finally Statment
---
```Python
try:
	getfile = open("myfile", "r")
	getfile.write("My file for exception handling")
except IOError:
	print("Unable to open or read the data in the file")
else:
	print("The file was written successfully")
finally:
	getfile.close()
	print("File is now closed.")
```

### Try…except statement
---
This type of statement will first attempt to execute the code in the “try” block,  but if an error occurs it will kick out and begin searching for the exception that matches  the error. 

Once it finds the correct exception to handle the error it will then execute that line of code.


Because of this error the program skipped over the code lines under the “try” statement  and went directly to the exception line. 

Since this error fell within the IOError guidelines it printed “Unable to open or read the data in the file.” to our console.

#### But what happens if another error occurs that is not caught by the IOError? 

If that happened we would need to add another except statement. 

For this except statement you will notice that the type of error to catch is not specified. 

#### Adding the else statement

It will provide us a notification to the console that “The file was written successfully”. 

Now that we have defined what will happen if our program executes properly, or if an error occurs there is one last statement to add.

#### By adding a finally statement 

It will tell the program to close the file no matter the end result and print “File is now closed” to our console. 


# List of many more exceptions that are built into Python, 

Here is a list of them 
[https://docs.python.org/3/library/exceptions.html](https://docs.python.org/3/library/exceptions.html)
