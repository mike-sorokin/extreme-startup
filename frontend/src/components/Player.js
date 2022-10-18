import React from "react"
import { useParams } from "react-router-dom"

function Player() {

  const params = useParams()

  const deletePlayer = (id) => {
    console.log("deleted player", id)
  }

  const events = {
    event1: "test1",
    event2: "test2"
  }

  return (
  <div>
    <h1> Extreme Restartup Game id: </h1>
    <div> Hello {params.id}</div>
    <div> Your score is: </div>
    <div onClick={deletePlayer(params.id)}> Withdraw</div>
  </div>
  )
}

export default Player