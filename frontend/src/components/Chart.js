import React, { useState, useEffect, useCallback } from 'react'
import { Line, LineChart, CartesianGrid, YAxis, Tooltip } from 'recharts'
import { MD5 } from 'crypto-js'

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
        const playerDataObj = {
          id: player.id,
          name: player.name
        }
        playerData.push(playerDataObj)
      })

      return [playerData, scoreData]
    } catch (err) {
      // TODO
    }
  }, [gameId])

  // TODO use sockets instead?
  useEffect(() => {
    stringToColour('d')
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

  const stringToColour = (str) => {
    const colour = '#'
    const hash = MD5(str).toString().substring(0, 6)
    return colour.concat(hash)
  }

  return (
    <div>
      <LineChart width={750} height={450} data={scores}>
        {/* <XAxis dataKey="name" /> */}
        <YAxis />
        <CartesianGrid stroke="#111" strokeDasharray="5 5" />

        {players.map((playerDataObj) => {
          // eslint-disable-next-line react/jsx-key
          return <Line
          key={playerDataObj.id}
          type="monotone"
          animationDuration={300}
          name={playerDataObj.name}
          dataKey={playerDataObj.id}
          stroke={stringToColour(playerDataObj.name)}
          dot={false}/>
        })}
        <Tooltip />
      </LineChart>
    </div>
  )
}

export default Chart

// TEMPORARY
// <LineChart width={750} height={450} data={speeddata}>
//   <XAxis dataKey="time" type="number"/>
//   <YAxis type="number" yAxisId={1}/>
//   <CartesianGrid stroke="#111" strokeDasharray="5 5" />
//
//   <Line type="monotone" connectNulls key="speed" dataKey="speed" stroke="#8884d8" yAxisId={1}/>
//   <Line type="monotone" connectNulls key="velocity" dataKey="velocity" stroke="#82ca9d" yAxisId={1}/>
//   <Tooltip />
// </LineChart>
