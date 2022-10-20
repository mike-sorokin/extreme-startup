import React from "react"
import { useParams } from "react-router-dom"
import { Button } from "@mantine/core"

function Player() {

  const params = useParams()

  const deletePlayer = (id) => {
    console.log("deleted player", id)
  }

  const events = [{ id: "1", request: "request1" },
  { id: "2", request: "request2" }]

  return (
    <div>
      <div> Hello {params.id}</div>
      <div> Your score is: </div>
      <Button onClick={() => { deletePlayer(params.id) }}> Withdraw</Button>
      <ul>
        {events.map((event) => (<p key={event.id}> {event.request} </p>))}
      </ul>
    </div>
  )
}

export default Player
