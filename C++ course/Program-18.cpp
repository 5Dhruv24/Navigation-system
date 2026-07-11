# include<iostream>
using namespace std;


class new90{
    int a,b;
    friend new90 valueassum(new90 m,new90 n); 
    public:
        void enterdata(int N1,int N2){
            a=N1;
            b=N2;
        }

        void showdata(){
            cout<<"The sum of both number is "<<a+b<<"."<<endl;
        }

};

new90 valueassum(new90 m,new90 n){
    new90 z;
    int x=m.a+n.a;
    int y=m.b+n.b;
    z.enterdata(x,y);
    return z;
    
}

int main(){
    new90 o1,o2,o3;
    o1.enterdata(1,2);
    o1.showdata();
    o2.enterdata(3,4);
    o2.showdata();
    o3=valueassum(o1,o2);
    o3.showdata();
    return 0;
}