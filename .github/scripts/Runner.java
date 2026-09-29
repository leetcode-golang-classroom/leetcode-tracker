// Generic verification driver for a Java solution file. No external deps —
// JSON is hand-rolled into native Java types (Map/List/Double/String/Boolean).
//
// Convention: the solution file declares a package-private `class Solution`
// with `static Object solve(Map<String, Object> input)`. Compiled together
// with this driver by run_java.sh (which renames the solution file to
// Solution.java first, since Java requires public-class-name == file-name
// but is fine with non-public classes under any file name).
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Runner {
    static String src;
    static int pos;

    static void skipWs() {
        while (pos < src.length() && Character.isWhitespace(src.charAt(pos))) pos++;
    }

    static Object parseValue() {
        skipWs();
        char c = src.charAt(pos);
        if (c == '{') return parseObject();
        if (c == '[') return parseArray();
        if (c == '"') return parseString();
        if (c == 't') { pos += 4; return Boolean.TRUE; }
        if (c == 'f') { pos += 5; return Boolean.FALSE; }
        if (c == 'n') { pos += 4; return null; }
        return parseNumber();
    }

    static Map<String, Object> parseObject() {
        pos++; // {
        Map<String, Object> map = new LinkedHashMap<>();
        skipWs();
        if (src.charAt(pos) == '}') { pos++; return map; }
        while (true) {
            skipWs();
            String key = parseString();
            skipWs();
            pos++; // :
            map.put(key, parseValue());
            skipWs();
            char c = src.charAt(pos);
            if (c == ',') pos++;
            else if (c == '}') { pos++; break; }
            else throw new RuntimeException("bad object at " + pos);
        }
        return map;
    }

    static List<Object> parseArray() {
        pos++; // [
        List<Object> list = new ArrayList<>();
        skipWs();
        if (src.charAt(pos) == ']') { pos++; return list; }
        while (true) {
            list.add(parseValue());
            skipWs();
            char c = src.charAt(pos);
            if (c == ',') pos++;
            else if (c == ']') { pos++; break; }
            else throw new RuntimeException("bad array at " + pos);
        }
        return list;
    }

    static String parseString() {
        pos++; // opening quote
        StringBuilder sb = new StringBuilder();
        while (true) {
            char c = src.charAt(pos);
            if (c == '"') { pos++; break; }
            if (c == '\\') {
                pos++;
                char esc = src.charAt(pos);
                switch (esc) {
                    case 'n': sb.append('\n'); break;
                    case 't': sb.append('\t'); break;
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    default: sb.append(esc);
                }
                pos++;
            } else {
                sb.append(c);
                pos++;
            }
        }
        return sb.toString();
    }

    static Object parseNumber() {
        int start = pos;
        if (src.charAt(pos) == '-') pos++;
        while (pos < src.length()) {
            char c = src.charAt(pos);
            if (Character.isDigit(c) || c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') pos++;
            else break;
        }
        return Double.parseDouble(src.substring(start, pos));
    }

    static Object parseJson(String s) {
        src = s;
        pos = 0;
        return parseValue();
    }

    @SuppressWarnings("unchecked")
    static Object normalize(Object o) {
        if (o == null) return null;
        if (o instanceof Number) return ((Number) o).doubleValue();
        if (o instanceof int[]) {
            List<Object> list = new ArrayList<>();
            for (int v : (int[]) o) list.add((double) v);
            return list;
        }
        if (o instanceof Object[]) {
            List<Object> list = new ArrayList<>();
            for (Object v : (Object[]) o) list.add(normalize(v));
            return list;
        }
        if (o instanceof List) {
            List<Object> list = new ArrayList<>();
            for (Object v : (List<Object>) o) list.add(normalize(v));
            return list;
        }
        if (o instanceof Map) {
            Map<String, Object> map = new LinkedHashMap<>();
            for (Map.Entry<String, Object> e : ((Map<String, Object>) o).entrySet()) {
                map.put(e.getKey(), normalize(e.getValue()));
            }
            return map;
        }
        return o; // String, Boolean
    }

    static String toJson(Object o) {
        if (o == null) return "null";
        if (o instanceof String) return "\"" + ((String) o).replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
        if (o instanceof Boolean) return o.toString();
        if (o instanceof Double) {
            double d = (Double) o;
            if (d == Math.floor(d) && !Double.isInfinite(d) && Math.abs(d) < 1e15) return String.valueOf((long) d);
            return String.valueOf(d);
        }
        if (o instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            List<?> list = (List<?>) o;
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) sb.append(",");
                sb.append(toJson(list.get(i)));
            }
            return sb.append("]").toString();
        }
        if (o instanceof Map) {
            StringBuilder sb = new StringBuilder("{");
            boolean first = true;
            for (Map.Entry<?, ?> e : ((Map<?, ?>) o).entrySet()) {
                if (!first) sb.append(",");
                first = false;
                sb.append(toJson(String.valueOf(e.getKey()))).append(":").append(toJson(e.getValue()));
            }
            return sb.append("}").toString();
        }
        return "\"" + o + "\"";
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: (via run_java.sh) <testcases.json>");
            System.exit(2);
        }
        String content = new String(Files.readAllBytes(Paths.get(args[0])));
        List<Object> cases = (List<Object>) parseJson(content);

        Runtime rt = Runtime.getRuntime();
        System.gc();
        long memBefore = rt.totalMemory() - rt.freeMemory();
        long start = System.nanoTime();

        List<String> failures = new ArrayList<>();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> testCase = (Map<String, Object>) cases.get(i);
            Map<String, Object> input = (Map<String, Object>) testCase.get("input");
            Object expected = normalize(testCase.get("expected"));
            Object actual = normalize(Solution.solve(input));
            if (!Objects.equals(actual, expected)) {
                failures.add("case " + i + ": expected " + toJson(expected) + ", got " + toJson(actual));
            }
        }

        double elapsedMs = (System.nanoTime() - start) / 1e6;
        long memAfter = rt.totalMemory() - rt.freeMemory();
        double memoryKb = Math.max(0, memAfter - memBefore) / 1024.0;

        String status = failures.isEmpty() ? "passed" : "failed";
        String details = failures.isEmpty() ? (cases.size() + " case(s) passed") : String.join("; ", failures);

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("status", status);
        result.put("runtime_ms", Math.round(elapsedMs * 1000) / 1000.0);
        result.put("memory_kb", Math.round(memoryKb * 10) / 10.0);
        result.put("details", details);
        System.out.println(toJson(result));
        if (!failures.isEmpty()) System.exit(1);
    }
}
