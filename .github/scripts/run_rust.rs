// Generic verification driver for a Rust solution file. Compiled with plain
// `rustc` (no Cargo/serde) via the run_rust.py wrapper, which sets the
// SOLUTION_PATH env var and splices the solution file in at compile time.
//
// Convention: the solution file defines `fn solve(<params...>) -> <return>`
// with the problem's natural owned types (e.g. `fn solve(nums: Vec<i64>,
// target: i64) -> Vec<i64>`). Rust has no reflection, so the driver converts
// the JSON testcase to/from those types with the `FromValue` / `ToValue`
// traits below, and calls `solve` through the `Solvable` trait, which is
// implemented for fn items of each arity. Like Go, arguments are matched by
// position: the keys of a testcase's "input" object must be in the same order
// as `solve`'s parameters. New types (e.g. ListNode) only need their own
// `FromValue` / `ToValue` impls. No external crates needed.
#![allow(dead_code)]

include!(env!("SOLUTION_PATH"));

// ---- minimal JSON value type, parser, serializer (no external crates) ----

#[derive(Debug, Clone, PartialEq)]
enum Value {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<Value>),
    Obj(Vec<(String, Value)>),
}

impl Value {
    fn get(&self, key: &str) -> Value {
        if let Value::Obj(pairs) = self {
            for (k, v) in pairs {
                if k.as_str() == key {
                    return v.clone();
                }
            }
        }
        Value::Null
    }
    fn as_f64(&self) -> f64 {
        match self {
            Value::Num(n) => *n,
            _ => panic!("expected number"),
        }
    }
    fn as_i64(&self) -> i64 {
        self.as_f64() as i64
    }
    fn as_array(&self) -> &Vec<Value> {
        match self {
            Value::Arr(v) => v,
            _ => panic!("expected array"),
        }
    }
    fn as_vec_i64(&self) -> Vec<i64> {
        self.as_array().iter().map(|v| v.as_i64()).collect()
    }
    fn from_i64(n: i64) -> Value {
        Value::Num(n as f64)
    }
    fn from_vec_i64(v: Vec<i64>) -> Value {
        Value::Arr(v.into_iter().map(Value::from_i64).collect())
    }
}

// ---- conversion between JSON `Value` and solution types ----

trait FromValue {
    fn from_value(v: &Value) -> Self;
}

trait ToValue {
    fn to_value(self) -> Value;
}

impl FromValue for i64 {
    fn from_value(v: &Value) -> Self {
        v.as_i64()
    }
}
impl ToValue for i64 {
    fn to_value(self) -> Value {
        Value::from_i64(self)
    }
}

impl FromValue for f64 {
    fn from_value(v: &Value) -> Self {
        v.as_f64()
    }
}
impl ToValue for f64 {
    fn to_value(self) -> Value {
        Value::Num(self)
    }
}

impl FromValue for bool {
    fn from_value(v: &Value) -> Self {
        match v {
            Value::Bool(b) => *b,
            _ => panic!("expected bool"),
        }
    }
}
impl ToValue for bool {
    fn to_value(self) -> Value {
        Value::Bool(self)
    }
}

impl FromValue for String {
    fn from_value(v: &Value) -> Self {
        match v {
            Value::Str(s) => s.clone(),
            _ => panic!("expected string"),
        }
    }
}
impl ToValue for String {
    fn to_value(self) -> Value {
        Value::Str(self)
    }
}

impl<T: FromValue> FromValue for Vec<T> {
    fn from_value(v: &Value) -> Self {
        v.as_array().iter().map(T::from_value).collect()
    }
}
impl<T: ToValue> ToValue for Vec<T> {
    fn to_value(self) -> Value {
        Value::Arr(self.into_iter().map(ToValue::to_value).collect())
    }
}

