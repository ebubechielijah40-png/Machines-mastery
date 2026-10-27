fn bad() -> &'static str { let temporary=String::from("local"); &temporary }
fn main() { println!("{}",bad()); }
