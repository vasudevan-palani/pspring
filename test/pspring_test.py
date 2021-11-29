import sys,os,time
sys.path.insert(0,".")
from pspring import Configuration, ConfigurationProvider, ApplicationContext,Bean,Autowired, JsonConfigProvider

def test_defaults():
    Configuration.defaults({
        "a.b.c" : "123"
    })
    assert Configuration.getProperty("a.b.c") == "123"

def test_ConfigurationProvider():
    class TestConfigProvider(ConfigurationProvider):
        def __init__(self):
            self.data={
                "pspring.test.name" : "myname"
            }
        def getProperty(self,propertyName):
            return self.data.get(propertyName)

    Configuration.initialize([TestConfigProvider()])
    assert Configuration.getProperty("pspring.test.name") == "myname"

def test_EnvConfig():
    os.environ["pspring.test.name"] = "environname"
    class TestConfigProvider(ConfigurationProvider):
        def __init__(self):
            self.data={
                "pspring.test.name" : "myname"
            }
        def getProperty(self,propertyName):
            return self.data.get(propertyName)

    Configuration.initialize([TestConfigProvider()])
    assert Configuration.getProperty("pspring.test.name") == "environname"

def test_beanwithargs():

    @Bean(args={"q":"1","b":"2"})
    class Test1():
        def __init__(self,q,b):
            self.q=q
            self.b=b

        def getQ(self):
            return self.q

    class Test2():
        @Autowired()
        def getVal(self,test1:Test1):
            return test1.getQ()

    ApplicationContext.initialize()

    assert Test2().getVal() == "1"

def test_beanfrommethod():
    ApplicationContext.clear()

    class Test1():
        def __init__(self,q):
            self.q = q

        def getQ(self):
            return self.q

    @Bean(name="testbean")
    def getBean():
        return Test1(1)

    ApplicationContext.initialize()

    assert ApplicationContext.resolve("testbean",None).getQ() == 1

def test_autowired():

    @Bean()
    class Test1():
        def __init__(self):
            pass

        def getName(self):
            return "testName"

    class Test2():
        @Autowired()
        def getTestName(self,name:Test1):
            #print(name.getName())
            return name.getName()

    ApplicationContext.initialize()

    assert Test2().getTestName() == "testName"

def test_autowiredsubclass():

    class Test():
        def __init__(self):
            pass

        def getName(self):
            return "testName"

    @Bean()
    class Test1(Test):
        def __init__(self):
            pass

        def getName(self):
            return "testName1"


    class Test3():
        @Autowired()
        def getTestName(self,name:Test):
            #print(name.getName())
            return name.getName()

    ApplicationContext.initialize()
    assert Test3().getTestName() == "testName1"

def test_autowiredsubclassconflict():

    class Test():
        def __init__(self):
            pass

        def getName(self):
            return "testName"

    @Bean()
    class Test1(Test):
        def __init__(self):
            pass

        def getName(self):
            return "testName"

    @Bean()
    class Test2(Test):
        def __init__(self):
            pass

        def getName(self):
            return "testName"

    class Test3():
        @Autowired()
        def getTestName(self,name:Test):
            #print(name.getName())
            return name.getName()

    ApplicationContext.initialize()
    try:
        Test3().getTestName() == "testName"
        assert False
    except Exception as e:
        assert True

def test_jsonconfigprovider():
    configp = JsonConfigProvider({"name":"vasu"})
    Configuration.initialize([configp])

    config = Configuration.getConfig(__name__)

    assert config.getProperty("name") == "vasu"


def test_funcastrue():
    configp = JsonConfigProvider({"name":"vasu"})
    Configuration.initialize([configp])

    config = Configuration.getConfig(__name__)

    getName = config.getProperty("name", Func=True)
    assert getName() == "vasu"



def test_funcasfalse():
    configp = JsonConfigProvider({"name":"vasu"})
    Configuration.initialize([configp])

    config = Configuration.getConfig(__name__)

    name = config.getProperty("name", Func=False)
    assert name == "vasu"


def test_funcasfalse_useitasfunc():
    configp = JsonConfigProvider({"name":"vasu"})
    Configuration.initialize([configp])

    config = Configuration.getConfig(__name__)

    name = config.getProperty("name", Func=False)

    try:
        name() == "vasu"
        assert False
    except Exception as e:
        assert True

