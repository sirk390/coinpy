import unittest
from coinpy.tools.event2 import Event, AllreadySubscribedException,\
    NotSubscribedException, Listener, CallArgs, DuplicateKeywordArgument
import mock

class TestEvent(unittest.TestCase):
    def test_Event_NewEvent_HasNoListeners(self):
        event = Event()
        
        listeners = event.get_listeners()
        
        self.assertEquals(listeners, [])
        
    def test_Event_NewEventWithListernerArguement_HasListenersGiven(self):
        event = Event.with_listerners([Listener("listener1")])
        
        listeners = event.get_listeners_methods()
        
        self.assertEquals(listeners, ["listener1"])


    def test_Event_CallIngSubscribe_AddAListenerObject(self):
        event = Event()
        
        event.subscribe("listener1")
        
        self.assertEquals(event.listeners["listener1"], Listener("listener1"))

    def test_Event_CallIngSubscribeWithArgs_AddAListenerWithArgs(self):
        event = Event()
        
        event.subscribe("listener1", "args1", "arg2")
        
        self.assertEquals(event.listeners["listener1"], Listener("listener1", CallArgs(args=("args1", "arg2"))))

    def test_Event_CallIngSubscribeWithKwargs_AddAListenerWithKwargs(self):
        event = Event()
        
        event.subscribe("listener1", kwarg1="kwarg1_value",  kwarg2="kwarg2_value")
        
        self.assertEquals(event.listeners["listener1"], Listener("listener1", 
                                                                  CallArgs(kwargs={"kwarg1": "kwarg1_value", 
                                                                                   "kwarg2" : "kwarg2_value"})))

    def test_Event_WhenAllreadySubscribedCallIngSubscribe_RaisesAnException(self):
        event = Event.with_listerners([Listener("listener1")])
        
        with self.assertRaises(AllreadySubscribedException):
            event.subscribe("listener1")

    def test_Event_CallIngUnsubscribe_RemovesAListener(self):
        event = Event.with_listerners([Listener("listener1")])
        
        event.unsubscribe("listener1")
        
        self.assertEquals(event.get_listeners_methods(), [])

    def test_Event_WhenNotSubscribedCallIngUnsubscribe_RaisesAnException(self):
        event = Event.with_listerners([])
        
        with self.assertRaises(NotSubscribedException):
            event.unsubscribe("listener1")

    def test_Event_CreateAnEventWithListener_GetListernerReturnsSameValue(self):
        event = Event.with_listerners([Listener("listener1")])
        
        self.assertEquals(event.get_listeners(), [Listener("listener1")])

    def test_Event_SubscribeWithArgsAndKwargsFireWithArgsAndKwargs_ListenerIsCalledWithMergedArguments(self):
        mockListener = mock.Mock()
        event = Event()
        event.subscribe(mockListener, "arg1", "arg2", kword1="value1", kword2="value2")
    
        event.fire("arg3", "arg4", kword3="value3", kword4="value4")
    
        mockListener.assert_called_with('arg1', 'arg2', 'arg3', 'arg4', kword4='value4', kword3='value3', kword2='value2', kword1='value1')
    
    def test_Event_SubscribeAndFireWithDupplicateKeyword_RaisesException(self):
        mockListener = mock.Mock()
        event = Event()
        event.subscribe(mockListener, kword1="value1")
    
        with self.assertRaises(DuplicateKeywordArgument):
            event.fire(kword1="value2")


    def test_Event_SubscribeInACallBack_CallbackIsSubscribed(self):
        def subscriber_callback(event, callback2):
            event.subscribe(callback2)
        event = Event()
        event.subscribe(subscriber_callback, event=event, callback2="callback1")
    
        event.fire()

        self.assertTrue(event.is_subscribed("callback1"))
        
    def test_Event_UnsubscribeItselfInACallBack_CallbackIsUnsubscribed(self):
        def unsubscriber_callback(event):
            event.unsubscribe(unsubscriber_callback)
        event = Event()
        event.subscribe(unsubscriber_callback, event=event)
    
        event.fire()

        self.assertFalse(event.is_subscribed(unsubscriber_callback))

    def test_Event_FireUsingDifferentCallMethod_CallMethodIsCalled(self):
        mock_call_method = mock.Mock()
        event = Event(call_method=mock_call_method)
        event.subscribe("fct1", "arg1")
    
        event.fire("arg2")

        mock_call_method.assert_called_with("fct1", "arg1", "arg2")

    def test_CallArgs_AddCallArgsWithOptionalArguments_AppendsOptionalArguments(self):
        c1 = CallArgs(args=("a", "b"))
        c2 = CallArgs(args=("c", "d"))
        
        result = c1 + c2
        
        self.assertEquals( result, CallArgs(args=("a", "b", "c", "d")))
        
    def test_CallArgs_AddCallArgsWithKeyWordArguments_MergesKeyWordArguments(self):
        c1 = CallArgs(kwargs={"a":1, "b":2})
        c2 = CallArgs(kwargs={"c":3, "d":4})
        
        result = c1 + c2
        
        self.assertEquals( result, CallArgs(kwargs={"a":1, "b":2, "c":3, "d":4}))
        
    def test_CallArgs_AddWithBothOptionalAndKeyWordArguments_AppendsOptionAndMergesKeyWordArguments(self):
        c1 = CallArgs(args=("1", "2"), kwargs={"a":1, "b":2})
        c2 = CallArgs(args=("3", "4"), kwargs={"c":3, "d":4})
        
        result = c1 + c2
        
        self.assertEquals( result, CallArgs(args=("1", "2", "3", "4"), kwargs={"a":1, "b":2, "c":3, "d":4}))
        


        
if __name__ == '__main__':
    unittest.main()
    
