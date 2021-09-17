import json

from collections import Counter
from dataclasses import dataclass
from http.client import HTTPResponse
from typing import List, Tuple
from urllib.request import Request, urlopen as send_request

from plantix.service import ADDRESS, PORT


@dataclass
class PlantExpert(object):
    """Represents a plantix community expert.
    
    Each expert has a unique id, a list of plants
    they can give advice on and a list of other
    expert uid-s they follow.
    """	
    uid: str
    topics: Tuple[str]
    following: Tuple[str]


class PlantixApiClient(object):
    """SDK for our Plantix Community REST API.
    """
    API_ENDPOINT = f"http://{ADDRESS}:{PORT}/community"

    def _fetch(self, method: str, resource: str) -> HTTPResponse:
        """Fetch a resource from the service endpoint over HTTP

        @param method: HTTP verb
        @param resource: Resource path
        """
        return send_request(
            Request(f"{self.API_ENDPOINT}{resource}", method=method)
        )

    def get(self, uid: str) -> PlantExpert:
        """Get a community plant expert by uid.

        @param uid: ID of the expert to fetch
        """
        response = self._fetch("GET", f"/experts/{uid}")
        topics, following = json.load(response)

        return PlantExpert(uid, topics, following)

    def find_topics(self, start: str, n: int) -> List:
        response = self.get(start)
        topics, connections = response.topics, response.following

        visited = dict({response.uid:True})
        ranked_topics = Counter(topics)

        self._visit_connections(connections, visited, ranked_topics)

        return ranked_topics.most_common()[:n]

    def _visit_connections(self, connections: str, visited: dict, ranked_topics: Counter):
        for connection in connections:  
            if not visited.get(connection, 0):
                visited.update({connection:True})
                response = self.get(connection)
                ranked_topics.update(response.topics)
                self._visit_connections(response.following, visited, ranked_topics)

