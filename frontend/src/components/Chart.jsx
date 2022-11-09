import React, { useState, useEffect } from 'react'
import { Line, LineChart, CartesianGrid, XAxis, YAxis, Legend } from 'recharts'
import { MD5 } from 'crypto-js'

import { fetchAllPlayers, fetchGameScores } from '../utils/requests'

function Chart ({ gameId }) {
  const [chartData, setChartData] = useState([])
  const [playerIds, setPlayerIds] = useState([])

  // Update chartData to up-to-date scorelist by refetching it from Flask backend
  // Also refetch the entire player list, just in case
  useEffect(() => {
    const getChartData = async () => {
      try {
        const pResponse = await fetchAllPlayers(gameId)
        setPlayerIds(pResponse.map((p) => ({ id: p.id, name: p.name })))

        const response = await fetchGameScores(gameId)
        const startTime = response[0].time

        response.forEach((pt) => {
          pt.time -= startTime
          pt.time /= 1000
        })
        setChartData(response)
      } catch (error) {
        console.log(error)
      }
    }

    getChartData()
    const timer = setInterval(getChartData, 2000)
    return () => {
      clearInterval(timer)
    }
  }, [])

  const stringToColour = (str) => {
    const colour = '#'
    const hash = MD5(str).toString().substring(0, 6)
    return colour.concat(hash)
  }

  return (
    <div>
      <LineChart width={750} height={450} data={chartData}>
        <XAxis dataKey="time" type="number"/>
        <YAxis type="number" yAxisId={1}/>
        <CartesianGrid stroke="#111" strokeDasharray="5 5" />

        {playerIds.map((p) => {
          return <Line
          key={p.id}
          connectNulls
          type="monotone"
          animationDuration={300}
          name={p.name}
          dataKey={p.id}
          stroke={stringToColour(p.name)}
          yAxisId={1}
          dot={false}/>
        })}
        <Legend/>
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
