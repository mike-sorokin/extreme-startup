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
          <Badge color="red"> NO RESPONSE </Badge>
        )}
        {event.response_type === "WRONG" && (
          <Badge color="orange"> INCORRECT </Badge>
        )}
        {event.response_type === "CORRECT" && (
          <Badge color="green"> CORRECT </Badge>
        )}
      </Group>
    </Card>
  );
}

export default PlayerEventCard;
