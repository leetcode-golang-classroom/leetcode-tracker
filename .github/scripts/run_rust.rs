// Generic verification driver for a Rust solution file. Compiled with plain
// `rustc` (no Cargo/serde) via the run_rust.py wrapper, which sets the
// SOLUTION_PATH env var and splices the solution file in at compile time.
//
// Convention: the solution file defines `fn solve(input: &Value) -> Value`
// using the minimal JSON `Value` type below (no external crates needed).
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
        let actual = solve(&input);
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
