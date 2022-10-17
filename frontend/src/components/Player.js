import React from "react"
import { useParams } from "react-router-dom"

function Player() {

  const params = useParams()

  return (
  <div>
    <div>team id: {params.id}</div>
  </div>
  )
}

export default Player