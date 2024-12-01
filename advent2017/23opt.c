#include <stdio.h>

// Day 23 part 2: decoded assembly

/*constexpr
static int func(void){


}*/

int main(){
	int b,c,d,h=0;
	b= 57;
	b*=100;
	b+=100000;
	c = b + 17017;
	do{
		for(d=2;d*d <= b; d++){
			if( (b%d==0) ){
				h++;
				break;
			}
		}
		b+=17;
	} while (b!=c); //stop when b==c (1000 iterations)
	
	printf("%d\n",h);
	//puts(itoa(h));
	return 0;
}

