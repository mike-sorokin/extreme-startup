import { React, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Button, Card } from "@mantine/core";

import PlayerEventCard from "./PlayerEventCard";

function Player() {
  const params = useParams();
  const [events, setEvents] = useState([]);

  // Gets list of events from api (need to implement this with sockets)
  useEffect(() => {
    const getEvents = async () => {
      const events = await fetchEvents();
      console.log(events);
      setEvents(events);
    };

    getEvents();
  }, []);

  // Need to move this into requests.js
  const fetchEvents = async () => {
    try {
      const response = await axios.get(`/api/${params.gameid}/players/${params.id}/events`);
      return response;
    } catch (error) {
      // console.error(error);

      // Only here because no data from real endpoint yet
      return [
        { id: 1, query: "event1", difficulty: 0, response_type: "NO_RESPONSE", points_gained: -5 },
        { id: 2, query: "event2", difficulty: 1, response_type: "WRONG", points_gained: -3 },
        { id: 3, query: "event3", difficulty: 2, response_type: "CORRECT", points_gained: 5 },
      ];
    }
  };

  // Need to move this into requests.js
  const deletePlayer = (id) => {
    console.log("deleted player", id);
  };

  return (
    <div>
      <div> Hello {params.id}</div>
      <div> Your score is: </div>
      <Button
        onClick={() => {
          deletePlayer(params.id);
        }}
      >
        Withdraw
      </Button>
      <Card>
        <ul>
          {events.map((event) => (
            <PlayerEventCard key={event.id} event={event} />
          ))}
        </ul>
      </Card>
    </div>
  );
}

export default Player;
