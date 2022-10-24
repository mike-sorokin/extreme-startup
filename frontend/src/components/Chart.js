import React from 'react'
import { useState, useEffect } from "react"
import io from "socket.io-client"
import axios from "axios"
import { Line, LineChart, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts"

function Chart({ gameid }) {

    const [players, setPlayers] = useState([])
    const [scores, setScores] = useState([])

    // Currently runs only once, when the component is first mounted
    // Need to use sockets instead
    useEffect(() => {
        const getScores = async () => {
            const [playerData, scoreData] = await fetchScores()
            setScores([...scores, scoreData])
            setPlayers(playerData)
        }

        getScores();
    }, [])

    // Gets list of players objects and returns list of players
    // and an object with key-value pairs, where the keys are all the player id's
    // and the values are the player's scores 
    const fetchScores = async () => {

        try {
            const response = await axios.get(`/api/${gameid}/players`)
            let scoreData = {}
            let playerData = []
            response.forEach(player => {
                scoreData[player.id] = player.score;
                playerData.push(player.id)
            })

            return [playerData, scoreData]
        } catch (err) {
            console.error(err)

        }
    }

    return (
        <div>
            <LineChart width={750} height={450} data={scores}>
                {/* <XAxis dataKey="name" /> */}
                <YAxis />
                <CartesianGrid stroke="#eee" strokeDasharray="5 5" />

                {players.map((player) => {
                    <Line type="monotone" dataKey={player} stroke="#8884d8" />
                })}
                <Tooltip />
            </LineChart>
        </div>
    )
}

export default Chart