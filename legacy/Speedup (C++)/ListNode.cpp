#include <list>
#include <iostream>

using namespace std;

struct ListNode{
  list<int> graph;
  int support;
  int start;
  int end;
  ListNode* next;
};


ListNode* Creat_ListNode(list<int> Gt, int s, int t, int n)
{
       ListNode *a = new ListNode; 
       for(list<int>::iterator iter=Gt.begin(); iter!=Gt.end(); iter++)
              (a->graph).push_back(*iter);
 //      cout<<"the size of the graph is "<<(a->graph).size()<<endl; 
       a->start = s;
       a->end = t;
       a->support = n;
       a->next = NULL;
 //      cout<<" start "<<s << "end"<< t<< "support" <<n <<endl; 

       return a;
}


void update_graph(ListNode *N, list<int> C){
    (N->graph).clear();
    for(list<int>::iterator it = C.begin(); it!= C.end(); it++)
              (N->graph).push_back(*it);

}   





