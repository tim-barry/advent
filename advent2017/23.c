#include <stdio.h>

// Day 23 part 2: decoded assembly

int main(){
	int a=1,b=0,c=0,d=0,e=0,f=0,g=0,h=0;
	b= 57;
	c= b;
	if(a!=0){
		b = b*100 + 100000;
		c = b + 17000;
	}
	do{
		f= 1;
		d= 2;
		e= 2;
		for(d=2;d*d < b; d++){ // check if b is a prime
			// the assembly doesn't have a % operator,
			// so it does 2 for loops with d and e and checks if d*e==b.
			if( (b%d==0) ){
				f=0;
				break;
			}
		}
		if(f==0) // not a prime
			h++;
		g = b-c;
		b+=17;
	} while (g!=0); //stop when b==c (1000 iterations)
	
	printf("%d\n",h);
	return 0;
}


int original_main(){
	int a=1,b=0,c=0,d=0,e=0,f=0,g=0,h=0;
	b= 57;
	//if (a!=0){ //# jnz a 2
	//	//#jmp +5
	//	b = b * 100;
	//	b = b + 100000;
	//	c = b;
	//	c+= 17000;
	//}
	b = b*100 + 100000;
	c = b + 17000;
	do{
		f= 1;  //lbl A
		d= 2;
		e= 2;
//		do{
			for(d=2;d*d < b; d++){
				if( (b%d==0) ){
					f=0;
					break;
				}
			}
			/*do{
				g= d*e-b;// for all d>2
				// such that b-2*e is zero
				//g*=e;
				//g = g-b;
				if(g==0) // #jnz g 2
					f=0; // break
				e++;
				g = e-b;
				//g -= b;
			}while ((g!=0)&&(f)); //jnz g -8
			*/ // g==0
//			d++; // do (b-d) times
//			g=d-b;
			//g-=b;
//		}while ((g!=0)&&(f)); //jnz g -13
		if(f==0) //#jnz f 2
			h++;
		g = b-c;
		//g -= c;
		//if (g==0):
		//	END
		b+=17;
	} while (g!=0); //stop when b==c
	
	printf("%d\n",h);
	return 0;
}