impl<T: FromValue> FromValue for Option<T> {
    fn from_value(v: &Value) -> Self {
        match v {
            Value::Null => None,
            _ => Some(T::from_value(v)),
        }
    }
}
impl<T: ToValue> ToValue for Option<T> {
    fn to_value(self) -> Value {
        match self {
            Some(x) => x.to_value(),
            None => Value::Null,
        }
    }
}

// `solve` is called through this trait so the driver needn't know its arity.
trait Solvable<Args> {
    fn call_with(&self, args: &[Value]) -> Value;
}

macro_rules! impl_solvable {
    ($n:expr; $($arg:ident $idx:tt),+) => {
        impl<F, R, $($arg),+> Solvable<($($arg,)+)> for F
        where
            F: Fn($($arg),+) -> R,
            R: ToValue,
            $($arg: FromValue),+
        {
            fn call_with(&self, args: &[Value]) -> Value {
                assert_eq!(
                    args.len(),
                    $n,
                    "solve takes {} parameter(s) but the testcase input has {}",
                    $n,
                    args.len()
                );
                self($($arg::from_value(&args[$idx])),+).to_value()
            }
        }
    };
}

impl_solvable!(1; A 0);
impl_solvable!(2; A 0, B 1);
impl_solvable!(3; A 0, B 1, C 2);
impl_solvable!(4; A 0, B 1, C 2, D 3);
impl_solvable!(5; A 0, B 1, C 2, D 3, E 4);
impl_solvable!(6; A 0, B 1, C 2, D 3, E 4, G 5);

fn call_solve(input: &Value) -> Value {
    let args: Vec<Value> = match input {
        Value::Obj(pairs) => pairs.iter().map(|(_, v)| v.clone()).collect(),
        _ => panic!("\"input\" must be a JSON object"),
    };
    solve.call_with(&args)
}

struct Parser<'a> {
    s: &'a [u8],
    pos: usize,
}

impl<'a> Parser<'a> {
    fn new(s: &'a str) -> Self {
        Parser { s: s.as_bytes(), pos: 0 }
    }

    fn peek(&self) -> u8 {
        self.s[self.pos]
    }

    fn skip_ws(&mut self) {
        while self.pos < self.s.len() && (self.peek() as char).is_whitespace() {
            self.pos += 1;
        }
    }

    fn parse_value(&mut self) -> Value {
        self.skip_ws();
        match self.peek() {
            b'{' => self.parse_object(),
            b'[' => self.parse_array(),
            b'"' => Value::Str(self.parse_string()),
            b't' => {
                self.pos += 4;
                Value::Bool(true)
            }
            b'f' => {
                self.pos += 5;
                Value::Bool(false)
            }
            b'n' => {
                self.pos += 4;
                Value::Null
            }
            _ => self.parse_number(),
        }
    }

    fn parse_object(&mut self) -> Value {
        self.pos += 1; // {
        let mut pairs = Vec::new();
        self.skip_ws();
        if self.peek() == b'}' {
            self.pos += 1;
            return Value::Obj(pairs);
        }
        loop {
            self.skip_ws();
            let key = self.parse_string();
            self.skip_ws();
            self.pos += 1; // :
            let value = self.parse_value();
            pairs.push((key, value));
            self.skip_ws();
            match self.peek() {
                b',' => {
                    self.pos += 1;
                }
                b'}' => {
                    self.pos += 1;
                    break;
                }
                _ => panic!("bad object"),
            }
        }
        Value::Obj(pairs)
    }

    fn parse_array(&mut self) -> Value {
        self.pos += 1; // [
        let mut items = Vec::new();
        self.skip_ws();
        if self.peek() == b']' {
            self.pos += 1;
            return Value::Arr(items);
        }
        loop {
            let value = self.parse_value();
            items.push(value);
            self.skip_ws();
            match self.peek() {
                b',' => {
                    self.pos += 1;
                }
                b']' => {
                    self.pos += 1;
                    break;
                }
                _ => panic!("bad array"),
            }
        }
        Value::Arr(items)
    }

