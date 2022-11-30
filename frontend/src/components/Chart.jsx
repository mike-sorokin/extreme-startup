import React, { useState, useEffect } from 'react'
import { Line, LineChart, CartesianGrid, XAxis, YAxis } from 'recharts'
import { MD5 } from 'crypto-js'
import { require } from 'requirejs'

import { fetchAllPlayers, fetchGameScores } from '../utils/requests'

function Chart ({ gameId }) {
  const [chartData, setChartData] = useState([])
  const [playerIds, setPlayerIds] = useState([])
  const tinycolor = require('tinycolor2')

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
        console.error(error)
        if (error.response && error.response.status === 406) {
          console.error('invalid game id')
        }
      }
    }

    getChartData()
    const timer = setInterval(getChartData, 2000)
    return () => {
      clearInterval(timer)
    }
  }, [])

  const stringToColour = (str) => {
    const prefix = '#'
    const hash = MD5(str).toString().substring(0, 6)
    const colourStr = prefix.concat(hash)
    const colour = tinycolor(colourStr)
    while (colour.getBrightness() < 75) {
      colour.lighten(20)
    }
    return colour.toHexString()
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
          isAnimationActive={false}
          name={p.name}
          dataKey={p.id}
          stroke={stringToColour(p.name)}
          yAxisId={1}
          dot={false}/>
        })}
      </LineChart>
    </div>
  )
}

export default Chart
