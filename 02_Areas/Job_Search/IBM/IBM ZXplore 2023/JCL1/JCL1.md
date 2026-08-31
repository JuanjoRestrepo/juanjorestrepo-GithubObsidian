
**PURPOSE**

Your  mission is to learn the concept of job cards, job scheduling, data definition (DD) statements, disposition (DISP) parameters, and reading output.

Think back to what you learned in the Files Challenge -- we had you right-click on a file and submit it. 

Did you peek in the file and see what it looked like?

//CHKSTAGE JOB
//EXP EXPORT SYMLIST=*
//SYM SET STAGE=FILES1
//CHKSTAGE  EXEC PGM=IKJEFT1A
//SYSPROC  DD DSN=VENDOR.CLIST,DISP=SHR
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *,SYMBOLS=EXECSYS
CHK -
&SYSUID. -
&STAGE
/*
	

You're all good either way, but in case you were wondering what that file _was_, it was **job control language (JCL)**, and we are going to learn more about it here. 

**Although JCL stands for job control language, don't think of it as a programming language**. It's merely a way of telling the IBM® z/OS® operating system what you'd like to do, and how you'd like to handle the details of that assignment. 

  

**FOR EXAMPLE**

If we were all working in an office, someone might say "Take the papers from the conference room, alphabetize them by last name, and put them on my desk." And then there might be a lively discussion about whether that's your job, but at least you'd understand the task at hand. 

There's an input, the papers, and a location of where to find it, the conference room; an action to be performed, alphabetize by the last name, and where to put the output, on the boss's desk. **JCL is very similar in that it's not just indicating "do this," but it's providing enough information around the task that it can be carried out exactly as intended**.


LOOK AT THIS JCL

![](https://cdn.filestackcontent.com/86w8h3kUQHmzTPU6RsKg)

It's stating:

_"Run this program, and this is how I want you to run it"_

The program is expecting some input, you'll find it here. And when you're done, put the output here.

We submit this JCL to z/OS and it's up to the job entry subsystem (JES) to get all of the pieces it needs to carry out its task, and then actually carry out the steps described in the JCL. Every time JCL is submitted, it creates what's known as a _job_, and we can look at that job as JES holds onto it, gets it ready for execution, and starts printing the output.

So, in addition to any output it might generate, we can also look at the job output through Visual Studio (VS) Code and make sure that it ran correctly. All of these steps sounds tricky, but we'll walk you through all of it in this JCL challenge.

# Challenge
---

![[JCL1Challenge.pdf]]

