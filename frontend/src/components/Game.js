import React from 'react'
import { Outlet, useParams } from "react-router-dom"

function Game() {

  const params = useParams()

  return (
    <div>
      <h1> Extreme Startup - Game {params.gameid} </h1>
      <Outlet />
    </div>
  )
}

export default Game