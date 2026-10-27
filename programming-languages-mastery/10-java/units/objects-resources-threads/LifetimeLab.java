import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

public final class LifetimeLab {
    private static int checks;
    static void require(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
        checks++;
    }
    static final class Packet {
        private final byte[] bytes;
        Packet(byte[] source) {
            if (source == null || source.length == 0 || source.length > 1024)
                throw new IllegalArgumentException("packet length must be 1..1024");
            bytes = source.clone();
        }
        byte first() { return bytes[0]; }
        byte[] snapshot() { return bytes.clone(); }
    }
    static final class AliasedPacket {
        final byte[] bytes;
        AliasedPacket(byte[] source) { bytes = source; }
    }
    static void rebind(Packet local) { local = new Packet(new byte[]{99}); }
    static final class Resource implements AutoCloseable {
        private final String name;
        private final List<String> trace;
        Resource(String name, List<String> trace) {
            this.name = name;
            this.trace = trace;
            trace.add("open:" + name);
        }
        @Override public void close() throws Exception {
            trace.add("close:" + name);
            throw new Exception("close failed:" + name);
        }
        void use() { trace.add("use:" + name); }
    }
    static final class VolatileCounter { volatile int value; }
    static void runPair(Runnable task) throws Exception {
        AtomicReference<Throwable> failure = new AtomicReference<>();
        Runnable guarded = () -> {
            try { task.run(); }
            catch (Throwable error) { failure.compareAndSet(null, error); }
        };
        Thread first = new Thread(guarded, "first");
        Thread second = new Thread(guarded, "second");
        first.start(); second.start();
        first.join(5000); second.join(5000);
        if (first.isAlive() || second.isAlive()) {
            first.interrupt(); second.interrupt();
            first.join(1000); second.join(1000);
            throw new AssertionError("thread completion deadline exceeded");
        }
        if (failure.get() != null) throw new AssertionError("worker failed", failure.get());
    }
    static void ownership() {
        byte[] source = new byte[]{3, 5};
        AliasedPacket broken = new AliasedPacket(source);
        Packet owned = new Packet(source);
        source[0] = 8;
        require(broken.bytes[0] == 8, "final reference still aliases mutable contents");
        require(owned.first() == 3, "constructor copies caller storage");
        byte[] snapshot = owned.snapshot(); snapshot[0] = 42;
        require(owned.first() == 3, "accessor does not leak owned array");
        rebind(owned);
        require(owned.first() == 3, "reference argument copied by value");
        require(!Arrays.equals(source, owned.snapshot()), "copied values evolve independently");
        for (byte[] invalid : new byte[][]{null, new byte[0], new byte[1025]}) {
            try { new Packet(invalid); throw new AssertionError("accepted invalid packet"); }
            catch (IllegalArgumentException expected) { checks++; }
        }
    }
    static void resources() {
        List<String> trace = new ArrayList<>();
        Exception primary = null;
        try (Resource a = new Resource("A", trace); Resource b = new Resource("B", trace)) {
            a.use(); b.use();
            throw new Exception("body failed");
        } catch (Exception error) { primary = error; }
        require(trace.equals(List.of("open:A", "open:B", "use:A", "use:B", "close:B", "close:A")), "reverse close order");
        require(primary != null && primary.getMessage().equals("body failed"), "body failure stays primary");
        require(primary.getSuppressed().length == 2, "both close failures retained");
        require(primary.getSuppressed()[0].getMessage().equals("close failed:B"), "suppressed close order");
        System.out.println("resource_trace=" + String.join(",", trace));
    }
    static void concurrency() throws Exception {
        VolatileCounter counter = new VolatileCounter();
        CyclicBarrier bothRead = new CyclicBarrier(2);
        runPair(() -> {
            int previous = counter.value;
            try { bothRead.await(); } catch (Exception e) { throw new RuntimeException(e); }
            counter.value = previous + 1;
        });
        require(counter.value == 1, "volatile read/write pair loses one increment");
        AtomicInteger atomic = new AtomicInteger();
        runPair(atomic::incrementAndGet);
        require(atomic.get() == 2, "atomic whole update");
        int[] locked = {0}; Object monitor = new Object();
        runPair(() -> { synchronized (monitor) { locked[0]++; } });
        require(locked[0] == 2, "monitor protects whole update");
        System.out.println("counters=volatile_split:" + counter.value + ",atomic:" + atomic.get() + ",monitor:" + locked[0]);
    }
    public static void main(String[] arguments) throws Exception {
        ownership(); resources(); concurrency();
        System.out.println("checks=" + checks);
    }
}
