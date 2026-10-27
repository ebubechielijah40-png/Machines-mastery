fn main() { let mut bytes=vec![1u8]; let view=&bytes; bytes.push(2); println!("{view:?}"); }
