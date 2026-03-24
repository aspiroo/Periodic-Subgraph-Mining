#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <list>
#include <math.h>

#include "myList.cpp"
#include "Table.cpp"
#include "GetStat.cpp"

using namespace std;


Table* H;
ListNode* A[41][41];


ListNode * Update(ListNode* L, int t, int p, int Sigma);
ListNode * Update_special(ListNode *L,int t,int p,int Sigma);
bool Subsume(ListNode* G, int p, int Sigma);

void printGx(ListNode* G, int period)
{
      fstream myfile;
      myfile.open("c:/Users/safwa/Periodic-Subgraph-Mining/results/list_miner/default_run/results.txt",ios::app | ios::out);
      myfile<<G->start<<" "<<G->end<<" "<<G->support<<" "<<period<<endl;
      myfile<<"  [ ";
      list<int> Gt (G->graph);
      for(list<int>::iterator iter = Gt.begin(); iter!= Gt.end(); iter++ )
              myfile<<*iter <<"  ";
      myfile<<"]"<< endl;


      myfile.close();

      //At the same time compute the statistics


}

int Miner(int Sigma, int Pmax)
{

   //start mining
   fstream myfile;
   //myfile.open("enron-dated.itemset", fstream::in);
   //myfile.open("enron-large", fstream::in);
   myfile.open("c:/Users/safwa/Periodic-Subgraph-Mining/data/processed/listMinerInputs.txt",fstream::in);
   //myfile.open("test1",fstream::in);
   //myfile.open("test",fstream::in);
   if(myfile.is_open())
   {
     int t=0;
     while(myfile.good() )
     {
      t++;
      cout<<"the t value is "<<t<<endl;
      string a;
      getline(myfile, a);
      list<int> Gt;
      get_graph(a, Gt);    //Now we get the graph at time t as vector Gt


      //update the head of list and update the list
      if(Gt.size()!=0) {
      	for(int p=1; p<=min(t,Pmax); p++)
      	{
        	int phase = t%p;
       	   	ListNode *L;
                L = A[p][phase];
          	ListNode *N =  Creat_ListNode(Gt, t,t,1);
                list<int> tempG = N->graph;
        //        cout<<"in miner the size of graph is "<<tempG.size()<<endl;
          	L = push_head(N,L);
       //         cout<<"push head succeed "<<endl;
          	L = Update(L,t,p, Sigma);
                A[p][phase]= L;
    	  }
     }
      else{  //Gt.size()==0
          for(int p=1; p<= min(t,Pmax); p++)
          {
                int phase = t%p;
                ListNode *L;
                L = A[p][phase];
                Update_special(L,t,p,Sigma);
                A[p][phase] = NULL;
          }
       }

}
    myfile.close();



    cout<<"dealing with the rest part"<<endl;
     for(int i=0;i<=Pmax;i++)
         for(int j=0;j<i;j++)
         {
            ListNode* L;
            L = A[i][j] ;
            if(L!=NULL){
                 ListNode *p;
         	   for(p=L; p!=NULL && p->start>0; p = p->next)
      	  	    {
                          cout<<" dealing with the rest of p "<<i<<endl;
                          cout<<p->start <<" " <<p->end <<" "<<p->support<<endl;
      	         	  if(!Subsume(p,i, Sigma) && p->support>=Sigma)
    	                             printGx(p, i);
     	       	   }
      	         	 delete_whole(L);
                         A[i][j]=NULL;
             }
         }

    }
   else
      cout<<"Unable to open file"<<endl;
   return 0;
}



