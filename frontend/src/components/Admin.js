import React from 'react'
import { Button } from "@mantine/core"

function Admin() {

  const pauseGame = () => {
    console.log("pause")
  }

  const advanceRound = () => {
    console.log("advance")
  }

  return (
    <div>
      <h1>Admin</h1>
      <Button onClick={pauseGame()}>Pause Game</Button>
      <Button onClicc={advanceRound()}>Advance Round</Button>
    </div>
  )
}

export default Admin