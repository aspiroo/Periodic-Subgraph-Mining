#include <list>
#include <vector>
#include <iostream>

using namespace std;

struct Descriptor{
  list<int> graph;
  int start, end, period;
};

struct descp{
  int start, end, period;
};


bool EqualGraph(list<int> G1, list<int> G2)
{
 //    cout<<" the size of G1 "<<G1.size()<< " the size of G2 " <<G2.size()<<endl;
     if(G1.size()!= G2.size())
         return false;
     else{
         list<int>::iterator iter1, iter2;
         for(iter1=G1.begin(), iter2=G2.begin(); iter1!=G1.end() && iter2!=G2.end(); iter1++, iter2++)
         {
                     if(*iter1!=*iter2)
                          return false;
         }
         return true;
     }
}

class Table{
  public:
    //Descriptor* search(list<int> G);
    list<descp> search(list<int> G);
    void insert(list<int> G, int s, int t, int n);
    Table();
    ~Table();
  private:
    vector< list<Descriptor> >  table;
};


Table::Table()
{ 
   list<Descriptor> Temp;
   for(unsigned int i=0;i<22111;i++)
          table.push_back(Temp);

   cout<<"creat table is done "<<endl;
}

Table::~Table()
{
    table.clear();
}

list<descp> Table::search(list<int> G)
{
    long int p = 193939;
    for(list<int>::iterator it=G.begin(); it!=G.end(); it++)
            p *= ( (*it) +1 ) % 193939;
    unsigned int h = (unsigned int) p%22111;
    
//   cout<<"the size of h " << (table[h]).size()<<endl;
//    cout<<"value of h is "<<h<<endl;
    
    list<descp> A;
    
    list<Descriptor>::iterator itd = (table[h]).begin();
    while(itd != (table[h]).end() )
    {

            if(EqualGraph(itd->graph, G))
            {
                descp a;
                a.start = itd->start;
                a.end = itd->end;
                a.period = itd->period;
                A.push_front(a);
            }
            itd++;
    }
    return A;
}

void Table::insert(list<int> G, int s, int t, int n)
{
    Descriptor A;
    A.start =s; A.end = t; A.period = n; 

 //   cout<<A.start<<" "<<A.end<<" "<<A.period<<endl;

    long int p = 193939;
    for(list<int>::iterator it=G.begin(); it!=G.end(); it++)
            p *= ( (*it) +1 ) % 193939;
    unsigned int h = (unsigned int) p%22111;

    for(list<int>::iterator it=G.begin(); it!=G.end(); it++)
          (A.graph).push_back(*it);

   ( table[h] ).push_front(A);
 //  cout<<" after insert the size of h " << (table[h]).size()<<endl;
}

