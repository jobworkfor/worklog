SqLite 数据库
============

实现SqLiteOpenHelper
----------------------------------------------------------------------------------------------------
```java
public class MySqlLiteOpenHelper extends SQLiteOpenHel
    public MySqlLiteOpenHelper(Context context, String
        super(context, dbName, null, version);
    }
    /*
    * 当数据第一次被创建的时候该方法会给执行
    * 这个方法特别适合做表的初始化
    * */
    @Override
    public void onCreate(SQLiteDatabase db) {
    }
    /*
    * 当数据库的版本升级的时候会执行该方法
    * 这个方法特别适合做表结构的修改
    * 注意：数据库的版本正能增加不能降低 否则会抛异常
    * */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVe
    }
}
```

SqLite 的增删改查
----------------------------------------------------------------------------------------------------
### 初始化
```java
private MySqlLiteOpenHelper mySqlLiteOpenHelper;
private SQLiteDatabase sDB;
public final String TAG = "SqLiteActivity";
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_sql_lite);
    //这一步操作的时候数据库并不会被创建
    mySqlLiteOpenHelper = new MySqlLiteOpenHelper(this, "db.db", 1);
    //在这一步操作的时候数据库才会被读取或者创建 如果数据库不存在那么将会在/data/data/对应的包名 下建立一个databases目录其中包含刚刚创建的数据库以及其缓存文件
    sDB = mySqlLiteOpenHelper.getWritableDatabase();
}
```

### insert
```java
//执行插入操作
@RequiresApi(api = Build.VERSION_CODES.N)
public void insert(View v) {
    try {
        /*
        * 通过sql语句来插入数据
        * 注意：下面是两种占位符的方式 如果是通过format方法来进行占位符操作需要对【单引号】使用【''】进行转义
        * 如果是通过exceSql方法进行拼接的话那么 是不需要加 【单引号】的
        * */
        //两种拼接sql语句的方式
        String sql = MessageFormat.format("insert into userinfo (username,password)
                             values(''{0}'',''{1}'')", "天王2121", "专刊需求到");
        sDB.execSQL("insert into userinfo (username,password) values(?,?)", new String[]{"天王1", "专刊需求到"});
        //执行sql语句
        sDB.execSQL(sql);
      
        //如果sql语句不太熟练可以通过Google提供的方法进行插入操作
        ContentValues values = new ContentValues();
        values.put("username", "tianwang12121gaidihu");
        values.put("password", "baotazhenheyao");
        
        /*
        * 执行插入
        * 第二个参数是：如果为null 那么 如果values 是null 的话那么就会 向 数据库中插入一条null 行，如
        * 果是可以的话 该参数一般为null 即可
        * 返回值:返回主键的值 如果插入失败那么返回-1
        * */
        long pk= sDB.insert("userinfo", null, values);
        values.clear();
        Toast.makeText(this, "insert successfully!", Toast.LENGTH_SHORT).show();
    } catch (Exception e) {
        Log.i(this.TAG, e.toString());
    }
}
```

### Delete
```java
public void delete(View v) {
    //执行删除操作
    try {
        //返回被删除的行数
        int count = this.sDB.delete("userinfo", "username='天王2121'", null);
        Toast.makeText(this, String.valueOf(count), Toast.LENGTH_SHORT).show();
    } catch (Exception e) {
        Log.i(this.TAG, e.toString());
    }
}
```

### Update
```java
 //执行更新操作
 public void update(View v) {
     //需要进行修改的内容
     ContentValues values = new ContentValues();
     values.put("password", "123456");
     //参数: 需要进行更新操作的表 , 需要更新的内容， 过滤条件 ，过滤条件的值
     //返回值： 返回受营销的行数
     int count = this.sDB.update("userinfo", values, "_id>100", null);
     values.clear();
     Toast.makeText(this, String.valueOf(count), Toast.LENGTH_SHORT).show();
 }
```

### Query
```java
//数据库的查询操作
public void select(View v) {
    Cursor cursor = null;
    //通过sql语句直接查询
    //String sql = "select * from userinfo where _id>100";
    //cursor = this.sDB.rawQuery(sql, null);
    //通过Google提供的方法来进行查询操作
    cursor = this.sDB.query("userinfo", new String[]{"_id", "username", "password"}, "_id > 100", null, null, null, null);
    if (cursor != null) {
        //打印获取到的内容
        while (cursor.moveToNext()) {
            Log.i(this.TAG, cursor.getString(cursor.getColumnIndex("_id")));
            Log.i(this.TAG, cursor.getString(cursor.getColumnIndex("username")));
            Log.i(this.TAG, cursor.getString(cursor.getColumnIndex("password")));
        }
    } else {
        Toast.makeText(this, "我就是null了", Toast.LENGTH_SHORT).show();
    }
}
```
