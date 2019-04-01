# pspring

This is a lightweight framework to enable spring developers to quickly develop apps with annotations/decorators. Inspired by Spring Framework of Java, the framework provides the ability for IOC ( Inversion of control ) and Autowiring the beans.

The default environment variables can always be found `defaultvars.py` file

Below is the index the annotations/decorators supported by this module

* `@Bean(name="")`

  This decorator will register the class or method ( which returns an instance of bean ) to the pspring application context. You can provide an optional `name` attribute to register the bean with a qualified name. Providing no name would register the bean for its type ( and its base classes )
  
  
* `@Autowired(name=beanname)`

  This decorator is the heard of dependency injection and will autowire the arguments of a method ( especially used in `__init__` constructor ). You can provide a list of name value pairs where, `name` is the argument name in the method definition for which a bean named `beanname` would be injected with that qualifier.
 
