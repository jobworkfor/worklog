

### load_properties_from_file("/system/build.prop", NULL);
xref: /system/core/init/property_service.cpp
```java
775void load_system_props() {
776    load_properties_from_file("/system/build.prop", NULL);
777    load_properties_from_file("/odm/build.prop", NULL);
778    load_properties_from_file("/vendor/build.prop", NULL);
779    load_properties_from_file("/factory/factory.prop", "ro.*");
780    load_recovery_id_prop();
781}
```














* 深入讲解Android Property机制 http://www.codeweblog.com/%E6%B7%B1%E5%85%A5%E8%AE%B2%E8%A7%A3android-property%E6%9C%BA%E5%88%B6/
* https://www.jianshu.com/p/4ec914c7e013
* https://www.cnblogs.com/bastard/archive/2012/10/11/2720314.html
