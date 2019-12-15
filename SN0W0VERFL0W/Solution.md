## Hello! Welcome to my solution for the SN0W0VERFL0W challenge.

* As the name suggested, we should approach this challenge with a Buffer Overflow exploit in our mindset. 
* The prompt given to us is down below.

![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/SN0W0VERFL0W.png)

### 1. Let's first try and run the executable they give us and see what we get.

![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/firstrun.png)
  
   * As we can see, the executable is prompting for some user input. After we type in something, it will print out "Mhmmm... Boring..." 
   * Since it's taking user input, we can proceed to check if the program is vulnerable to Buffer Overflow. One way to test it is to just input a really really long string to the input, and if the program outputs a SEGFAULT, then we know it's vulnerable.
   * There are various ways to do this, but I usually like to just pipe some python script into the executable!
  
  ```terminal
  python -c "print('A'*100)" | ./chall
  ```
    ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/2.png)
  
   * And we did get a SEGFAULT! Perfect! Now we know that this executable is vulnerable to Buffer Overflow cause we overflow the return address of whatever function being called causing it to access invalid address in memory.
  
### 2. Next, we need to find out how big the buffer is

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
  
  * A lot of registers here are not related to what we are doing, and we only need to care about the RSP(stack pointer) and RBP(base pointer)
  
### 3. Analyze gdb result
  
  * Before diving into the actual content of RSP and RBP we just get, let's take a look at the stack layout when a method is call
  
  ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/x64_frame_nonleaf.png)
  
  * As you can see, local variables are push below RBP(at a negative index). We can assume in the context of our binary, the buffer is below the RBP and it's growing upward toward the RBP. During buffer overflow, the saved RBP and returned address can be overwritten with whatever we just input in to overflow the buffer.
  * If you take a look at the registers' state above, we can see that RBP = 0x4545444444444343, and RSP = 0x7fffffffdf38.
  * During stack clean up, RSP points back to RBP, so we know that 0x7fffffffdf38 is the memory address of RBP
  * RBP has been overwritten with some weird pattern, as you can see. These are the ascii values of the character we type in! 
  * In ascii, 'C'= 0x43, 'D' = 0x44, and 'E'=0x45. So now, we can start understanding the layout on the actual stack.
  * Since our padding is "AAAABBBBCCCCDDDDEEEEFFFFGGGG", and we overwrite the RBP with CCDDDDEE, we know that the buffer is length(AAAABBBBCC) = 10 bytes!
  * After these 10 bytes, the next 8 bytes will overwrite the RBP(as we can see up there), and the next 8 bytes after that will overwrite the return address to jump to anywhere we want!
  * To test this, let's go back to our python script. Let's try and jump back to the leave instruction(it should be right before ret instruction. We know the ret instruction is at 0x401201 through `info registers`, so leave is at 0x401200
  ```python
  import struct
  padding = "AAAABBBBCC"
  rbp = "CCDDDDEE"
  ret_addr = struct.pack('I', 0x401200)
  ret_addr1 = struct.pack('I', 0x0000) # padd the address up to 8 bytes to fully overwrite the RSP
  
  print(padding + rbp + ret_addr + ret_addr1)
  ```
  * Before run this again, you should create a break point at the leave instruction just so we know if we sucessfully jump back here. Type ``` break *0x401200 ``` or whatever the address on your machine is
  * run ``` python your_script_name.py > exploit ``` again, and pipe it in gdb just like how we did above
  * When we run the executable in gdb, we should hit the breakpoint at leave! Type ``` s ``` to step 1 step to the return instruction
  * At this point, you can ``` info registers ``` to see that you have written into RBP with "CCDDDDEE"
  * To see the current state of the stack, run ``` x/5wx $rsp ```. This will show the content of 5 words above where the current RSP is pointing(which is pointing at our RBP). We should see something like 
  ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/4.png)
  * The first 8 bytes we see is the return address on the stack. We can see that we have overwritten it to be 0x00401200!
  * If we ``` s ```, we can see that we hit the breakpoint again at leave! You can also check that we are correctly at the leave instruction by doing ``` x/i $rip ```
  
  ![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/5.png)
  * Awesome! Now we know that we can redirect code by redirecting to any address! So what can we do? Where should we jump to?
  
### 4. Where to get flag?
  * We can start dissecting the binary to look around for the flag, but since the binary is stripped, it's annoying to do it.
  * Let's just throw it into a disassembler! I'll use Hopper for this, but you can use any similar application.
  * After looking around at the different procedures in this binary in Hopper, there is one that stood out!
  
  
  
  
