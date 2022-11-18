import React, { useState } from 'react'
import { Line, LineChart, CartesianGrid, XAxis, YAxis } from 'recharts'
import { MD5 } from 'crypto-js'

import { fetchGameScores } from '../utils/requests'

function FinalChart({ gameId, players }) {
  const [chartData, setChartData] = useState([])

  // Update chartData to up-to-date scorelist by refetching it from Flask backend
  // Also refetch the entire player list, just in case
  const getChartData = async () => {
    try {
      const loadOldGame = true
      const response = await fetchGameScores(gameId, loadOldGame)
      setChartData(response)
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 406) {
        console.error('invalid game id')
      }
    }
  }
  getChartData()

  const stringToColour = (str) => {
    const colour = '#'
    const hash = MD5(str).toString().substring(0, 6)
    return colour.concat(hash)
  }

  console.log("lmao")
  console.log(players)

  return (
    <div>
      {
        /* 
          TODO: This is a copypast from Chart. A good idea would be 
          to extract comon code to a separate component 
        */
      }
      <LineChart width={750} height={450} data={chartData}>
        <XAxis dataKey="time" type="number" />
        <YAxis type="number" yAxisId={1} />
        <CartesianGrid stroke="#111" strokeDasharray="5 5" />

        {players?.map((p) => {
          return <Line
            key={p.id}
            connectNulls
            type="monotone"
            isAnimationActive={false}
            name={p.name}
            dataKey={p.id}
            stroke={stringToColour(p.name)}
            yAxisId={1}
            dot={false} />
        })}
      </LineChart>
    </div>
  )
}

export default FinalChart
