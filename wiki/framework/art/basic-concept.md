









### What are the 'shadow$_klass_' and 'shadow$_monitor_' variables for in java.lang.Object?

In the latest android update (SDK 21), it appears that 2 new variables have been added to java.lang.Object:
```
private transient Class<?> shadow$_klass_;
private transient int shadow$_monitor_;
```
I notice that shadow$_monitor_ is briefly used in hashCode():
```
public int hashCode() {
    int lockWord = shadow$_monitor_;
    final int lockWordMask = 0xC0000000;  // Top 2 bits.
    final int lockWordStateHash = 0x80000000;  // Top 2 bits are value 2 (kStateHash).
    if ((lockWord & lockWordMask) == lockWordStateHash) {
        return lockWord & ~lockWordMask;
    }
    return System.identityHashCode(this);
}
```
But otherwise there are no references to them. Are they somehow related to GC in ART? Or some sort of native stuff?

#### Answer
They are indeed connected to GC. They seem to have been added in order to support Brooks pointers. I found some information on Brooks pointers here:

The idea is that each object on the heap has one additional reference field. This field either points to the object itself, or, as soon as the object gets copied to a new location, to that new location. This will enable us to evacuate objects concurrently with mutator threads
See especially these two commits:

* [libcore: a7c69f785f7d1b07b7da22cfb9150c584ee143f4](https://android.googlesource.com/platform/libcore/+/a7c69f785f7d1b07b7da22cfb9150c584ee143f4)
* [art: 9d04a20bde1b1855cefc64aebc1a44e253b1a13b](https://android.googlesource.com/platform/art/+/9d04a20bde1b1855cefc64aebc1a44e253b1a13b)

> [from stackoverflow](http://stackoverflow.com/questions/26933888/what-are-the-shadow-klass-and-shadow-monitor-variables-for-in-java-lang)

#### comment in code
libcore\ojluni\src\main\java\java\lang\Object.java
```
    /**
     * Returns the runtime class of this {@code Object}. The returned
     * {@code Class} object is the object that is locked by {@code
     * static synchronized} methods of the represented class.
     *
     * <p><b>The actual result type is {@code Class<? extends |X|>}
     * where {@code |X|} is the erasure of the static type of the
     * expression on which {@code getClass} is called.</b> For
     * example, no cast is required in this code fragment:</p>
     *
     * <p>
     * {@code Number n = 0;                             }<br>
     * {@code Class<? extends Number> c = n.getClass(); }
     * </p>
     *
     * @return The {@code Class} object that represents the runtime
     *         class of this object.
     * @see    Class Literals, section 15.8.2 of
     *         <cite>The Java&trade; Language Specification</cite>.
     */
    public final Class<?> getClass() {
      return shadow$_klass_;
    }
```