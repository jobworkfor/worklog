# 使用 RecyclerView 创建动态列表

**[ Android Jetpack](https://developer.android.com/jetpack) 的一部分。**

RecyclerView 可以让您轻松高效地显示大量数据。您提供数据并定义每个列表项的外观，而 RecyclerView 库会根据需要动态创建元素。

顾名思义，RecyclerView 会回收这些单个的元素。当列表项滚动出屏幕时，RecyclerView 不会销毁其视图。相反，RecyclerView 会对屏幕上滚动的新列表项重用该视图。这种重用可以显著提高性能，改善应用响应能力并降低功耗。

**注意**：RecyclerView 除了是类的名称，也是库的名称。在本页中，采用 `code font` 字体的 `RecyclerView` 始终表示 RecyclerView 库中的类。

## 关键类

将多个不同的类搭配使用，可构建动态列表。

- **[`RecyclerView`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView)** 是包含与您的数据对应的视图的 [`ViewGroup`](https://developer.android.com/reference/android/view/ViewGroup)。它本身就是视图，因此，将 `RecyclerView` 添加到布局中的方式与添加任何其他界面元素相同。
- 列表中的每个独立元素都由一个 ViewHolder 对象进行定义。创建 ViewHolder 时，它并没有任何关联的数据。创建 ViewHolder 后，`RecyclerView` 会将其绑定到其数据。您可以通过扩展 [`RecyclerView.ViewHolder`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.ViewHolder) 来定义 ViewHolder。
- `RecyclerView` 会请求这些视图，并通过在 Adapter 中调用方法，将视图绑定到其数据。您可以通过扩展 [`RecyclerView.Adapter`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter) 来定义 Adapter。
- 布局管理器负责排列列表中的各个元素。您可以使用 RecyclerView 库提供的某个布局管理器，也可以定义自己的布局管理器。布局管理器均基于库的 [`LayoutManager`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.LayoutManager) 抽象类。

您可以在 [RecyclerView 示例应用 (Kotlin)](https://github.com/android/views-widgets-samples/tree/main/RecyclerViewKotlin/) 或 [RecyclerView 示例应用 (Java)](https://github.com/android/views-widgets-samples/tree/main/RecyclerView/) 中查看各部分如何组合在一起。

## 实现 RecyclerView 的步骤

如果您打算使用 RecyclerView，那么您需要完成几项工作。下面几部分对这些工作进行了详细介绍。

- 首先，确定列表或网格的外观。一般来说，您可以使用 RecyclerView 库的某个标准布局管理器。
- 设计列表中每个元素的外观和行为。根据此设计，扩展 `ViewHolder` 类。您的 `ViewHolder` 版本提供了列表项的所有功能。您的 ViewHolder 是 `View` 的封装容器，且该视图由 `RecyclerView` 管理。
- 定义用于将您的数据与 `ViewHolder` 视图相关联的 `Adapter`。

此外，您还可以使用[高级自定义选项](https://developer.android.com/guide/topics/ui/layout/recyclerview-custom)根据自己的具体需求定制 RecyclerView。

## 规划布局

RecyclerView 中的列表项由 [`LayoutManager`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.LayoutManager) 类负责排列。RecyclerView 库提供了三种布局管理器，用于处理最常见的布局情况：

- [`LinearLayoutManager`](https://developer.android.com/reference/androidx/recyclerview/widget/LinearLayoutManager) 将各个项排列在一维列表中。

- `GridLayoutManager`

   

  将所有项排列在二维网格中：

  - 如果网格垂直排列，`GridLayoutManager` 会尽量使每行中所有元素的宽度和高度相同，但不同的行可以有不同的高度。
  - 如果网格水平排列，`GridLayoutManager` 会尽量使每列中所有元素的宽度和高度相同，但不同的列可以有不同的宽度。

- [`StaggeredGridLayoutManager`](https://developer.android.com/reference/androidx/recyclerview/widget/StaggeredGridLayoutManager) 与 `GridLayoutManager` 类似，但不要求同一行中的列表项具有相同的高度（垂直网格有此要求）或同一列中的列表项具有相同的宽度（水平网格有此要求）。其结果是，同一行或同一列中的列表项可能会错落不齐。

您还需要设计各个列表项的布局。在设计 ViewHolder 时，您需要使用此布局，如下一部分所述。

## 实现 Adapter 和 ViewHolder

确定布局后，您需要实现 `Adapter` 和 `ViewHolder`。这两个类配合使用，共同定义数据的显示方式。`ViewHolder` 是包含列表中各列表项的布局的 `View` 的封装容器。`Adapter` 会根据需要创建 `ViewHolder` 对象，还会为这些视图设置数据。将视图与其数据相关联的过程称为“绑定”。

定义 Adapter 时，您需要替换三个关键方法：

- [`onCreateViewHolder()`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter#onCreateViewHolder(android.view.ViewGroup, int))：每当 `RecyclerView` 需要创建新的 `ViewHolder` 时，它都会调用此方法。此方法会创建并初始化 `ViewHolder` 及其关联的 `View`，但不会填充视图的内容，因为 `ViewHolder` 此时尚未绑定到具体数据。
- [`onBindViewHolder()`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter#onBindViewHolder(VH, int))：`RecyclerView` 调用此方法将 `ViewHolder` 与数据相关联。此方法会提取适当的数据，并使用该数据填充 ViewHolder 的布局。例如，如果 `RecyclerView` 显示的是一个名称列表，该方法可能会在列表中查找适当的名称，并填充 ViewHolder 的 [`TextView`](https://developer.android.com/reference/android/widget/TextView) widget。
- [`getItemCount()`](https://developer.android.com/reference/androidx/recyclerview/widget/RecyclerView.Adapter#getItemCount())：RecyclerView 调用此方法来获取数据集的大小。例如，在通讯簿应用中，这可能是地址总数。RecyclerView 使用此方法来确定什么时候没有更多的列表项可以显示。

下面是一个典型的简单 Adapter 示例，该 Adapter 包含一个显示数据列表的嵌套 `ViewHolder`。在本例中，RecyclerView 显示了一个简单的文本元素列表。系统会向 Adapter 传递一个字符串数组，该数组包含了 `ViewHolder` 元素的文本。

[Kotlin](https://developer.android.com/guide/topics/ui/layout/recyclerview#kotlin)[Java](https://developer.android.com/guide/topics/ui/layout/recyclerview#java)

```kotlin
class CustomAdapter(private val dataSet: Array<String>) :
        RecyclerView.Adapter<CustomAdapter.ViewHolder>() {

    /**
     * Provide a reference to the type of views that you are using
     * (custom ViewHolder).
     */
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val textView: TextView

        init {
            // Define click listener for the ViewHolder's View.
            textView = view.findViewById(R.id.textView)
        }
    }

    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        // Create a new view, which defines the UI of the list item
        val view = LayoutInflater.from(viewGroup.context)
                .inflate(R.layout.text_row_item, viewGroup, false)

        return ViewHolder(view)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {

        // Get element from your dataset at this position and replace the
        // contents of the view with that element
        viewHolder.textView.text = dataSet[position]
    }

    // Return the size of your dataset (invoked by the layout manager)
    override fun getItemCount() = dataSet.size

}
```

每个视图项的布局照例在 XML 布局文件中定义。在本例中，应用包含一个 `text_row_item.xml` 文件，如下所示：

```xml
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="@dimen/list_item_height"
    android:layout_marginLeft="@dimen/margin_medium"
    android:layout_marginRight="@dimen/margin_medium"
    android:gravity="center_vertical">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/element_text"/>
</FrameLayout>
```

## 后续步骤

您可能只需要这样一个简单的 `RecyclerView` 实现。不过，该库还提供了许多其他方式供您对实现进行自定义。如需了解详情，请参阅[高级 RecyclerView 自定义](https://developer.android.com/guide/topics/ui/layout/recyclerview-custom)。

## 其他资源

如需详细了解如何在 Android 平台上进行测试，请参阅以下资源。

### 示例应用

- [RecyclerView 示例应用 (Kotlin)](https://github.com/android/views-widgets-samples/tree/main/RecyclerViewKotlin/)
- [RecyclerView 示例应用 (Java)](https://github.com/android/views-widgets-samples/tree/main/RecyclerView/)
- [Sunflower 演示版应用](https://github.com/googlesamples/android-sunflower)