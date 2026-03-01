#include <fstream>
#include <iostream>
#include <stdlib.h>

using namespace std;





int*  get_S(string a)
{
    cout<<"get in here"<<endl; 
    int *A = new int[3];
    int p;

    int j=0;
    int k=0; 
    string temp;
    while(j< 3 )
    {
        char c = a[k];
        if( c!=' ')
            temp.push_back(c);
        else
         {
             p = atoi(temp.c_str());
             A[j]= p;
             j++;
             temp = "";
         }
        k++;
    }
    A[0] =  ( (A[0])/100) * 100 ;
    cout<<A[0]<<" "<<A[1]<< " "<<A[2]<<endl; 
    cout<<"get out of here"<<endl; 
    return A;
}


int stats(){

int Stat[2100][100];
for(int i=0;i<2100;i++)
   for(int j =0; j<100;j++)
       Stat[i][j]=0;

int *PSE;
int start, support;

fstream f1,f2;
f1.open("results.txt", iostream::in);
string a;
while(f1.good()){
   getline(f1, a);
   if(a.size()>0){

       PSE = get_S(a);
       start = PSE[0];
       support = PSE[2];
       Stat[start][support] += 1;
   }
}
f1.close();


f2.open("results_stat.txt", iostream::out);
for(int i=0;i<2100;i++)
   for(int j=0; j<100; j++)
      if(Stat[i][j]>0)
          {
             cout<< i <<"-"<<j<<"=" <<Stat[i][j]<<endl;
             f2<< i <<"-"<<j<<"=" <<Stat[i][j]<<endl;
          }

f2.close();


return 1;

}


/*
int main(){
 
return stats();

}
*/




