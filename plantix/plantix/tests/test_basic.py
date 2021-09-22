import plantix 

from collections import Counter

def test_version_can_be_read():
    '''This test is just to make sure the packaging is OK'''
    assert plantix.__version__ is not None

def test_visit_connections_returns_empty_ranked_topics_if_no_connections_given():
    connections, visited, ranked_topics = list(), dict(), Counter()

    plantix.sdk.find_topics(connections, visited, ranked_topics)
    assert ranked_topics == Counter() 

def test_user_uid_0_most_common_topic():
    pass 
