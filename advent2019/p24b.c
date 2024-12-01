#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

typedef unsigned __int128 u128;

//#define DEBUG 1

#define SZ 300
const int MID = SZ/2;
u128 _arr[SZ];

const char* about =
"We use 75 bits (3 per bug).\n"
"Initialize our masks: "
"Low bit is the top left corner, "
"High bit is the bottom right corner.\n"
"Compile with g++ (for the masks)."
;

const u128 left_mask  = (1<<0)+(1<<15)+(1<<30)+(1ULL<<45)+(1ULL<<60);
const u128 right_mask = left_mask<<12;
const u128 high_mask  = (1<<0)+(1<<3)+(1<<6)+(1<<9)+(1<<12);
const u128 low_mask   = high_mask<<60;

const u128 all_mask   = left_mask * high_mask;
const u128 three_mask = all_mask | all_mask<<1;

const u128 the_middle = (1ULL<<(12*3));
const uint8_t mids[4] = {7*3, 11*3, 13*3, 17*3};
const u128 masks[4]   = {high_mask, left_mask, right_mask, low_mask};


void printb3(u128 bi){
	// Print a level to stdout.
	for(int i=0; i<25; i++){
		if(bi&1) putchar('#');
		else putchar('.');
		if(i%5==4) putchar('\n');
		bi>>=3;
	}
	printf("\n");
}

void printbc(u128 bi){
	// Print neighbour counts to stdout.
	for(int i=0; i<25; i++){
		putchar('0'+(bi&7));
		if(i%5==4) putchar('\n');
		bi>>=3;
	}
	printf("\n");
}

u128 read_input(){
	char c;
	u128 res = 0;
	u128 cur = 1;
	for(int i=0; i<25; i++){
		c = getchar();
		if (c=='\n') c = getchar();
		if (c=='#') res |= cur;
		cur<<=3;
	}
	return res;
}

u128 popcnt(u128 b){
	// almost all calls will count 0-5 bits
	uint32_t res;
	for(res=0; b; res++){
		b &= b-1;
	}
	return res;
}

uint32_t b3_to_bio(u128 b3) {
	"Intercal would allow a simple b3$all_mask ...";
	uint32_t bio = 0;
	uint8_t shift = 0;
	while(b3) {
		bio |= (b3&1)<<shift;
		shift+=1;
		b3>>=3;
	}
	return bio;
}

// Basic cellular automata functions

u128 neighbours(u128 state){
	// Same-layer neighbours
	u128 res = state >> 15; // shift up
	res += (state&~left_mask) >> 3; // shift left
	res += (state&~right_mask) << 3; // shift right
	res += (state&~low_mask) << 15; // shift down
	return res;
}

u128 next_state(u128 state, u128 res){
	"Apply cellular automaton rules (res is neighbour count)";
	u128 count_1 = res & ~res>>1 & ~res>>2 & all_mask;
	u128 count_2 = ~res & res>>1 & ~res>>2 & all_mask;
	return count_1 | (count_2 & ~state);
}


// Part 1 functions

bool check_seen(u128* seen, uint32_t sz, u128 val){
	for(uint32_t i=0; i<sz; i++) if(seen[i]==val) return true;
	return false;
}

u128 step_part1(u128 state){
	return next_state(state, neighbours(state));
}

void part1(u128 b){
	u128 seen[100];
	uint32_t sz = 0;
	while(!check_seen(seen, sz, b)){
		seen[sz++] = b;
		b = step_part1(b);
	}
	printf("Part 1: biodiversity is %d after %d minutes\n", b3_to_bio(b), sz);
	printb3(b);
}

// Part 2 functions

void step_arr(u128* arr, int minp, int maxp){
	u128 prev = 0;
	u128 cur = 0;
	u128 nex = 0;
	u128 res, in_out;
	u128 mask;
	uint8_t mid;
	"We go from out (negative) to in (positive)";
	for(int p=minp-1; p<=maxp+1; p++){
		"Advance our small sliding window";
#ifdef DEBUG
		printf("At level %d\n", p);
#endif
		prev = cur;
		cur = arr[p];
		nex = arr[p+1];
		"Compute the current level shift";
		res = step_part1(cur);
		"Compute the inner and outer level contributions. For each direction:";
		in_out = 0;
		u128 t_in = 0;
		u128 t_out = 0;
		//u128 t_add = 0;
		for(int i=0; i<4; i++){
			mask = masks[i];
			mid = mids[i];
#ifdef DEBUG
			printf("for mask %d (mid: %d):\n", i, mid);
#endif
			"Add the bugs from inside and then from outside";
			t_in += ((u128)popcnt(nex & mask))<<mid;
			//printbc(t_add);
			//t_in += t_add;
			t_out += mask * (prev>>mid & 1);
		}
#ifdef DEBUG
		printf("t_in is:\n");
		printbc(t_in);
#endif
		in_out = t_in+t_out;
		//printb3(in_out);
		"Avoid overflow (unwanted carry) of our 3-bit cells"
		"This is unnecessary if we use 4-bit cells.";
		in_out |= (in_out>>2 & all_mask)*3;
		in_out &= three_mask;
		res += in_out; // no unwanted carry
#ifdef DEBUG
		printf("Neighbours are:\n");
		printbc(res);
#endif
		"Apply cellular automaton rules";
		res = next_state(cur, res);
		"Ensure no bug in the centre (part 2)";
		res &= ~the_middle;
		"Save our state";
		arr[p] = res;
#ifdef DEBUG
		printf("resulting bugs are %d:\n", p);
		printb3(arr[p]);
#endif
	}
}

void part2(u128 b){
	_arr[MID] = b;
	for(int i=0; i<200; i++){
#ifdef DEBUG
		printf("after minute %d:\n", i+1);
#endif
		step_arr(_arr+MID, -2-i/2, i/2+2);
#ifdef DEBUG
		printf("\n\n");
#endif
	}
	uint32_t tot = 0;
	for(int i=-100; i<=100; i++){
	//for(int i=-100; i<=100; i++){
		tot += popcnt(_arr[MID+i]);
	}
	printf("Part 2: after 200 minutes there were %d bugs\n", tot);
}

void debug_masks(){
	for(int i=0; i<4; i++){
		printb3(masks[i]);
	}
	printb3(all_mask);
	printb3(the_middle);
}

int main(){
	u128 b = read_input();
	printb3(b);
	part1(b);
	part2(b);
	return 0;
}