ListNode* Update(ListNode * L, int t, int period, int Sigma)
{
   ListNode * Be = L;

   if( Be->next ==NULL || Be==NULL )
                return L;

//   cout<<"Update the list "<<endl;

   ListNode *p;
   p = Be;
   p = p->next;
   ListNode *prev = Be;
   ListNode *prevprev = Be;

 //  cout<<"the start time of Gt is "<<Be->start <<endl;
   list<int> Gt( Be->graph );
 //  cout<<"the size of Gt is "<<Gt.size()<<endl;

   while(p!=NULL)
   {
        ListNode *N = p;
        list<int> F( N->graph );
        list<int> C( Intersect(Gt, F) ); //C is the common subgraph of Gt and F

        if(C.size()>0 && C.size()==F.size() ) //which means that F is contained in Gt
        {
             while(p!=NULL)
             {
           //      cout<<"t value is "<< t<< "case 1"<<endl;
                 N = p;
           //      cout<<"the start time"<<p->start<<endl;
                 N->end =t ;
                 N->support = N->support +1;

                 //delete any duplicate graph
                    if( EqualGraph(prev->graph, N->graph ) )
                    {
                    //  L = delete_previous2(L, prev, N);
                      L = delete_current(L,prev,prevprev);
                      if(prevprev == NULL)
                            prevprev = L;
                      // else prevprev doesn't change
                      prev = p;
                      p = p->next;
                    }
                     else{
                        prevprev = prev;
                        prev = p;
                        p = p->next;
                     }
             }
            return L;
        }

        else{

            if(C.size()==0)  //which means that C is empty
             {
                while(p!=NULL)
                {
                   if(t==29) cout<<"t is "<<t << "case 2"<<endl;
                   N = p;
                   ListNode *qq = p->next;
                   list<int> tempGG = N->graph;
                   if(t==29) cout<< N->support <<" "<<N->start <<"  "<<N-> end <<"size of the graph "<<tempGG.size()<<endl;
                   if(!Subsume(N, period, Sigma) && N->support>=Sigma)
                   {
                            printGx(N, period);
                   }
                   L = delete_current( L, N ,prev);
                   p = qq;
                }
                return L;
             }
             else          //which means that C is not empty and C!=F
                {

                  if(!Subsume(N, period, Sigma) && N->support>=Sigma)
                            printGx(N,period);
                  update_graph(N,C);
                  N->end = t;
                  N->support = N->support +1;

                  //delete any duplicate graph
                    if( EqualGraph(prev->graph, N->graph ) )
                    {
                      //L = delete_previous2(L, prev, N);
                      L = delete_current(L,prev,prevprev);
                      //prevprev doesn't change
                      prev = p;
                      p = p->next;
                    }
                     else{
                        prevprev = prev;
                        prev = p;
                        p = p->next;
                     }

                } //inner else
             }//outer else

   }//end whil

   return L;



}//end Update

ListNode* Update_special(ListNode * L, int t, int period, int Sigma){

   if(L==NULL)
       return L;
   else{
        ListNode *p=L;
        while(p!=NULL)
                {
                   ListNode *N = p;
                   p=p->next;
                   if(!Subsume(N, period, Sigma) && N->support >=Sigma && (N->graph).size()>0)
                   {
                            printGx(N, period);
                   }

                }
         delete_whole(L);
   }
   return NULL;

}

bool Subsume(ListNode *G, int p, int Sigma)
{
    bool subsumed = false;
    list<descp> Dset (H->search(G->graph) );

    if(Dset.size()==0)
    {
         if(G->support>=Sigma)
            H->insert(G->graph, G->start, G->end, p);
    }//end if
    else
    {
         for(list<descp>::iterator itD = Dset.begin(); itD!=Dset.end(); itD++){
              if( p%( itD->period )==0  && G->start >= itD->start && G->end <= itD->end)
              {
                   subsumed = true;
                   break;
              }
         }

         if(subsumed==false && G->support>=Sigma)
         {
              H->insert(G->graph, G->start, G->end, p);
         }

    }//end else
    return subsumed;
}

int main(){
   H = new Table();
   for(int i=0;i<40+1;i++)
      for(int j=0;j<40+1; j++)
         {
            A[i][j] = NULL;
         }

   Miner(3, 10);

   stats();

   return 1;

}
