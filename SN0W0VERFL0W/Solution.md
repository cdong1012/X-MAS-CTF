## Hello! Welcome to my solution for the SN0W0VERFL0W challenge.

* As the name suggested, we should approach this challenge with a Buffer Overflow exploit in our mindset. 
* The prompt given to us is down below.

![Alt text](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/SN0W0VERFL0W.png)

1. Let's first try and run the executable they give us and see what we get.

![Alt test](https://github.com/cdong1012/X-MAS-CTF/blob/master/SN0W0VERFL0W/images/firstrun.png)
  
  * As we can see, the executable is prompting for some user input. After we type in something, it will print out "Mhmmm... Boring..." 
  * Since it's taking user input, we can proceed to check if the program is vulnerable to Buffer Overflow. One way to test it is to just input a really really long string to the input, and if the program outputs a SEGFAULT, then we know it's vulnerable.
  * There are various ways to do this, but I usually like to just pipe some python script into the executable!
  
  ```terminal
  python -c "print('A'*100)" | ./chall
  ```
  