    fn parse_string(&mut self) -> String {
        self.pos += 1; // opening quote
        let mut out = String::new();
        loop {
            let c = self.peek();
            if c == b'"' {
                self.pos += 1;
                break;
            }
            if c == b'\\' {
                self.pos += 1;
                let esc = self.peek();
                match esc {
                    b'n' => out.push('\n'),
                    b't' => out.push('\t'),
                    b'"' => out.push('"'),
                    b'\\' => out.push('\\'),
                    other => out.push(other as char),
                }
                self.pos += 1;
            } else {
                out.push(c as char);
                self.pos += 1;
            }
        }
        out
    }

    fn parse_number(&mut self) -> Value {
        let start = self.pos;
        if self.peek() == b'-' {
            self.pos += 1;
        }
        while self.pos < self.s.len() {
            let c = self.peek();
            if c.is_ascii_digit() || c == b'.' || c == b'e' || c == b'E' || c == b'+' || c == b'-' {
                self.pos += 1;
            } else {
                break;
            }
        }
        let slice = std::str::from_utf8(&self.s[start..self.pos]).unwrap();
        Value::Num(slice.parse().unwrap())
    }
}

fn parse_json(s: &str) -> Value {
    Parser::new(s).parse_value()
}

fn to_json_string(v: &Value) -> String {
    match v {
        Value::Null => "null".to_string(),
        Value::Bool(b) => b.to_string(),
        Value::Num(n) => {
            if n.fract() == 0.0 && n.abs() < 1e15 {
                format!("{}", *n as i64)
            } else {
                format!("{}", n)
            }
        }
        Value::Str(s) => format!("\"{}\"", s.replace('\\', "\\\\").replace('"', "\\\"")),
        Value::Arr(items) => {
            let parts: Vec<String> = items.iter().map(to_json_string).collect();
            format!("[{}]", parts.join(","))
        }
        Value::Obj(pairs) => {
            let parts: Vec<String> = pairs
                .iter()
                .map(|(k, v)| format!("\"{}\":{}", k, to_json_string(v)))
                .collect();
            format!("{{{}}}", parts.join(","))
        }
    }
}

// ---- driver ----

fn read_peak_memory_kb() -> f64 {
    let status = std::fs::read_to_string("/proc/self/status").unwrap_or_default();
    for line in status.lines() {
        if let Some(rest) = line.strip_prefix("VmHWM:") {
            if let Some(kb) = rest.split_whitespace().next() {
                return kb.parse().unwrap_or(0.0);
            }
        }
    }
    0.0
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("usage: (via run_rust.py) <testcases.json>");
        std::process::exit(2);
    }

    let content = std::fs::read_to_string(&args[1]).expect("failed to read testcases file");
    let parsed = parse_json(&content);
    let cases = parsed.as_array();

    let start = std::time::Instant::now();
    let mut failures: Vec<String> = Vec::new();
    for (i, case) in cases.iter().enumerate() {
        let input = case.get("input");
        let expected = case.get("expected");
        let actual = call_solve(&input);
        if actual != expected {
            failures.push(format!(
                "case {}: expected {}, got {}",
                i,
                to_json_string(&expected),
                to_json_string(&actual)
            ));
        }
    }
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;
    let memory_kb = read_peak_memory_kb();

    let status = if failures.is_empty() { "passed" } else { "failed" };
    let details = if failures.is_empty() {
        format!("{} case(s) passed", cases.len())
    } else {
        failures.join("; ")
    };

    let result = Value::Obj(vec![
        ("status".to_string(), Value::Str(status.to_string())),
        ("runtime_ms".to_string(), Value::Num((elapsed_ms * 1000.0).round() / 1000.0)),
        ("memory_kb".to_string(), Value::Num(memory_kb)),
        ("details".to_string(), Value::Str(details)),
    ]);
    println!("{}", to_json_string(&result));
    if status == "failed" {
        std::process::exit(1);
    }
}
