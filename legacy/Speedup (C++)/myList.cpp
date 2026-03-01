#include <iostream>
#include <list>

#include "ListNode.cpp"

using namespace std;


ListNode* push_head(ListNode *N, ListNode *L)
{
      if(L==NULL)
         return N;
      else{
         N->next = L; 
         return N;
      }
}

void delete_ListNode( ListNode *N){
    N->next = NULL;
    (N->graph).clear();
    delete N;
}

ListNode * delete_current( ListNode *L, ListNode *N , ListNode *prev)
{
      if(N == L)
      {
            L = L->next;
            delete_ListNode(N);
            return L;
      }
      else{
       
         prev->next = N->next;
         delete_ListNode(N);
        return L;
      }

}

ListNode* delete_previous2(ListNode *L, ListNode *prev, ListNode *N){
   if(L==prev)
   {
         L = prev->next;
         delete_ListNode(prev);
         return L;
   }
  else{
      ListNode *p = L->next;
      ListNode *q = L;
      while(p!=NULL){
           if(p == prev)
           {
                 q->next = p->next; 
                 delete_ListNode(prev);
                 return L;
           }
          q = p;
          p=p->next; 
         
      }

  }

}

ListNode* delete_previous(ListNode *L, ListNode *pprev, ListNode *prev, ListNode *N){

      if(prev == L)
      {
            L = L->next;
            delete_ListNode(prev);
            return L;
      }
      else{
       
         pprev->next = prev->next;
         delete_ListNode(prev);
         return L;
      }

}

void delete_whole(ListNode *L){
   ListNode *p = L->next;
   ListNode *q = L;
   while(p!=NULL)
   {
          delete_ListNode(q);
          q=p;
          p=p->next;
   }
   delete_ListNode(q);
}



list<int> Intersect(list<int>  G1, list<int>  G2)
{
    //compute the common subgraph of G1 and G2
    list<int>::iterator iter1, iter2;
    list<int> C;
   
    iter1=G1.begin();
    iter2=G2.begin();
    while(iter1!=G1.end() && iter2!=G2.end())
    {
        if( *iter1 == *iter2 )
        {
             C.push_back(*iter1);
             iter1++;
             iter2++;
        }
        else{
            if(*iter1<*iter2)
                 iter1++;
            else
                 iter2++;
        }
    }
    return C;
}



void get_graph(string a, list<int> & Gt)
{
    if(!a.empty())
      {
           size_t position = a.find(' ');
           size_t j=position+1;
           string temp;
           int t;
           while(j<a.size() )
           {
                 char c = a[j];
                 if(c!=' ')
                     temp.push_back(c);
                 else
                 {
                     t = atoi(temp.c_str());
                     Gt.push_back(t);
                     temp = "";
                 }
                 j++;
           }
           t = atoi(temp.c_str());
           Gt.push_back(t);
    }
}



