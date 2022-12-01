import React, { useState, useEffect } from 'react'
import { Line, LineChart, CartesianGrid, XAxis, YAxis } from 'recharts'

import { fetchGameScores } from '../utils/requests'
import { stringToColour } from '../utils/utils'

function FinalChart ({ gameId, players }) {
  const [chartData, setChartData] = useState([])

  useEffect(() => {
    const getChartData = async () => {
      try {
        const loadOldGame = true
        const response = await fetchGameScores(gameId, loadOldGame)

        const startTime = response[0].time

        response.forEach((pt) => {
          pt.time -= startTime
          pt.time /= 1000
        })

        setChartData(response)
      } catch (error) {
        console.error(error)
        if (error.response && error.response.status === 406) {
          console.error('invalid game id')
        }
      }
    }
    getChartData()
  }, [])

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
