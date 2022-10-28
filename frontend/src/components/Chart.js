import React, { useState, useEffect, useCallback } from 'react'
import { Line, LineChart, CartesianGrid, YAxis, Tooltip } from 'recharts'

import { fetchAllPlayers } from '../utils/requests'

function Chart ({ gameId }) {
  const [players, setPlayers] = useState([])
  const [scores, setScores] = useState([])

  // Gets list of players objects and returns list of players
  // and an object with key-value pairs, where the keys are all the player id's
  // and the values are the player's scores
  const fetchScores = useCallback(async () => {
    try {
      const response = await fetchAllPlayers(gameId)
      const scoreData = {}
      const playerData = []
      response.forEach(player => {
        scoreData[player.id] = player.score
        playerData.push(player.id)
      })

      return [playerData, scoreData]
    } catch (err) {
      // TODO
    }
  }, [gameId])

  // TODO use sockets instead?
  useEffect(() => {
    const getScores = async () => {
      const [playerData, scoreData] = await fetchScores()
      setScores(s => [...s, scoreData])
      setPlayers(playerData)
    }

    const timer = setInterval(getScores, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [fetchScores])

  return (
    <div>
      <LineChart width={750} height={450} data={scores}>
        {/* <XAxis dataKey="name" /> */}
        <YAxis />
        <CartesianGrid stroke="#111" strokeDasharray="5 5" />

        {players.map((player) => {
          // eslint-disable-next-line react/jsx-key
          return <Line
          type="monotone"
          animationDuration={300}
          dataKey={player}
          stroke="#8884d8"
          dot={false}/>
        })}
        <Tooltip />
      </LineChart>
    </div>
  )
}

export default Chart
