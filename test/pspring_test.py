import sys,os
sys.path.append("../../")
from pspring import Configuration, ConfigurationProvider, ApplicationContext,Bean,Autowired

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
    except Exception as e:
        assert True
