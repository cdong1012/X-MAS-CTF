## Hello! Welcome to my solution for the SN0W0VERFL0W challenge.

* As the name suggested, we should approach this challenge with a Buffer Overflow exploit in our mindset. 
* The prompt given to us is down below.

![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/SN0W0VERFL0W.png)

1. Let's first try and run the executable they give us and see what we get.

![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/firstrun.png)
  
  * As we can see, the executable is prompting for some user input. After we type in something, it will print out "Mhmmm... Boring..." 
  * Since it's taking user input, we can proceed to check if the program is vulnerable to Buffer Overflow. One way to test it is to just input a really really long string to the input, and if the program outputs a SEGFAULT, then we know it's vulnerable.
  * There are various ways to do this, but I usually like to just pipe some python script into the executable!
  
  ```terminal
  python -c "print('A'*100)" | ./chall
  ```
  ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/2.png)
  
  * And we did get a SEGFAULT! Perfect! Now we know that this executable is vulnerable to Buffer Overflow cause we overflow the return address of whatever function being called causing it to access invalid address in memory.
  
2. Next, we need to find out how big the buffer is

  * We want to do this because we want to know the exact stack layout before the method returns. By knowing the exact length of the buffer, we can start injecting into the stack to overwrite the return address either to jump into shellcode, ret2libc, or just redirect the code flow to wherever we want.
  * Usually for this point, I like to create a python script to do this for me.
  ```python3
  padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGG"
  print(padding)
  ```
  * With a recognizable pattern like this, we can know what is exactly in the RBP, RSP, and return address at the point of segfault
  * Let's try and run gdb on the executable with the input from the python script.
  * First, run the command ``` python your_script_name.py > exploit ```. After this, the output of the script is contain in a file called "exploit"
  * After you run ``` gdb ./chall ```, type ``` r < exploit ``` in the gdb prompt.
  * This will automatically pipe the content of the exploit into the input of the executable
  * You should run into a segfault in gdb, and the program will come to a halt!
  * Next, we can check the registers of the system at the time of segfault by running ``` info registers ``` in gdb. You should see something like this 
  
  ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/3.png)
  
  
