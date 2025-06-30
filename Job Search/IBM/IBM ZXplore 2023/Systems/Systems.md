
The IBM® z/OS® operating system is the _flagship_ operating system running on the IBM Z® hardware. The z/OS operating is trusted by the biggest businesses and governments worldwide to manage critical data. These organizations expect the z/OS operating system to be operational 24 hours a day, 365 days a year.

If these machines aren't operational for any amount of time, it could be a massive problem for these organizations. The IBM Z mainframe is built to have zero down time - in fact, the _Z_ in the name actually refers to _zero_.

**So**

Why do these businesses and governments trust management of critical data to the z/OS operating system and the IBM Z mainframe?

To meet the ever-evolving needs of IBM Z clients, the technology has been consistently improved and advanced.

The operating systems for personal computers work by having other tasks wait while one task is being executed. The z/OS operating system, running on an IBM Z server, is designed for _mixed_ work where many tasks are running at once. The z/OS operating system is constantly receiving millions of requests to process critical data.

---

_How do these IBM Z systems manage all the massive volume of daily workload?_

_How does the z/OS operating system process millions of requests per second concurrently?_

---

These questions are great ones. And we'll explain.

The z/OS operating system consist of _components_ that work together. These components include:![](https://cdn.filestackcontent.com/DW2x3ZC4SkSnzQqMqVtL)

- Operating system service tasks
- Real-time transaction tasks
- Batch tasks

  

If you want to learn more about these components, we'll go into more detail now.

**OPERATING SYSTEM SERVICE TASKS**

The z/OS operating system service tasks act like a traffic coordinator for thousands of physical resources, including disk storage devices, network connections, processors and terabytes of memory in a single IBM Z system. Traffic flows through an IBM Z mainframe significantly faster than a general-purpose computer. The reason is because the IBM Z system is designed for input and output (I/O) throughput. Some z/OS operating system service tasks are known as _started tasks_, meaning they can be started and made immediately available to batch tasks and real-time transaction tasks. Started tasks are generally used for long-running critical applications. An advantage offered by started tasks are control over where and when the job control language (JCL) is run. For example, you could have the JCL started at each initial program load (IPL) of the system.

  

**REAL-TIME TRANSACTION TASKS**

Real-time transaction tasks are interactive and typically involve a relatively small amount of input to quickly return a result. The entire I/O round trip of a transaction is much less than a millisecond. The real-time transaction task relies upon z/OS operating system services to load the appropriate program, get data requested by the program from the IBM Z managed physical resources, then send result to the requesting application or users. Real-time transaction tasks are generally _started tasks_ initiated when the operating system starts, IPLs, ready to receive requests, immediately process the request, and return the result.

  

**AN EXAMPLE**

Have you ever been checking out at a store and wondered what happened _after_ you swipe your credit?

A credit card swipe travels through the public network into an IBM Z mainframe computer where a real-time transaction task is waiting – ready to receive the request.  In the case of a credit card swipe, a program was loaded to look up data about the credit card account. _Approved_ or _denied_ is returned and disk storage credit card account balance was updated upon approval.  Millions of these happen every second of every day.

  

What kind of real-time transaction systems are out there?

****REAL-TIME TRANSACTION SYSTEMS****

  

**IBM CICS**®** (Customer Information Control System)  
**

[IBM CICS**®**](https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-introduction-cics) is a z/OS real-time transaction processor started task. CICS can process transactions from hundreds of users at the same time as they run a variety of application programs. It processes about 1.1 million transactions per second - that's 100 billion per day. It's common for a single z/OS operating system to be concurrently running hundreds of CICS started tasks, called _regions_, where each CICS is concurrently processing many transactions. These transactions are the actions and updates resulting from messages sent to a CICS application program. Insurance companies use CICS to manage claims, travel companies use CICS to manage reservations and banks use CICS to track things like their clients’ deposits and withdrawals.

  

**IBM IMS**®** (Information Management System)**

[IBM IMS**®**](https://www.ibm.com/it-infrastructure/z/ims) is capable of both z/OS real-time transaction processing and data base transaction processing. IMS can process 21,000 transactions per second - over 1 billion per day.

  

**IBM z/OS UNIX System Services**®** (USS)**

[IBM z/OS USS****®****](https://www.ibm.com/docs/en/zos/2.3.0?topic=security-zos-unix-system-services) is a z/OS component that serves as a z/OS real-time started task that provides a UNIX-certified file and process environment, as well-known Transmission Control Protocol (TCP) applications, such as Secure Shell (SSH), File Transfer Protocol (FTP) and any TCP socket application processing.

  

**IBM DB2**® Family  
****

[IBM Db2****®****](https://www.ibm.com/docs/en/db2-for-zos/11?topic=getting-started-db2-zos) is real-time transaction started task managing a relational data base data source used by other transaction systems such as CICS, IMS, USS, time sharing option (TSO) and message queue (MQ).

  

**IBM MQ**®****

[IBM MQ****®****](https://www.ibm.com/products/mq/zos), a message delivery real-time transaction started task, helps make business application programming far easier. It simplified it by eliminating the need for business application programs to verify data was successfully sent and received by other business application programs within the same computer system or a foreign computer system, regardless of the computer hardware and operating systems. Examples of foreign computer systems are bank ATMs, hospital admissions, retail point of sales (POS), IBM business partners large-scale computer systems, and so on.  

  

**TIME SHARE OPTION (TSO)**

[TSO](https://www.ibm.com/docs/en/zos-basic-skills?topic=interfaces-what-is-tso) is a classic interactive system available before the internet and browsers. TSO is relied upon today and into the future by z/OS system programmers and administrators.

---

  

_Do other real-time transaction started tasks exists?_

Absolutely. The z[/OS operating system](https://www.ibm.com/it-infrastructure/z/zos), is concurrently running many real-time transactions started tasks, handling millions of business-critical transactions every second of every day. In fact, the IBM Z mainframe has other concurrently running operating systems, such as [IBM z/TPF® Transaction Processing Facility](https://www.ibm.com/products/z-transaction-processing-facility), dedicated to real-time transactions; and [IBM z/VSE®](https://www.ibm.com/it-infrastructure/z/zvse) operating system, often used to run CICS on smaller IBM Z systems.

We still have batch jobs to think about.


**BATCH TASKS**

Otherwise called batch jobs, batch tasks are used for bulk processing of data from real-time transactions. A batch job is a _submitted_ task workload for the system to complete in the background. It's best for processing a massive amount of data records.

An example might be a major retail company processing its daily inventory.

Batch jobs can also be a good fit for a sequence of activities, _job steps_, for which no user interaction is needed. The z/OS operating system typically processes many batch jobs while concurrently processing many real-time transactions.

A real-time system started task, _[IBM Job Entry Subsystem (JES)](https://www.ibm.com/docs/en/zos-basic-skills?topic=jobs-what-is-jes)_, is responsible of accepting _submitted_ batch work, scheduling the work according to a variety of priorities and managing the batch output.

Security and privacy are critical real-time system components in the z/OS environment. Security and privacy real-time started tasks are discussed in another challenge.

We've shown you a section of this image earlier, here it is full picture. You'll notice this image includes things we talked about in this article, but also other components that will be talked about later on (like security manager).

![](https://cdn.filestackcontent.com/ObgzAVRTzCkDx0MpOgwV)

