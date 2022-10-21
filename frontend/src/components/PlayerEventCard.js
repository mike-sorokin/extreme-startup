import React from "react";
import { Card, Badge, Group } from "@mantine/core";

function PlayerEventCard({ event }) {
  return (
    <Card key={event.id} shadow="sm" radius="md" withBorder>
      <Group>
        <div>id: {event.id}</div>
        <div>difficulty: {event.difficulty}</div>
        <div>{event.points_gained} points </div>
        {event.response_type === "NO_RESPONSE" && (
          <div>
            <Badge color="red"> NO RESPONSE </Badge>
          </div>
        )}
        {event.response_type === "WRONG" && (
          <div>
            <Badge color="orange"> INCORRECT </Badge>
          </div>
        )}
        {event.response_type === "CORRECT" && (
          <div>
            <Badge color="green"> CORRECT </Badge>
          </div>
        )}
      </Group>
    </Card>
  );
}

export default PlayerEventCard;
