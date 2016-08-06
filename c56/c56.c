#include <stdlib.h>
#include <stdio.h>

void rc4_gen(char *key, int keylen, char *stream, int streamlen)
{
	unsigned char S[256];
	int i,j;
	for (i=0; i<256; i++)
		S[i] = i;

	char tmp;
	for (i=0, j=0; i<256; i++)
	{
		j = (j+S[i]+(unsigned char)key[i%keylen])%256;
		tmp = S[i];
		S[i] = S[j];
		S[j] = tmp;
	}
	
	int x;
	for (i=0, j=0, x=0; x<streamlen; x++)
	{
		i = (i+1)%256;
		j = (j+S[i])%256;
		tmp = S[i];
		S[i] = S[j];
		S[j] = tmp;
		stream[x] = S[(S[i]+S[j])%256];
	}
	
	return;
}

//Uniformly random. My biases are small enough as it is
char randbyte()
{
	int x = rand();
	if (x > RAND_MAX & ~(255))
		return randbyte();
	return x%256;
}

char *cookie = "BE SURE TO DRINK YOUR OVALTINE";
void oracle(char *in, int inlen, char *out)
{
	char key[16];
	int i;
	for (i=0; i<16; i++)
		key[i] = randbyte();
		
	rc4_gen(key,16,out,inlen+30);

	for (i=0; i < inlen; i++)
		out[i] = out[i]^in[i];
	for (i=0; i< 30; i++)
		out[i+inlen] = out[i+inlen]^cookie[i];
	
	return;
}

char decrypt_pos(int pos)
{
	char *pad = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
	int padlen = 31-pos;
	
	char *out = (char *)malloc(64*sizeof(char));
	int i;
	int count[256] = {0};
	for (i=0; i < 1<<24; i++)
	{
		//cout << (int)(unsigned char)oracle(pad)[32] << endl;
		oracle(pad,padlen,out);
		unsigned int x = (unsigned char)out[31]; //Yes horrible casting
		count[x ^ 0xE0] += 4;	//Big bias here, but also small biases for the other two
		count[x ^ 0x20] += 1;
		count[x ^ 0x00] += 1;
	}
	
	free(out);
	
	int max_ct =  count[0];
	char max_ch = 0;
	for (i=0; i < 256; i++)
	{
		if (count[i] > max_ct)
		{
			max_ct = count[i];
			max_ch = i;
		}
	}
	
	return max_ch;
}

int main()
{
	char secret[31];
	int i;
	for (i=0; i < 30; i++)
		secret[i] = decrypt_pos(i);
	secret[30] = 0;
	printf("%s\n",secret);
}