package pipeline

import (
    "context"
    "errors"
    "fmt"
    "reflect"
    "testing"
    "time"
)
func joined(t *testing.T, done <-chan struct{}) {
    t.Helper()
    select { case <-done: case <-time.After(3*time.Second): t.Fatal("workers did not join") }
}
func TestExactValuesEveryWorkerCount(t *testing.T) {
    values := []int64{-1000000,-3,0,5,1000000}
    for workers:=1;workers<=16;workers++ {
        got,err:=Squares(context.Background(),values,workers)
        if err!=nil || !reflect.DeepEqual(got,[]int64{1000000000000,9,0,25,1000000000000}) { t.Fatalf("workers=%d got=%v err=%v",workers,got,err) }
    }
}
func TestEmpty(t *testing.T) {
    got,err:=Squares(context.Background(),nil,1)
    if err!=nil || len(got)!=0 { t.Fatalf("%v %v",got,err) }
}
func TestInvalidBeforeStart(t *testing.T) {
    if _,e:=Start(nil,nil,1);e==nil { t.Fatal("nil context accepted") }
    for _,w:=range []int{-1,0,17} { if _,e:=Start(context.Background(),nil,w);e==nil { t.Fatal(w) } }
    for _,input:=range [][]int64{{1000001},{-1000001},make([]int64,8193)} { if _,e:=Start(context.Background(),input,1);e==nil { t.Fatal("invalid input accepted") } }
}
func TestPreCancelled(t *testing.T) {
    ctx,cancel:=context.WithCancel(context.Background());cancel()
    if got,e:=Squares(ctx,[]int64{1,2},2);got!=nil || !errors.Is(e,context.Canceled) { t.Fatalf("%v %v",got,e) }
}
func TestCancelledAbandonedOutputJoinsAllStages(t *testing.T) {
    for trial:=0;trial<30;trial++ {
        ctx,cancel:=context.WithCancel(context.Background())
        stream,err:=Start(ctx,make([]int64,8192),4);if err!=nil { t.Fatal(err) }
        select { case <-stream.Results: case <-time.After(3*time.Second):cancel();t.Fatal("no first result") }
        // Stop receiving; cancellation must release both possible blocked sends.
        cancel();joined(t,stream.Done)
    }
}
func TestInputSnapshotIsIndependentAfterStart(t *testing.T) {
    values:=[]int64{3,4};stream,e:=Start(context.Background(),values,2);if e!=nil {t.Fatal(e)}
    values[0]=99
    got:=make([]int64,2)
    for result:=range stream.Results {got[result.Index]=result.Square};joined(t,stream.Done)
    if !reflect.DeepEqual(got,[]int64{9,16}) {t.Fatal(got)}
}
func TestChannelCopiesSliceDescriptor(t *testing.T) {
    original:=[]int{1,2};channel:=make(chan []int,1);channel<-original
    original[0]=7;received:=<-channel
    if received[0]!=7 {t.Fatal(received)}
    // This is sequential aliasing, not an intentional concurrent data race.
    copyValue:=append([]int(nil),original...);copyValue[0]=8
    if original[0]!=7 {t.Fatal(original)}
}
func TestAppendCapacityChangesAliasing(t *testing.T) {
    source:=make([]int,1,2);source[0]=1
    first:=append(source,3);second:=append(source,9)
    if first[1]!=9 || second[1]!=9 {t.Fatal(first,second)}
    grown:=append(first,4);grown[0]=8
    if source[0]!=1 {t.Fatal("growth did not detach from full backing array")}
}
func TestObservation(t *testing.T) {
    values,e:=Squares(context.Background(),[]int64{3,-2,5},3);if e!=nil {t.Fatal(e)}
    fmt.Printf("input=[3 -2 5]; ordered_squares=%v\n",values)
    ctx,cancel:=context.WithCancel(context.Background());stream,e:=Start(ctx,make([]int64,8192),2);if e!=nil {t.Fatal(e)}
    <-stream.Results;cancel();joined(t,stream.Done)
    fmt.Println("abandoned_output_after_first_result: all_stages_joined=true")
}
