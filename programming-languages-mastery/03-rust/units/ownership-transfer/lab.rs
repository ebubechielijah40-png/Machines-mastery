use std::cell::RefCell;
use std::rc::Rc;
use std::thread;

#[derive(Clone, Debug, PartialEq)]
pub struct Packet { bytes: Vec<u8> }
#[derive(Debug, PartialEq)]
pub enum PacketError { BadLength, BadIndex }
impl Packet {
    pub fn new(bytes: Vec<u8>) -> Result<Self, PacketError> {
        if bytes.is_empty() || bytes.len() > 4096 { return Err(PacketError::BadLength); }
        Ok(Self { bytes })
    }
    pub fn view(&self) -> &[u8] { &self.bytes }
    pub fn set(&mut self, index: usize, value: u8) -> Result<(), PacketError> {
        let entry = self.bytes.get_mut(index).ok_or(PacketError::BadIndex)?;
        *entry = value;
        Ok(())
    }
    pub fn into_bytes(self) -> Vec<u8> { self.bytes }
}
struct Tracked { label: &'static str, events: Rc<RefCell<Vec<&'static str>>> }
impl Drop for Tracked {
    fn drop(&mut self) { self.events.borrow_mut().push(self.label); }
}
fn tracked(label: &'static str, events: &Rc<RefCell<Vec<&'static str>>>) -> Tracked {
    Tracked { label, events: events.clone() }
}
fn main() {
    let mut vector = Vec::new();
    let mut transitions = Vec::new();
    let mut previous = vector.capacity();
    for value in 0..33u8 {
        vector.push(value);
        if vector.capacity() != previous {
            transitions.push((vector.len(), vector.capacity()));
            previous = vector.capacity();
        }
    }
    let pointer = vector.as_ptr() as usize;
    let packet = Packet::new(vector).unwrap();
    let handle = thread::spawn(move || {
        let same_buffer = packet.view().as_ptr() as usize == pointer;
        let sum: u64 = packet.view().iter().map(|&b| u64::from(b)).sum();
        (same_buffer, sum, packet)
    });
    let (same_buffer, sum, returned) = handle.join().unwrap();
    assert_eq!(sum, 528);
    assert!(same_buffer);
    println!("capacity_transitions={transitions:?}");
    println!("move_preserved_buffer={same_buffer};sum={sum};length={}", returned.view().len());
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn rejects_lengths() {
        assert_eq!(Packet::new(vec![]), Err(PacketError::BadLength));
        assert_eq!(Packet::new(vec![0;4097]), Err(PacketError::BadLength));
        assert_eq!(Packet::new(vec![0;4096]).unwrap().view().len(),4096);
    }
    #[test] fn shared_read_and_later_exclusive_write() {
        let mut p = Packet::new(vec![2,3]).unwrap();
        let first = p.view(); let second = p.view();
        assert_eq!((first[0],second[1]),(2,3));
        p.set(0,7).unwrap();
        assert_eq!(p.view(), &[7,3]);
    }
    #[test] fn checked_failure_preserves_buffer() {
        let mut p=Packet::new(vec![1,2]).unwrap();
        assert_eq!(p.set(2,8),Err(PacketError::BadIndex));
        assert_eq!(p.view(), &[1,2]);
    }
    #[test] fn clone_owns_independent_bytes() {
        let p=Packet::new(vec![3,4]).unwrap();let mut q=p.clone();
        q.set(0,9).unwrap();assert_eq!(p.view(),&[3,4]);assert_eq!(q.view(),&[9,4]);
    }
    #[test] fn consume_returns_allocation() {
        let input=vec![8,9];let pointer=input.as_ptr();
        let output=Packet::new(input).unwrap().into_bytes();
        assert_eq!(pointer,output.as_ptr());assert_eq!(output,vec![8,9]);
    }
    #[test] fn local_drop_order_is_reverse_declaration() {
        let events=Rc::new(RefCell::new(Vec::new()));
        { let _a=tracked("A",&events);let _b=tracked("B",&events); }
        assert_eq!(*events.borrow(),vec!["B","A"]);
    }
    #[test] fn struct_fields_drop_in_declaration_order() {
        struct Group { _a:Tracked, _b:Tracked }
        let events=Rc::new(RefCell::new(Vec::new()));
        { let _group=Group{_a:tracked("A",&events),_b:tracked("B",&events)}; }
        assert_eq!(*events.borrow(),vec!["A","B"]);
    }
    #[test] fn thread_transfers_owned_buffer() {
        let p=Packet::new(vec![4,5,6]).unwrap();
        let handle=thread::spawn(move || p.into_bytes());
        assert_eq!(handle.join().unwrap(),vec![4,5,6]);
    }
}
